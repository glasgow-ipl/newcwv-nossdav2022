import os
import subprocess
import datetime
import glob

import plot_transmission_acks
import matplotlib.pyplot as plt

def get_video_packets(pcap_path):
    p = subprocess.Popen(f'tcpdump -n -r {pcap_path} -ttttt | grep "10.0.0.1.80 >" | grep seq', stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out: bytes
    lines = out.decode().split('\n')

    lines = lines[:-1] # discard the last (empty) line
    seqs = {}
    print(pcap_path)
    # print(lines[0])
    # init_timestamp = datetime.datetime.fromtimestamp(float(lines[0].split()[0]))
    # print(init_timestamp)
    for i, line in enumerate(lines):
        line = line.split()
        # timestamp = (datetime.datetime.fromtimestamp(float(line[0])) - init_timestamp).seconds
        time_delta_str = line[0]
        hours, minutes, seconds = time_delta_str.split(':')
        seconds, microseconds = seconds.split('.')
        timestamp = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), microseconds=int(microseconds)).total_seconds()


        receiver = line[4]
        seq = line[8]
        if ":" not in seq:
            # this is a setup packet
            continue
        key = f'{receiver} {seq}' # A combination of receiver and sequence numbers is unique for a packet
        if key not in seqs:
            seqs[key] = ([timestamp], 1)
        else:
            lost, count = seqs[key]
            lost.append(timestamp)
            seqs[key] = (lost, count + 1)
        
    return seqs


def count_all_packets(root):
    server_pcap_path = os.path.join(root, 'server.pcap')
    server_packets = get_video_packets(server_pcap_path)

    client_pattern = os.path.join(root, 'client*pcap')
    client_paths = glob.glob(client_pattern)

    
    for client_path in client_paths:
        client_ip = os.path.basename(client_path)[len('client_'):-len('.pcap')]
        client_packets = get_video_packets(client_path)
        for key, (timestamps, occurrence) in client_packets.items():
            packet_timestamps, server_occurrence = server_packets[key]
            server_packets[key] = (packet_timestamps, server_occurrence - occurrence)

    return server_packets

def count_lost_packets(root):
    server_packets = count_all_packets(root)

    import matplotlib.pyplot as plt
    send_info = server_packets.values()
    timestamp_send = {}
    # print('counting')
    for (timestamps, _) in send_info:
        for time in timestamps:
            timestamp_send[time] = timestamp_send.get(time, 0) + 1
    # print('done counting')

    seconds, count = zip(*timestamp_send.items())
    # plt.bar(seconds, count, color='green', label='Sent Packets')

    server_packets = {key: (timestamps, occurrence) for key, (timestamps, occurrence) in server_packets.items() if occurrence != 0}

    # print(server_packets)

    ack_info = plot_transmission_acks.get_ack_info(os.path.join(root, 'server.pcap'))

    # lost_info = []
    # for ack, (timestamps, occurence) in server_packets.items():
    #     seq = int(ack.split(':')[-1])

    # lost_info = server_packets.values()
    # timestamps_lost = {}
    # for timestamps, occurrence in lost_info:
    #     for time in timestamps[:occurrence]:
    #         timestamps_lost[time] = timestamps_lost.get(time, 0) + 1

    # seconds, count = zip(*timestamps_lost.items())
    # plt.bar(seconds, count, color='red', label='Lost Packets')

    # plt.xlim(left=100, right=120)
    # plt.xlabel('Time (s)')
    # plt.ylabel('# of Lost Packets')
    # plt.legend()
    # fig_name = os.path.join('/', 'vagrant', 'img', 'test.png')
    # plt.savefig(fig_name)

    return server_packets

def plot_lost_packets(root):
    server_packets = count_all_packets(root)

    # 102, 105 for 1_newcwv and 1_reno
    PLOT_MIN_TIME = 102
    PLOT_MAX_TIME = 105

    transferred_packets = []
    lost_packets = []
    for seq_id, (timestamps, occurence) in server_packets.items():
        seq = int(seq_id.split(':')[-1][:-1])
        for lost_ts in timestamps[:occurence]:
            if PLOT_MIN_TIME < lost_ts < PLOT_MAX_TIME:
                lost_packets.append((lost_ts, seq))
        for transferred_ts in timestamps[occurence:]:
            if PLOT_MIN_TIME < transferred_ts < PLOT_MAX_TIME:
                transferred_packets.append((transferred_ts, seq))
    
    # transfrerred_filtered = [(transfered)]
    relative_ts, relative_seq = min(min(transferred_packets), min(lost_packets))
    transferred_packets = [(t - relative_ts, s - relative_seq) for (t, s) in transferred_packets]
    lost_packets = [(t - relative_ts, s - relative_seq) for (t, s) in lost_packets]


    transferred_tss, transferred_seqs = zip(*transferred_packets)
    lost_tss, lost_seqs = zip(*lost_packets)


    plt.scatter(transferred_tss, transferred_seqs, c='green', alpha=0.2, label='received')
    plt.scatter(lost_tss, lost_seqs, c='red', alpha=0.2, label='lost')

    # plt.gcf().set_size_inches(12, 4)
    plt.xlim(-0.01, 0.25)
    plt.ylim(bottom=-10000, top=300_000)
    plt.xlabel('Time (s)')
    plt.ylabel('TCP Sequence number')
    plt.legend()

    alg = os.path.basename(root).split('_')[1]
    extension = 'pdf'

    fig_name = f'/vagrant/doc/paper/figures/lost_packets_{alg}.{extension}'
    print(f"saving {fig_name}")
    plt.savefig(fig_name)


if __name__ == '__main__':
    plot_lost_packets('/vagrant/logs/clients/1/DSL/1_newcwv')