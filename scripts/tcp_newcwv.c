/*
 * New-CWV implementation for Linux: draft-ietf-tcpm-newcwv-05.txt
 */

#include <linux/module.h>
#include <net/tcp.h>

#define UNDEF_PIPEACK 	                -1
#define PIPEACK_INIT  			TCP_INFINITE_SSTHRESH
#define TCP_RESTART_WINDOW		1
#define FIVEMINS  			(HZ*75000)
#define NO_OF_BINS                      4
#define IS_VALID                        0x0002
#define IS_RECOVERY                     0x0001
#define nextbin(x)  (((x)+1) & 0x03)
#define prevbin(x)  (((x)-1) & 0x03)

/* contains newcwv state variables */
struct newcwv {
	int psample[NO_OF_BINS];	/* pipeACK samples circular buffer */
	u32 time_stamp[NO_OF_BINS];	/* pipeACK sample timestamps */
	int pipeack;		/* pipeACK value after filtering */
	u8 rsvd;
	u8 head;		/* index for psample array */
	u16 flags;
	u32 prior_in_flight;	/* Packets in flight for cwnd reduction */
	u32 prior_retrans;	/* Retransmission before going into FR */
	u32 prev_snd_una;	/* snd_una when last record kept */
	u32 prev_snd_nxt;	/* snd_una when last record kept */
	u32 cwnd_valid_ts;	/* last time cwnd was found 'validated' */
	u32 psp;		/* pipeACK Sampling Period */
};

/* helper function for division */
static u32 divide_or_zero(u32 dividend, u32 divisor)
{
	if (divisor == 0)
		return 0;
	else
		return (u32) (dividend / divisor);
}

/* adds an element to the circular buffer for maximum filter */
static void add_element(struct newcwv *nc, int val, struct tcp_sock *tp)
{
	nc->head = nextbin(nc->head);
	nc->psample[nc->head] = val;
	nc->time_stamp[nc->head] = tcp_time_stamp(tp);
}

/* This fuction removes all the expired elements from the circular buffer
 * and returns the maximum from the remaining elements
 */
static int remove_expired_element(struct newcwv *nc, struct tcp_sock *tp)
{
	int k = nc->head;
	int tmp = nc->psample[nc->head];

	while (nc->psample[k] != UNDEF_PIPEACK) {
		/* remove expired */
		if (nc->time_stamp[k] < tcp_time_stamp(tp) - nc->psp) {
			nc->psample[k] = UNDEF_PIPEACK;
			continue;
		}

		/* search the maximum */
		if (nc->psample[k] > tmp)
			tmp = nc->psample[k];

		k = prevbin(k);
		if (k == nc->head)
			return tmp;
	}

	return tmp;
}

/* is TCP in the validated phase? */
static inline bool tcp_is_in_vp(struct tcp_sock *tp, int pa)
{
	printk(KERN_INFO "FUNCTION: TCP_IS_IN_VP\n");
	if (pa == UNDEF_PIPEACK)
	{
		printk(KERN_INFO "VALID_STATE: valid\n");
		return true;
	}
	else
	{
		printk(KERN_INFO "VALID_STATE: %d\n", ((pa << 1) >= (tp->snd_cwnd * tp->mss_cache)));
		return ((pa << 1) >= (tp->snd_cwnd * tp->mss_cache));
	}
}

/* reduces the cwnd after 5mins of non-validated phase */
static void datalim_closedown(struct sock *sk)
{
	//printk("5 mins of inactivity detected, reducing CWND\n");
	struct newcwv *nc = inet_csk_ca(sk);
	struct tcp_sock *tp = tcp_sk(sk);
	u32 nc_ts;

	printk(KERN_INFO "FUNCTION: DATALIM_CLOSEDOWN\n");

	nc_ts = nc->cwnd_valid_ts;
	while ((tcp_time_stamp(tp) - nc_ts) > FIVEMINS) {
		printk(KERN_INFO "5 mins passed\n");
		nc_ts += FIVEMINS;
		nc->cwnd_valid_ts = nc_ts;
		tp->snd_ssthresh =
		    max((3 * tp->snd_cwnd) >> 2, tp->snd_ssthresh);
		tp->snd_cwnd =
		    max_t(u32, tp->snd_cwnd >> 1, TCP_INIT_CWND);
	}
}


