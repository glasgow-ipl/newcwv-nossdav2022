import os
import matplotlib.pyplot as plt
import datetime
import numpy as np
import sys
import argparse

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import detect_packet_loss
import verify_throughput
import parse_event_log


def plot_packet_loss(res_root):
    fmt_pcap = '%H:%M:%S.%f'

    fmt_event_log = '%H:%M:%S:%f'

    event_path = os.path.join(res_root, 'events.log')
    
    fig = plt.gcf()
    fig.set_size_inches((35, 5))

    changes_zipped = parse_event_log.get_bw_changes(event_path)

    server_pcap_path = os.path.join(res_root, 'server.pcap')
    print('Analysing lost packets')
    loss_times = detect_packet_loss.get_lost_packets(server_pcap_path)
    init_time_ts = parse_event_log.get_initial_ts(event_path)
    init_time = datetime.datetime.strptime(init_time_ts, fmt_event_log)

    loss_deltas = [(datetime.datetime.strptime(x, fmt_pcap) - init_time).total_seconds() for x in loss_times]
    print('Done')

    print('Calculating Tput')
    tput = verify_throughput.calculate_throughput(server_pcap_path, init_time=init_time)
    print('Done')

    time, tput = zip(*tput.items())
    plt.plot(time, tput, c='b', label='Throughput')

    print('Getting Link Change info')
    max_x_value = max(time)
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

    for i in range(0, len(changes_lines), 2):
        p1 = changes_lines[i]
        p2 = changes_lines[i + 1]
        x, y = zip(*[p1, p2])
        plt.plot(x, y, c='g', label='Bandwidth Capacity' if i==0 else '_no_legend_')
    print('Done')

    
    loss_y = [np.interp(x, time, tput) for x in loss_deltas]

    plt.scatter(loss_deltas, loss_y, c='r', marker='x', label='Packet Loss')

    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Bandwidth (bps)')
    plt.xlim(left=0)

    bin_base = res_root.replace('/logs/', '/doc/')
    os.makedirs(bin_base, exist_ok=True)

    fig.savefig(os.path.join(bin_base, 'plot.png'))
    fig.savefig(os.path.join(bin_base, 'plot.pdf'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Plots packet loss over time')
    parser.add_argument('--source', required=True, help='Root of log directory')

    args = parser.parse_args()

    plot_packet_loss(args.source)