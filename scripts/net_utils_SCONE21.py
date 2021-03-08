import sys
import csv
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
import numpy as np
import os
import argparse
import json

import functools
import math

kbps = [1410237, 3720740, 6961267, 11097137]

quality_to_kbps_3s = {360: 1368193, 480: 3619359, 720: 6747721, 1080: 10660219}

def count_oscillations(values): # returns the number of oscillations in the value list (cwnd)
    changes = 0
    if(len(values) < 2):
        return 0
    direction = int(values[1] > values[0]) # 1 - increasing, 0 - decreasing
     
    for idx in range(1, len(values) - 1):
        if direction:
            if values[idx][1] > values[idx + 1][1]:
                direction = not direction
                changes += 1
        else:
            if values[idx][1] < values[idx + 1][1]:
                direction = not direction
                changes += 1
        
    return changes


def gen_plot(plot_info, root='.'):
    cwnd_info = plot_info['cwnds']
    print(sorted(x[1] for x in cwnd_info))
    cwnd_info = np.array(cwnd_info)#, dtype=np.dtype('float64,int'))

    # print(cwnd_info)

    quality_info = plot_info['qualities']
    quality_info = np.array(quality_info)

    time = cwnd_info[:,0]
    cwnd = cwnd_info[:,1]
    cwnd = [x * 1500 * 8  * 1000 / 70 / 1_000_000 for x in cwnd]

    quality = quality_info[:,1]
    fig, axs = plt.subplots(2)

    # Axis setup
    for ax in axs:
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))

        # For the minor ticks, use no labels; default NullFormatter.
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.set_xlim(right=max(time) + 5)

    # axs[0].set_yticks(np.arange(0, 55, 10))
    axs[1].set_yticks([360, 480, 720, 1080])
    axs[1].set_ylim(bottom=0, top=1200)

    # plotting
    # axs[0].plot(time, cwnd)
    axs[1].scatter(time, quality)

    colors = iter(mcolors.TABLEAU_COLORS.keys())
    colors.__next__() # discard blue from the set

    col_values = []

    bw_changes = plot_info['bw_changes']
    for change in bw_changes:
        col = colors.__next__()
        for ax in axs:
            ax.axvline(x=change[0], color=col, linewidth=3, label='bw changed to: %sMbps' % change[1])

    for video_quality in kbps:
        video_quality /= 1_000_000
        col = colors.__next__()
        col_values.append(col)
        axs[0].axhline(y=video_quality, color=col, linewidth=2)

    quality_col = {360: col_values[0], 480: col_values[1], 720: col_values[2], 1080: col_values[3]}

    y_new_cwnd = np.array([kbps[1] / 1_000_000, kbps[2] / 1_000_000, kbps[2] / 1_000_000, kbps[1] / 1_000_000, kbps[1] / 1_000_000, kbps[2] / 1_000_000, kbps[2] / 1_000_000])
    x_new_cwnd = np.array([0, 2, 84, 85, 105, 108, 300])
    axs[0].plot(x_new_cwnd, y_new_cwnd, c='orange', linewidth=4)

    # labels configuration
    axs[0].set(ylabel='Throughput (Mbps)')
    axs[1].set(xlabel='Time (s)')
    axs[1].set(ylabel='Requested Bitrate')

    fig.set_size_inches((35, 5))
    for ax in axs:
        ax.tick_params(labelrotation=45)
    
    axs[1].scatter(time, quality, c=np.array([quality_col[q] for q in quality]))

    fig.legend()

    plt.tight_layout()

    for ext in ['fig.png', 'fig.pdf']:
        save_path = os.path.join(root, ext)
        plt.savefig(save_path)


def parse_logs(log_root):
    """[summary]

    Args:
        log_root ([type]): [description]

    Returns:
        [type]: [description]
    """
    plot_info = {}

    access_log_path = os.path.join(log_root, 'nginx_access.log')

    nginx_info = parse_nginx_log(access_log_path)
    # plot_info['cwnds'] = cwnds
    # plot_info['init_time'] = init_time
    plot_info.update(nginx_info)

    init_time = plot_info['init_time']

    event_log_path = os.path.join(log_root, 'events.log')
    bw_changes = get_bw_changes(event_log_path, init_time) 
    plot_info['bw_changes'] = bw_changes

    return plot_info
    

def get_bw_changes(event_log_path, init_time):
    bw_change_times = []

    with open(event_log_path) as f:
        for line in f:
            if 'changing BW' in line:
                string_tokens = line.split()
                change_time = datetime.datetime.strptime(string_tokens[-1], "%y-%m-%d-%H:%M:%S:%f")
                change_bw = float(string_tokens[-2].strip())
                change_time_rel = (change_time - init_time).total_seconds()
                bw_change_times.append((change_time_rel, change_bw))

    return bw_change_times