/* updates pipeack when an ACK is received */
static void update_pipeack(struct sock *sk)
{
	struct newcwv *nc = inet_csk_ca(sk);
	struct tcp_sock *tp = tcp_sk(sk);
	int tmp_pipeack;
	u32 tcp_ts = tcp_time_stamp(tp);

	printk(KERN_INFO "FUNCTION: update_pipeack\n");

	printk(KERN_INFO "srtt: %u (%u) srtt to jifiies: %lu (%u)\n", tp->srtt_us, tp->srtt_us >> 3, usecs_to_jiffies(tp->srtt_us), (u32) usecs_to_jiffies(tp->srtt_us));

	nc->psp = max((u32) (3 * usecs_to_jiffies(tp->srtt_us >> 3)), (u32) HZ);
	printk(KERN_INFO "SRTT %u %u\n", tp->srtt_us, nc->psp);

	if (tp->snd_una >= nc->prev_snd_nxt) {

		/* now get a new pipeack sample */
		tmp_pipeack = tp->snd_una - nc->prev_snd_una;
		nc->prev_snd_una = tp->snd_una;
		nc->prev_snd_nxt = tp->snd_nxt;
		printk(KERN_INFO "TMP PIPEACK: %u psample head: %u\n", tmp_pipeack, nc->psample[nc->head]);

		printk(KERN_INFO "TCP_TS %u nc time_stamp %u head nc psp %u \n", tcp_ts, nc->time_stamp[nc->head], (nc->psp >> 2) );
		/* create a new element at the end of current pmp */
		if (tcp_ts > nc->time_stamp[nc->head] + (nc->psp >> 2))
		{
			add_element(nc, tmp_pipeack, tp);
		}
		else if (tmp_pipeack > nc->psample[nc->head])
		{
			nc->psample[nc->head] = tmp_pipeack;
		}
	}

	nc->pipeack = remove_expired_element(nc, tp);
	printk(KERN_INFO "Current pipeack: %u, current CWND: %u\n", nc->pipeack, tp->snd_cwnd);

	/* check if cwnd is validated */
	if (tcp_is_in_vp(tp, nc->pipeack)) {
		nc->flags |= IS_VALID;
		nc->cwnd_valid_ts = tcp_ts;
	} else {
		nc->flags &= ~IS_VALID;
		datalim_closedown(sk);
	}
}


/* initialises newcwv variables */
static void tcp_newcwv_init(struct sock *sk)
{
	struct newcwv *nc = inet_csk_ca(sk);
	struct tcp_sock *tp = tcp_sk(sk);
	u32 tcp_ts = tcp_time_stamp(tp);

	printk(KERN_INFO "NEWCWV INIT CALLED\n");

	nc->prev_snd_una = tp->snd_una;
	nc->prev_snd_nxt = tp->snd_nxt;

	nc->cwnd_valid_ts = tcp_ts;
	nc->flags = IS_VALID;

	nc->psp = max(3 * (tp->srtt_us >> 3), (u32) HZ);

	nc->head = 0;
	nc->psample[0] = UNDEF_PIPEACK;
	nc->pipeack = UNDEF_PIPEACK;
}


/* cong_avoid action: non dubious ACK received */
static void tcp_newcwv_cong_avoid(struct sock *sk, u32 ack, u32 acked)
{
	struct newcwv *nc = inet_csk_ca(sk);
	struct tcp_sock *tp = tcp_sk(sk);



	nc->prior_in_flight = tcp_packets_in_flight(tp);
	nc->prior_retrans = tp->total_retrans;

	update_pipeack(sk);

	printk(KERN_INFO "FUNCTION: CONG_AVOID %u %u %u\n", nc->pipeack, tp->snd_cwnd, tp->mss_cache);

	//printk(KERN_INFO "is_valid: %d is_cwnd_limited: %d\n", !(nc->flags & IS_VALID), !tcp_is_cwnd_limited(sk));

	/* Check if cwnd is validated */
	if (!(nc->flags & IS_VALID) && !tcp_is_cwnd_limited(sk))
		return;
	//printk(KERN_INFO "Doing Reno\n");

	/* The following is the Reno behaviour */


	//printk(KERN_INFO "slow_start: %d entering slow start: %d acked num: %u\n", tcp_in_slow_start(tp), tp->snd_cwnd <= tp->snd_ssthresh, acked);

	//u32 acked_tmp = acked;
	//u32 cwnd = min(tp->snd_cwnd + acked, tp->snd_ssthresh);

	//acked_tmp -= cwnd - tp->snd_cwnd;
	//printk(KERN_INFO "Calculated cwnd: %u, acked: %u, cwnd_clamp: %u\n", cwnd, acked_tmp, tp->snd_cwnd_clamp);

	//printk(KERN_INFO "slow_start: %d entering slow start: %d acked num: %u\n", tcp_in_slow_start(tp), tp->snd_cwnd <= tp->snd_ssthresh, acked);
	/* In "safe" area, increase. */
	if (tp->snd_cwnd <= tp->snd_ssthresh)
	{
		acked = tcp_slow_start(tp, acked);
		if(!acked)
			return;
	}

	tcp_cong_avoid_ai(tp, tp->snd_cwnd, acked);

}

