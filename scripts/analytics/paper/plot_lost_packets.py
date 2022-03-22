import matplotlib.pyplot as plt
import argparse

plt.rc('font',**{'family':'Times New Roman', 'size': 20})
plt.rc('axes', axisbelow=True)
plt.rcParams['pdf.fonttype'] = 42

import os
import subprocess
import datetime
import glob

import plot_transmission_acks
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np

from count_lost_packets import count_all_packets

import json

def split_runs(packet_list):

    runs = []
    run = []
    for i in range(len(packet_list) - 1):
        run.append(packet_list[i])
        if float(packet_list[i][0]) > float(packet_list[i+1][0]):
            runs.append(run)
            run = []

    runs[-1].append(packet_list[-1])

    return runs


def plot_lost_packets(root, extension):
    server_packets = count_all_packets(root)

    # 102, 105 for 1_newcwv and 1_reno
    PLOT_MIN_TIME = 103
    PLOT_MAX_TIME = 105

    transferred_packets = []
    lost_packets = []
    for seq_id, (timestamps, occurence) in server_packets.items():
        seq = int(seq_id.split(':')[-1][:-1])
        for lost_ts in timestamps[:occurence]:
            if PLOT_MIN_TIME <= lost_ts <= PLOT_MAX_TIME:
                lost_packets.append((lost_ts, seq))
        for transferred_ts in timestamps[occurence:]:
            if PLOT_MIN_TIME <= transferred_ts <= PLOT_MAX_TIME:
                transferred_packets.append((transferred_ts, seq))
    
    # transfrerred_filtered = [(transfered)]
    relative_ts, relative_seq = min(min(transferred_packets), min(lost_packets))
    transferred_packets = [(t - relative_ts, s - relative_seq) for (t, s) in transferred_packets]
    lost_packets = [(t - relative_ts, s - relative_seq) for (t, s) in lost_packets]


    transferred_tss, transferred_seqs = zip(*transferred_packets)
    lost_tss, lost_seqs = zip(*lost_packets)


    plt.scatter(transferred_tss, transferred_seqs, c='green', alpha=0.2, label='Received', marker='.')
    plt.scatter(lost_tss, lost_seqs, c='red', label='Lost', marker='X')

    # plt.gcf().set_size_inches(12, 4)
    plt.xlim(-0.01, 0.25)
    plt.ylim(bottom=-10000, top=300_000)
    # plt.xlim(103.5, 104.5)
    # plt.ylim(bottom=66_500_000, top=68_000_000)
    plt.xlabel('Time since restart (s)')
    plt.ylabel('TCP Sequence number')
    plt.legend(loc='upper left')

    alg = os.path.basename(root).split('_')[1]

    plt.gcf().set_size_inches(6, 3)
    fig_name = f'/vagrant/doc/paper/figures/lost_packets_{alg}.{extension}'
    print(f"saving {fig_name}")
    plt.savefig(fig_name, bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', help="root directory to plot lost packets from (run root)", required=True)
    parser.add_argument('--extension', default='pdf')
    args = parser.parse_args()


    plot_lost_packets(args.root, args.extension)
