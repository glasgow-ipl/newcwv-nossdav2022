from net_utils import parse_nginx_log, count_oscillations_cwnd, count_oscillations_bitrates, get_bw_changes
import os
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

quality_to_bw = {360: 1410237, 480: 3720740, 720: 6961267, 1080: 11097137}

def cc_study():

    log_path = os.path.join('/', 'vagrant', 'logs', '2nd_year_report', 'cc_study')

    stats = {
            'cubic': {'bitrate_osc': [], 'cwnd_osc': [], 'avg_bitrate': []},
            'bbr': {'bitrate_osc': [], 'cwnd_osc': [], 'avg_bitrate': []},
            'reno': {'bitrate_osc': [], 'cwnd_osc': [], 'avg_bitrate': []}
        }

    quality_to_num = {360: 1, 480: 2, 720: 3, 1080: 4}
    alg_col = {'cubic': 'g', 'reno': 'b', 'bbr': 'r'}

    # plt.vlines(60, 0, 5, colors='y')
    # plt.axvline(60)
    fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)

    (ax0, ax1, ax2) = ax

    alg_ax = {'cubic': ax0, 'reno': ax1, 'bbr': ax2}

    for root, dirs, files in os.walk(log_path):
        if 'nginx_access.log' in files:
            print(root)
            
            nginx_log_path = os.path.join(root, 'nginx_access.log')
            parsed_log = parse_nginx_log(nginx_log_path)

            cwnd_osc = count_oscillations_cwnd(parsed_log['cwnds'])
            bitrate_osc = count_oscillations_bitrates(parsed_log['qualities'])
            print(parsed_log['init_time'])

            cong_name = root.split('_')[-1]

            time, quality = zip(*parsed_log['qualities'])
            quality = [quality_to_num[x] for x in quality]
            alg_ax[cong_name].scatter(time, quality, c=alg_col[cong_name], label=cong_name, alpha=0.07)

            events_path = os.path.join(root, 'events.log')
            bw_changes = get_bw_changes(events_path, parsed_log['init_time'])

            for i, change in enumerate(bw_changes):
                # alg_ax[cong_name].axvline(x=75 if i % 2 else 145, label=f'BW changed to {change[1]} Mbps', linestyle='-' if i % 2 else '--')
                alg_ax[cong_name].axvline(change[0], label=f'BW changed to {change[1]} Mbps', linestyle='-' if i % 2 else '--')

            stats[cong_name]['bitrate_osc'].append(bitrate_osc)
            stats[cong_name]['cwnd_osc'].append(cwnd_osc)

            chosen_bitrates = [quality_to_bw[x[1]] for x in parsed_log['qualities']]

            stats[cong_name]['avg_bitrate'].append(np.mean(chosen_bitrates))

    handles_all = []
    labels_all = []
    for _, v in alg_ax.items():
        handles, labels = legend_without_duplicate_labels(v)
        for i, lab in enumerate(labels):
            if lab not in labels_all:
                handles_all.append(handles[i])
                labels_all.append(labels[i]) 
        # handles_all.extend(handles)
        # labels_all.extend(labels)
        # print(handels, labels)
        # return
    print(handles_all, labels_all)
    # unique = [(h, l) for i, (h, l) in enumerate(zip(handles_all, labels_all)) if l not in labels[:i]]
    # for i, lab in enumerate(labels_all):
    # unique_handles = []
    # unique_labels = []
    # for i, label in enumerate(labels_all):
    #     if label not in unique_labels:
    #         unique_labels.append()


    fig.legend(handles_all, labels_all, bbox_to_anchor=(.265, 0.01))

    save_path = os.path.join('/', 'vagrant', 'logs', '2nd_year_report', 'CC_algorithms_bitrate_choices.pdf')
    plt.setp((ax0, ax1, ax2), yticks=[1, 2, 3, 4], yticklabels=['360p', '480p', '720p', '1080p'],
                                 xticks=np.arange(0, 700, 20),
                                  xlim=(0,700), ylim=(0, 5),
                                  xlabel='Time (s)', ylabel='Representation Set')

    plt.tight_layout()
    print( plt.gcf().get_size_inches())
    plt.gcf().set_size_inches(15, plt.gcf().get_size_inches()[1])
    plt.savefig(save_path, bbox_inches='tight')
    # plt.legend()

    print(stats)

    for key in stats:
        # stats[key]['avg_bitrate'] =
        print(key, np.mean(stats[key]['cwnd_osc']), np.mean(stats[key]['bitrate_osc']), np.mean(stats[key]['avg_bitrate']) / 1_000)
        stats[key]['cwnd_osc']  = np.mean(stats[key]['cwnd_osc'])
        stats[key]['bitrate_osc'] = np.mean(stats[key]['bitrate_osc'])
        stats[key]['avg_bitrate'] = np.mean(stats[key]['avg_bitrate']) / 1_000

    sorted_stats = sorted(stats.items())
    table_data = [[k, *v.values()] for k, v in sorted_stats]
    table_headers = ['Congestion Algorithm', *sorted_stats[0][1].keys()]

    table = tabulate(table_data, table_headers, tablefmt='latex')

    print(table)

    # print(np.var(stats['bbr']['cwnd_osc']))
    # parse_nginx_log()