/* newcwv actions in fast recovery */
static void tcp_newcwv_enter_recovery(struct sock *sk)
{
	struct newcwv *nc = inet_csk_ca(sk);
	struct tcp_sock *tp = tcp_sk(sk);
	u32 pipeack;

	printk(KERN_INFO "FUNCTION: enter_recovery\n");

	nc->flags |= IS_RECOVERY;

	pipeack = (nc->pipeack == UNDEF_PIPEACK) ? 0 : (u32)
	    nc->pipeack;
	pipeack = divide_or_zero(pipeack, (u32) tp->mss_cache);
	tp->snd_cwnd = max(pipeack, nc->prior_in_flight) >> 1;

	/* make sure the min. value for cwnd is 1 */
	tp->snd_cwnd = (tp->snd_cwnd < 1) ? 1 : tp->snd_cwnd;

}


/* newcwv actions at the end of recovery */
static void tcp_newcwv_end_recovery(struct sock *sk)
{
	struct newcwv *nc = inet_csk_ca(sk);
	struct tcp_sock *tp = tcp_sk(sk);
	u32 retrans, pipeack;

	printk(KERN_INFO "FUNCTION: end_recovery\n");

	pipeack = (nc->pipeack == UNDEF_PIPEACK) ? 0 : (u32)
	    nc->pipeack;

	pipeack = divide_or_zero(pipeack, (u32) tp->mss_cache);
	retrans = tp->total_retrans - nc->prior_retrans;
	tp->snd_cwnd = (max(pipeack, nc->prior_in_flight) - retrans) >> 1;
	if (tp->snd_cwnd < TCP_RESTART_WINDOW)
		tp->snd_cwnd = TCP_RESTART_WINDOW;

	tp->snd_ssthresh = tp->snd_cwnd;
	nc->flags &= ~IS_RECOVERY;

	/* restart cwv machine */
	tcp_newcwv_init(sk);

}

/* newcwv actions corresponding to event */
static void tcp_newcwv_event(struct sock *sk, enum tcp_ca_event event)
{
	struct newcwv *nc = inet_csk_ca(sk);
	// const struct inet_connection_sock *icsk = inet_csk(sk);

	switch (event) {
		case CA_EVENT_TX_START:
			printk(KERN_INFO "Got EVENT_TX_START\n");
			datalim_closedown(sk);
			break;

		case CA_EVENT_COMPLETE_CWR:
			printk(KERN_INFO "Got EVENT_COMPLETE_CWR\n");
			if (!(nc->flags & IS_VALID))
				tcp_newcwv_end_recovery(sk);
			break;

		case CA_EVENT_LOSS:
			printk(KERN_INFO "GOT EVENT LOSS\n");
			tcp_newcwv_init(sk);
			break;

	// TODO
	// ACK related events have been moved to in_ack_event function

	// case CA_EVENT_SLOW_ACK:

	// 	switch (icsk->icsk_ca_state) {
	// 	case TCP_CA_Recovery:
	// 		if (!nc->flags)
	// 			tcp_newcwv_enter_recovery(sk);
	// 		break;

	// 	case TCP_CA_Open:
	// 	case TCP_CA_Disorder:
	// 	default:
	// 		break;
	// 	}
	// 	break;

	case CA_EVENT_CWND_RESTART:
		printk(KERN_INFO "FUNCTION: CWND_RESTART\n");
		break;
//	case CA_EVENT_FAST_ACK:
	default:
		printk(KERN_INFO "FUNCTION: UNKNOWN EVENT\n");

		break;
	}

}

/* Slow start threshold resetting after loss */
u32 tcp_newcwv_ssthresh(struct sock *sk)
{
	const struct tcp_sock *tp = tcp_sk(sk);

	/* This is tcp_packets_in_flight */
	u32 prior_in_flight =
	    tp->packets_out - tp->sacked_out - tp->lost_out + tp->retrans_out;

	printk(KERN_INFO "FUNCTION: ssthresh\n");

	printk(KERN_INFO "sshtresh called with %u packets out: %u sacked_out: %u lost_out: %u, retrans_out: %u\n", max(prior_in_flight >> 1U, 2U),
	tp->packets_out, tp->sacked_out, tp->lost_out, tp->retrans_out);

	return max(prior_in_flight >> 1U, 2U);
}

