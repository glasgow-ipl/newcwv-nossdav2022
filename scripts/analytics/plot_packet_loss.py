import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import datetime
import numpy as np
import sys
import argparse

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import detect_packet_loss
import verify_throughput
import parse_event_log
import parse_access_log
import parse_network_model
import math


def plot_packet_loss(res_root):
    fmt_pcap = '%H:%M:%S.%f'

    fmt_event_log = '%H:%M:%S:%f'

    event_path = os.path.join(res_root, 'events.log')
    
    fig = plt.gcf()
    fig.set_size_inches((35, 5))

    ax1 = plt.subplot(212)

    changes_zipped = parse_event_log.get_bw_changes(event_path)

    server_pcap_path = os.path.join(res_root, 'server.pcap')
    print('Analysing lost packets')
    loss_times = detect_packet_loss.get_lost_packets(server_pcap_path)
    init_time_ts = parse_event_log.get_initial_ts(event_path)
    init_time = datetime.datetime.strptime(init_time_ts, fmt_event_log)

    loss_deltas = [(datetime.datetime.strptime(x, fmt_pcap) - init_time).total_seconds() for x in loss_times]
    print('Done')

    print('Calculating Tput')
    interval = 1
    tput = verify_throughput.calculate_throughput(server_pcap_path, init_time=init_time, interval=interval)
    scale = 1 / interval
    tput = {k / scale: v for k, v in tput.items()}
    print('Done')

    time, tput = zip(*tput.items())
    plt.plot(time, tput, c='b', label='Throughput')

    time_seconds = range(math.ceil(time[-1]))

    print('Getting Link Change info')
    max_x_value = max(time_seconds)
    x0 = (datetime.datetime.strptime(changes_zipped[0][0], fmt_event_log) - init_time).total_seconds()
    y0 = y1 = changes_zipped[0][1] * 1_000_000
    x1 = (datetime.datetime.strptime(changes_zipped[1][0], fmt_event_log) - datetime.datetime.strptime(changes_zipped[0][0], fmt_event_log)).total_seconds()
    changes_lines = [(x0, y0), (x1, y1)]
    for i in range(1, len(changes_zipped) - 1):
        x0 = (datetime.datetime.strptime(changes_zipped[i][0], fmt_event_log) - init_time).total_seconds()
        y0 = y1 = changes_zipped[i][1] * 1_000_000
        x1 = x0 + (datetime.datetime.strptime(changes_zipped[i + 1][0], fmt_event_log) - datetime.datetime.strptime(changes_zipped[i][0], fmt_event_log)).total_seconds()
        changes_lines.append((x0, y0))
        changes_lines.append((x1, y1))

    x0 = (datetime.datetime.strptime(changes_zipped[-1][0], fmt_event_log) - init_time).total_seconds()
    y0 = y1 = changes_zipped[-1][1] * 1_000_000
    x1 = max_x_value
    changes_lines.append((x0, y0))
    changes_lines.append((x1, y1))

    change_time, change_cpacity = zip(*changes_lines)
    plt.plot(change_time, change_cpacity, c='g', label='Bandwidth Capacity')
    print("Done")

    
    loss_y = [np.interp(x, time, tput) for x in loss_deltas]

    # we record network profile number as parent directory name. Get that
    profile_no = os.path.basename(os.path.dirname(res_root))
    bw_list = parse_network_model.get_bw_changes_list(os.path.join('/', 'vagrant', 'network_models', 'dash_if', f'network_config_{profile_no}.json'))
    bw_list = [x * 1_000_000 for x in bw_list] # parser returns value in Mbps. Make it bps

    y1 = []
    y2 = []
    for x in time:
        y1.append(np.interp(x, time, tput))
        if x % 30 == 0:
            x = x - 1
        y2.append(bw_list[(int(x) // 30) % len(bw_list)])

    ax1.fill_between(time, y1, y2, color='orange', label='Unused Bandwidth', alpha=.5)

    plt.scatter(loss_deltas, loss_y, c='r', marker='x', label='Packet Loss')

    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Bandwidth (bps)')
    plt.xlim(left=0)

    ax2 = plt.subplot(211, sharex=ax1)

    time_cwnd = parse_access_log.get_cwnds(os.path.join(res_root, 'nginx_access.log'))

    time, cwnd = zip(*time_cwnd)

    time = [(datetime.datetime.fromtimestamp(t).replace(year=init_time.year, month=init_time.month, day=init_time.day) - init_time).total_seconds() for t in time]

    ax2.scatter(time, cwnd, marker='o')
    ax2.set_ylabel('CWND Size (# MTUs)')

    bin_base = res_root.replace('logs' + os.path.sep, 'doc' + os.path.sep)
    os.makedirs(bin_base, exist_ok=True)
    long_name = bin_base.split('doc' + os.path.sep)[1].replace(os.path.sep, '_')

    fig.savefig(os.path.join(bin_base, 'plot.png'))
    fig.savefig(os.path.join(bin_base, f'{long_name}.pdf'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Plots packet loss over time')
    parser.add_argument('--source', required=True, help='Root of log directory')

    args = parser.parse_args()

    plot_packet_loss(args.source)