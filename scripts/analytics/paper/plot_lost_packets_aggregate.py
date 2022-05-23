import argparse
import matplotlib.pyplot as plt

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


def plot_dropped_packets(algs, clients):
    drop_info = {a : {} for a in algs}
    for c in clients: 
        with open(f'/vagrant/doc/paper/figures/parsed_data/clients/{c}/parsed_data.json') as f:
            tmp = json.load(f)['dropped_packets']['DSL']
            for a in algs:
                drop_info[a][c] = tmp[a]

    newcwv = drop_info['newcwv']
    reno = drop_info['vreno']

    clients_newcwv = {int(client): [v['lost'] / v['all'] for v in runs.values()] for client, runs in newcwv.items()}
    clients_reno = {int(client): [v['lost'] / v['all'] for v in runs.values()] for client, runs in reno.items()}

    fig, axs = plt.subplots(1, 2)

    plot_items = [clients_reno, clients_newcwv]
    max_y = 0
    min_y = 1
    for i, plot_item in enumerate(plot_items):
        runs, loss_data = zip(*plot_item.items())
        axs[i].boxplot(loss_data, labels=runs)
        max_y = max(max_y, axs[i].get_ylim()[1])
        min_y = min(min_y, axs[i].get_ylim()[0])

    for ax in axs:
        ax.set_ylim(top=max_y, bottom=0)
        ax.get_yaxis().set_major_formatter(PercentFormatter(1))
        ax.set_xlabel("Number of Clients")

    axs[0].set_ylabel("Percentage of Lost Packets")
    axs[0].set_title("CWV")
    axs[1].set_title("New CWV")

    # axs[0].set_yticks([0, 0.01, 0.02, 0.03, 0.04])
    axs[1].set_yticks([])

    save_path = 'doc/paper/figures/lost_packets_dynamic.pdf'
    print(f"Saving {save_path}")
    fig.set_size_inches(8, 3)
    fig.savefig(save_path, bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--algs', nargs='+', help='Algorithm names to consider', required=True)
    parser.add_argument('--clients_combined', nargs='+', help="List of all client combinations", required=True)

    args = parser.parse_args()

    plot_dropped_packets(algs=args.algs, clients=args.clients_combined)



