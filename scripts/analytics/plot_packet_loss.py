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
    event_path = os.path.join(res_root, 'events.log')
    
    fig = plt.gcf()
    fig.set_size_inches((35, 5))

    changes_zipped = parse_event_log.get_bw_changes(event_path)

    server_pcap_path = os.path.join(res_root, 'server.pcap')
    loss_times = detect_packet_loss.get_lost_packets(server_pcap_path)

    fmt_pcap = '%H:%M:%S.%f'

    fmt_event_log = '%H:%M:%S:%f'
    init_time_ts = parse_event_log.get_initial_ts(event_path)
    init_time = datetime.datetime.strptime(init_time_ts, fmt_event_log)

    loss_deltas = [(datetime.datetime.strptime(x, fmt_pcap) - init_time).total_seconds() for x in loss_times]


    tput = verify_throughput.calculate_throughput(server_pcap_path, init_time=init_time)

    time, tput = zip(*tput.items())
    plt.plot(time, tput, c='b', label='Throughput')

    max_x_value = max(time)
    x0 = (datetime.datetime.strptime(changes_zipped[0][0], fmt_event_log) - init_time).total_seconds()
    y0 = y1 = changes_zipped[0][1] * 1_000_000
    x1 = (datetime.datetime.strptime(changes_zipped[1][0], fmt_event_log) - datetime.datetime.strptime(changes_zipped[0][0], fmt_event_log)).total_seconds()
    changes_lines = [(x0, y0), (x1, y1)]
    for i in range(1, len(changes_zipped) - 1):
        x0 = (datetime.datetime.strptime(changes_zipped[i][0], fmt_event_log) - init_time).total_seconds()
        y0 = y1 = changes_zipped[0][1] * 1_000_000
        x1 = (datetime.datetime.strptime(changes_zipped[i + 1][0], fmt_event_log) - datetime.datetime.strptime(changes_zipped[i][0], fmt_event_log)).total_seconds()
        changes_lines.append((x0, y0))
        changes_lines.append((x1, y1))

    x0 = (datetime.datetime.strptime(changes_zipped[-1][0], fmt_event_log) - init_time).total_seconds()
    y0 = y1 = changes_zipped[-1][1] * 1_000_000
    x1 = max_x_value
    changes_lines.append((x0, y0))
    changes_lines.append((x1, y1))

    x_vals, y_vals = zip(*changes_lines)
    plt.plot(x_vals, y_vals, c='g', label='Bandwidth Capacity')

    loss_y = [np.interp(x, time, tput) for x in loss_deltas]

    plt.scatter(loss_deltas, loss_y, c='r', marker='x', label='Packet Loss')

    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Bandwidth (bps)')

    fig.savefig('plot.png')
    fig.savefig('plot.pdf')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Plots packet loss over time')
    parser.add_argument('--source', required=True, help='Root of log directory')

    args = parser.parse_args()

    plot_packet_loss(args.source)