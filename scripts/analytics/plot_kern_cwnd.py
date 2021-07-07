import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import datetime

from parse_kern_log import get_cwnds, get_packet_loss
from parse_dash_log import get_start_time

import numpy as np

def foo(log_root):
    cwnds_list = get_cwnds(os.path.join(log_root, 'kern.log'), video_only=False, disconnect=-1)

    disconnected = []
    for k, v in cwnds_list.items():
        first_ack = v[0][0]
        # time, size = zip(*v)
        tmp = []
        for time, size in v:
            if time != -1:
                tmp.append(((time - first_ack).total_seconds(), size))
            else:
                disconnected.append(tmp)
                tmp = []
        
        if tmp:
            disconnected.append(tmp)

    return disconnected
            

def plot_kern_cwnd(dash_log_root):
    # init_time = get_start_time(os.path.join(dash_log_root, 'dashjs_metrics.json'))
    # print(datetime.datetime.fromtimestamp(init_time))
    print(os.path.exists(os.path.join(dash_log_root, 'kern.log')))

    cwnds_list = get_cwnds(os.path.join(dash_log_root, 'kern.log'))

    lost_packets = get_packet_loss(os.path.join(dash_log_root, 'kern.log'))
    loss_time, _ = zip(*lost_packets)

    fig, axs = plt.subplots(3, sharex=True)

    # Ugly but functional. cwnds_list is a list of tuples (port, cwnd_changes on that port). Cwnd_changes is a list of tuples itself sorted chronologically. The first item in the tuple is a timestamp
    first_ack = cwnds_list[0][1][0][0]
    for _, cwnds in cwnds_list:
        time, size = zip(*cwnds)
        time_reno = [(t - first_ack).total_seconds() for t in time]
        # for t in loss_time:
        #     print(type(t))
        lt = [(t - first_ack).total_seconds() for t in loss_time]


        plt.plot(time_reno, size, label='Reno')


        axs[0].plot(time_reno, size, label='Reno', color='blue')
        min_t_reno = time_reno[0]
        max_t_reno = time_reno[-1]
        lt_loc = [x for x in lt if x >= min_t_reno and x <= max_t_reno]
        y_vals = [np.interp(x, time_reno, size) for x in lt_loc]

        axs[0].scatter(lt_loc, y_vals, color='red', marker='x', label='Packet Loss')

    print('--')
    cwnds_list = get_cwnds(os.path.join('/', 'vagrant', 'logs', 'tmp', 'newcwv', '3_18','newcwv_newcwvh2', 'kern.log'))
    _, cwnds = cwnds_list[0]
    lost_packets = get_packet_loss(os.path.join('/', 'vagrant', 'logs', 'tmp', 'newcwv', '3_18','newcwv_newcwvh2', 'kern.log'))
    loss_time, _ = zip(*lost_packets)

    time, size = zip(*cwnds)
    first_ack = time[0]
    time = [(t - first_ack).total_seconds() for t in time] 
    loss_time = [(t - first_ack).total_seconds() for t in loss_time]

    y_vals = [np.interp(x, time, size) for x in loss_time]

    plt.plot(time, size, label='Newcwv')
    axs[1].plot(time, size, label='Newcwv', color='orange')
    axs[1].scatter(loss_time, y_vals, label='Packet Loss', marker='x', color='red')

    plt.ylabel('Cwnd (MSS sized packets)')
    plt.xlabel('Time (s)')

    plt.xlim(left=-3, right=max(time_reno) + 3)

    fig = plt.gcf()
    fig.set_size_inches((35, 8))
    # plt.legend()
    for ax in axs:
        ax.legend()

    plt.savefig('cwnd_kernel.png', bbox_inches='tight')


def gen_idle_period_plot():
    fig, axs = plt.subplots(2, sharex=True, sharey=True)

    res = foo('/vagrant/logs/cwv_ver/tc/2sec/10mb/newcwv1/')
    start = end = None
    set_label = True
    avg = []
    for i, period in enumerate(res):
        time, size = zip(*period)
        # print(f'{900_000} / {time[-1] - time[0]} {900_000/ (time[-1] - time[0])}' )
        avg.append((900_000 * 8)/ (time[-1] - time[0]))
        end = time[0]
        if start and end:
            axs[0].axvspan(start, end, color='red', alpha=0.2, label='Idle Period' if set_label else '_no_label')
            set_label = False
        axs[0].plot(time, size, label='Newcwv'if i == 0 else '_nolegend_', c='blue')
        start = time[-1]

    print(len(avg))
    print(avg)
    print(np.average(avg))

    axs[0].axhline(y=30, c='green', label='Link Capacity')
    axs[0].legend()

    print('----')

    res = foo('/vagrant/logs/cwv_ver/tc/2sec/10mb/reno1/')
    start = end = None
    set_label = True
    avg = []
    for i, period in enumerate(res):
        time, size = zip(*period)
        # print(f'{900_000} / {time[-1] - time[0]} {900_000/ (time[-1] - time[0])}' )
        avg.append((900_000 * 8)/ (time[-1] - time[0]))
        end = time[0]
        if start and end:
            axs[1].axvspan(start, end, color='red', alpha=0.2, label='Idle Period' if set_label else '_no_label')
            set_label = False
        axs[1].plot(time, size, label='Reno' if i == 0 else '_nolegend_', c='orange')
        start = time[-1]

    axs[1].axhline(y=30, c='green', label='Link Capacity')
    axs[1].legend()
    print(len(avg))
    print(np.average(avg))

    plt.ylim(bottom=0)
    plt.xlim(left=0, right=60)
    plt.xlabel('Time (s)')
    for ax in axs:
        ax.set_ylabel('CWND Size (packets)')

    plt.savefig('cwv_idle_10mb.png')


if __name__ == '__main__':
    # inp = '/vagrant/logs/tmp/newcwv/newcwv_newcwvh'
    inp = '/vagrant/logs/tmp/newcwv/3_18/newcwv_renoh2'
    # plot_kern_cwnd(inp)

    gen_idle_period_plot()
    # fig, axs = plt.subplots(2, sharex=True)

    # res = foo('/vagrant/logs/cwv_ver/tc/2sec/short/newcwv1/')
    # for i, period in enumerate(res):
    #     time, size = zip(*period)
    #     axs[0].plot(time, size, label='Newcwv'if i == 0 else '_nolegend_', c='blue')
    # axs[0].axhline(y=30, c='red', label='Link Capacity')
    # axs[0].legend()
    # # axs[0].set_xlim((0, 1))


    # res = foo('/vagrant/logs/cwv_ver/tc/2sec/short/reno1/')
    # for i, period in enumerate(res):
    #     time, size = zip(*period)
    #     axs[1].plot(time, size, label='Reno' if i == 0 else '_nolegend_', c='orange')
    # axs[1].axhline(y=30, c='red', label='Link Capacity')
    # axs[1].legend()



    # plt.savefig('cwv_idle.pdf')