def parse_nginx_log(access_log_path):
    cwnd_time = []
    quality_time = []
    with open(access_log_path) as f:
        reader = csv.reader(f)
        # find the first video segment requested and treat it as start of time
        while True:
            rec = reader.__next__()
            if 'init' in rec[2]:
                time_init = float(rec[1])
                time_init = datetime.datetime.utcfromtimestamp(time_init)
                ms_delta = (time_init - time_init).total_seconds()
                cwnd = rec[6].strip()
                cwnd = int(cwnd[1:-1])
                cwnd_time.append((ms_delta, cwnd))
                quality = int(rec[2].split('data/')[1].split('/', 1)[0])
                quality_time.append((ms_delta, quality))
                break

        for line in reader:
            current_time = float(line[1])
            current_time = datetime.datetime.utcfromtimestamp(current_time)
            ms_delta = (current_time - time_init).total_seconds()
            cwnd = line[6].strip()
            cwnd = int(cwnd[1:-1]) # Remove the "" from the begining and the end of the cwnd value
            cwnd_time.append((ms_delta, cwnd))

            quality = int(line[2].split('data/')[1].split('/',1)[0])
            quality_time.append((ms_delta, quality))

    res = {}
    res['cwnds'] = cwnd_time
    res['init_time'] = time_init
    res['qualities'] = quality_time

    return res


def parse_dash_metrics(json_dump):
    dash_metrics = {}
    with open(json_dump) as f:
        dash_metrics = json.load(f)

    print(dash_metrics.keys())
    print(dash_metrics['bufferLevel'])
    print(dash_metrics['currentTime'])


def parse_log_dir(path):
    """
    Parses the given log directory. Generates plots from the data and stores them in /vagrant/doc/DIR
     where DIR is the same as the top level directory

    Args:
        path ([str]): A path like string pointing to the root log directory
    """
    print(f'parsing {path}')
    dir_name = os.path.split(path)[-1]
    doc_root = os.path.join('/', 'vagrant', 'doc', dir_name)
    if os.path.exists(doc_root):
        print(f'Warning: {doc_root} already exists, potentially overwriting data')
    else:
        os.mkdir(doc_root)
    plot_info = parse_logs(path)
    gen_plot(plot_info, root=doc_root)
    print(f'Plots saved to {doc_root}')

def calc_avg_bitrate_dir(dir_name):
    avg_bitrates_bbr = []
    avg_bitrates_cubic = []
    for root, dirs, files in os.walk(dir_name):
        # print(root, dirs, files)
        if 'nginx_access.log' in files:
            try:
                nginx_log_path = os.path.join(root, 'nginx_access.log')
                avg_bitrate = calc_avg_bitrate(nginx_log_path)
                if 'bbr' in root:
                    avg_bitrates_bbr.append(avg_bitrate)
                elif 'cubic' in root:
                    avg_bitrates_cubic.append(avg_bitrates_cubic)
            except:
                pass

    print(avg_bitrates_bbr)
    print(avg_bitrates_cubic)

def calc_avg_bitrate(fname):
    print(f'working on {fname}')
    parsed = parse_nginx_log(fname)
    qualities = np.array(parsed['qualities'])
    qualities = qualities[:,1]
    q_kbps = [quality_to_kbps_3s[q] for q in qualities]

    # print(q_kbps)

    print("average bitrate: %f" % np.average(q_kbps))

    avg_osc = functools.reduce(lambda i, j: abs(i - j), q_kbps) / (len(kbps) - 1)
    print("Average oscillation: %f" % avg_osc)

    return np.average(q_kbps)


if __name__ == '__main__':

    # if len(sys.argv) == 1: # script was run with no arguments
        # parse_dash_metrics('/vagrant/logs/10-12-1307/dashjs_metrics.json')
        # plot_info = parse_logs('/vagrant/logs/10-12-1307')
        # gen_plot(plot_info)
        # sys.exit(1)

    calc_avg_bitrate_dir('/vagrant/logs')


    sys.exit()

    parser = argparse.ArgumentParser(description='Collection of functions that handle graph plotting')
    parser.add_argument('--source', help='single log file to be parsed')
    parser.add_argument('--all', action='store_true', help='Creates plots for all data rooted at /vagrant/logs')

    args = parser.parse_args()

    if args.all:
        print("all arg")
        root = os.path.join('/', 'vagrant', 'logs')
        deps = ['nginx_access.log', 'events.log']
        for path, dirs, files in os.walk(root):
            print (path, dirs, files)
            if all(x in files for x in deps):
                parse_log_dir(path)
    elif args.source:
        parse_log_dir(args.source)