def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    # ax.legend(*zip(*unique))
    return zip(*unique)

def throughput_changing_bw():
    log_path = os.path.join('/', 'vagrant', 'logs', '2nd_year_report', 'throughput_changing_bw')

    bws = {}

    for root, dirs, files in os.walk(log_path):
        if 'events.log' in files:
            log_path = os.path.join(root, 'events.log')
            bw = _get_bw(log_path)
            print(bw)
            nginx_log_path = os.path.join(root, 'nginx_access.log')
            parsed_log = parse_nginx_log(nginx_log_path)
            bitrate_oscillations = count_oscillations_bitrates(parsed_log['qualities'])
            _, qualities = zip(*parsed_log['qualities'])
            qualities_kbps = [quality_to_bw[x] for x in qualities]
            mean_bitrate = np.mean(qualities_kbps)
            bws[float(bw)] = {'mean_bitrate': mean_bitrate / 1_000, 'oscillations_count': bitrate_oscillations,
             'min_bitrate': np.min(qualities_kbps) / 1_000, 'max_bitrate': np.max(qualities_kbps) / 1_000}
    
    sorted_bws = sorted(bws.items())
    print(sorted_bws)
    table_data = [[k, *v.values()] for k, v in sorted_bws]
    table_headers = ['Bandwidth Cap', *sorted_bws[0][1].keys()]

    table = tabulate(table_data, table_headers, tablefmt='latex')

    oscillations_for_bw = [(x[0], x[1]['oscillations_count']) for x in sorted_bws]
    bws, oscillations = zip(*oscillations_for_bw)
    print(oscillations)

    print(bws)

    plt.barh(np.arange(len(bws)), oscillations)
    plt.yticks(np.arange(len(bws)), bws)
    plt.ylim((1, len(bws)))
    plt.xlabel('Number of Oscillations')
    plt.ylabel('Bandwidth Cap')
    save_path = os.path.join('/', 'vagrant', 'logs', '2nd_year_report', 'oscillation_distribution_h.pdf')
    # print(save_path)
    plt.savefig(save_path)

    print(plt.gcf().get_size_inches())
    plt.gcf().set_size_inches(6.4, 20)
    plt.savefig(save_path, bbox_inches='tight')

    print(oscillations_for_bw)

    # print(table)

def _get_bw(log_path):
    with open(log_path) as f:
        for line in f:
            if line.startswith('changing BW'):
                bw = line.split()[2]
                return bw


throughput_changing_bw()
# cc_study()