void tcp_newcwv_in_ack_event(struct sock *sk, u32 flags) 
{
	// Check if ACK is associated with slow path
	if(flags & CA_ACK_SLOWPATH) 
	{
		struct newcwv *nc = inet_csk_ca(sk);
		const struct inet_connection_sock *icsk = inet_csk(sk);

		printk(KERN_INFO "SLOW ACK\n");

		switch (icsk->icsk_ca_state) {
			case TCP_CA_Recovery:
				if (!nc->flags){
					printk(KERN_INFO "RECOVERY\n");
					tcp_newcwv_enter_recovery(sk);
				}
				break;

			case TCP_CA_Open:
			case TCP_CA_Disorder:
			default:
				break;
		}
	}

	const struct tcp_sock *tp = tcp_sk(sk);
	const struct inet_sock *isock = inet_sk(sk);

	uint16_t sport = ntohs(isock->inet_sport);
	uint16_t dport = ntohs(isock->inet_dport);

	if(sport == 80) { // HTTP server doing
		printk(KERN_INFO "ACK Received. sourcep: %u dstp: %u proto%u send window: %u recv window %u\n",
			sport, dport, sk->sk_protocol, tp->snd_cwnd, tp->rcv_wnd);
	}


}


u32 tcp_newcwv_undo_cwnd(struct sock *sk)
{
	const struct tcp_sock *tp = tcp_sk(sk);

	u32 min_window = tp->snd_ssthresh / 2;

	u32 new_window = max(tp->snd_cwnd, tp->prior_cwnd);

	printk(KERN_INFO "Undoing cwnd: min_win: %u new_win: %u\n", min_window, new_window);

	//MY:
	// Make sure window is at least snd_ssthresh / 2;
	return max(new_window, min_window); 
}


void tcp_trace_state(struct sock* sk, u8 new_state)
{
	switch(new_state)
	{
		case TCP_CA_CWR:
			printk(KERN_INFO "Trace event: Entering CWR state (ECN mark or qdisc drop)\n");
			break;
		case TCP_CA_Recovery:
			printk(KERN_INFO "Trace event: Loss. Entering fast retransmit state (dup acks)\n");
			break;
		case TCP_CA_Loss:
			printk(KERN_INFO "Trace event: Loss. Entering loss recovery (Timeout)\n");
			break;
	}

}

struct tcp_congestion_ops tcp_newcwv = {
	.flags = TCP_CONG_NON_RESTRICTED,
	.name = "newcwv",
	.init = tcp_newcwv_init,
	.owner = THIS_MODULE,
	.ssthresh = tcp_newcwv_ssthresh,
	.cong_avoid = tcp_newcwv_cong_avoid,
	.cwnd_event = tcp_newcwv_event,
	.undo_cwnd = tcp_newcwv_undo_cwnd,

	//MY:
	//ACK related events have been moved to in_ack_event handle

	.in_ack_event = tcp_newcwv_in_ack_event,


	//MY:
	//tracing loss events
	.set_state = tcp_trace_state,

	// TODO
	// MY:
	//I do not think it makes much sense to re-add it.
	// But if needed CWND could always be bumped to at least "min_cwnd" value when reduced.
	// MY:
	// MIN_CWND was removed in 3.15
	// .min_cwnd = tcp_reno_min_cwnd,
};

/* newcwv registered as congestion control in Linux */
static int __init tcp_newcwv_register(void)
{
	BUILD_BUG_ON(sizeof(struct newcwv) > ICSK_CA_PRIV_SIZE);
	printk(KERN_INFO "Registering NEWCWV1\n");
	tcp_register_congestion_control(&tcp_newcwv);

	return 0;
}

/* unregister when module is disabled */
static void __exit tcp_newcwv_unregister(void)
{
	printk(KERN_INFO "Unregistering NEWCWV1\n");
	tcp_unregister_congestion_control(&tcp_newcwv);
}

module_init(tcp_newcwv_register);
module_exit(tcp_newcwv_unregister);

MODULE_AUTHOR("Ziaul Hossain/Raffaello Secchi/Mihail Yanev");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("NewCwv Reno variant");
