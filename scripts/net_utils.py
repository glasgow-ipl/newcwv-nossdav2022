import sys
import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
import numpy as np
import os
import argparse

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


def gen_plot(plot_info):
    cwnd_info = plot_info['cwnds']
    cwnd_info = np.array(cwnd_info)#, dtype=np.dtype('float64,int'))

    quality_info = plot_info['qualities']
    quality_info = np.array(quality_info)

    time = cwnd_info[:,0]
    cwnd = cwnd_info[:,1]

    quality = quality_info[:,1]

    fig, axs = plt.subplots(2)

    # Axis setup
    for ax in axs:
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))

        # For the minor ticks, use no labels; default NullFormatter.
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.set_xlim(right=max(time) + 5)

    axs[0].set_yticks(np.arange(0, 500, 50))
    axs[1].set_yticks([360, 480, 720, 1080])
    axs[1].set_ylim(bottom=0, top=1200)

    # plotting
    axs[0].plot(time, cwnd)
    axs[1].scatter(time, quality)

    colors = iter(mcolors.TABLEAU_COLORS.keys())
    colors.__next__() # discard blue from the set

    bw_changes = plot_info['bw_changes']
    for change in bw_changes:
        col = colors.__next__()
        for ax in axs:
            ax.axvline(x=change[0], color=col, linewidth=3, label='bw changed to: %sMbps' % change[1])

    # labels configuration
    axs[0].set(ylabel='Cwnd (MSS packets)')
    axs[1].set(xlabel='Time (s)')
    axs[1].set(ylabel='Requested Bitrate')

    fig.set_size_inches((35, 5))
    for ax in axs:
        ax.tick_params(labelrotation=45)
    

    fig.legend()

    plt.tight_layout()
    plt.savefig('fig2.png')


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

if __name__ == '__main__':

    if len(sys.argv) == 1: # script was run with no arguments
        plot_info = parse_logs('/vagrant/logs/10-12-1307')
        gen_plot(plot_info)

    parser = argparse.ArgumentParser(description='Collection of functions that handle graph plotting')
    parser.add_argument('--source', help='single log file to be parsed')
    parser.add_argument('-all', help='Root directory for logged data for batch plotting')

    args = parser.parse_args()