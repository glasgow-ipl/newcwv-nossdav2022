# from . import parse_dash_log
# from . import parse_access_log
# from . import parse_kern_log
from datetime import datetime
from matplotlib.text import Text
from numpy.lib.function_base import average
import parse_access_log
import parse_kern_log
import parse_dash_log
from constants import QUALITY_TO_BPS_3S
import numpy as np
import os

import matplotlib.pyplot as plt

def std_deviation(root, links, algs, runs):

    save_path = '/vagrant/img'

    plt.clf()
    fig, ax = plt.subplots(3, sharex=True, sharey=True)

    for i, link in enumerate(links):
        stats = {}
        for alg in algs:
            bandwidth_aggr = []
            for run in runs:
                metrics_path = os.path.join(root, link, f'{run}_{alg}', 'dashjs_metrics.json')
                bandwidth = parse_dash_log.get_throughput_estimates(metrics_path)['precise']
                (_time, values) = zip(*bandwidth.items())
                print(max(values))
                bandwidth_mbps = [v / 1000 for v in values]
                bandwidth_aggr += bandwidth_mbps
            
            print(f"Link: {link}, alg: {alg} (mean: {np.mean(bandwidth_aggr)}, std_dev: {np.std(bandwidth_aggr)})")
            stats[alg] = {'mean': np.mean(bandwidth_aggr), 'std_dev': np.std(bandwidth_aggr)}
            nn = np.percentile(bandwidth_aggr, 99)
            print(stats)
            # print(link, alg)
            # print(sorted(bandwidth_aggr))
            confidence = [v for v in bandwidth_aggr if v < nn]
            stats[alg]['mean_99'] = np.mean(confidence)
            stats[alg]['std_dev_99'] = np.std(confidence)



        ax[i].errorbar([1, 2, 3, 4],
         [
             stats['vreno']['mean'],
              stats['newcwv']['mean'],
              stats['vreno']['mean_99'],
              stats['newcwv']['mean_99']
         ],
        [
            stats['vreno']['std_dev'],
            stats['newcwv']['std_dev'],
            stats['vreno']['std_dev_99'],
            stats['newcwv']['std_dev_99']
        ],
            linestyle='none', marker='^', ecolor='red')
        ax[i].set_title(link)
        plt.xticks([1, 2, 3, 4], ['Reno', 'New CWV', 'Reno_99', 'New CWV_99'])
        plt.ylabel('Std Deviation')

    plt.savefig('/vagrant/img/stats.png')

def plot_cwnd_evolution(root, number):
    plt.clf()
    fig_dist, ax_dist = plt.subplots(1, sharex=True, sharey=True) 
    fig, axs = plt.subplots(4, sharex=True)

    alg_path = os.path.join(root, f'{number}_vreno')
    kernel_log_path = os.path.join(alg_path, 'kern.log')

    res = parse_kern_log.get_cwnds_disconnected(kernel_log_path, video_only=False, disconnect=-1)
    start = end = None
    port_old = res[0][0][2]
    port_idx = 0
    set_label = True
    for i, period in enumerate(res):
        time, size, port = zip(*period)
        if port_old != port[port_idx]:
            #New client connection was established, re-initiate tracing
            start = end = None
            port_old = port
            port_idx = 0
        end = time[0]
        if start and end:
            axs[0].axvspan(start, end, color='red', alpha=0.2, label='Idle Period' if set_label else '_no_label')
            set_label = False
        axs[0].plot(time, size, label='Reno'if i == 0 else '_nolegend_', c='blue')
        start = time[-1]

    estimates = parse_dash_log.get_throughput_estimates(os.path.join(alg_path, 'dashjs_metrics.json'))['precise']
    first_ack = parse_kern_log.get_first_ack(kernel_log_path)
    
    estimates_bar = [((datetime.fromtimestamp(float(x) / 1000) - first_ack).total_seconds(), y / 1000) for x, y in estimates.items()]
    xs, ys = zip(*estimates_bar)
    axs[1].bar(xs, ys)
    import math
    w = 10
    n = math.ceil((max(ys) - min(ys))/w)
    # ax_dist[0].hist(ys, bins=n)
    dist_reno = ys
    # axs[1].scatter([1 for _ in range(len(ys))], ys)

    alg_path = os.path.join(root, f'{number}_newcwv')
    kernel_log_path = os.path.join(alg_path, 'kern.log')

    res = parse_kern_log.get_cwnds_disconnected(kernel_log_path, video_only=False, disconnect=-1)

    start = end = None
    port_old = res[0][0][2]
    port_idx = 0
    set_label = True
    for i, period in enumerate(res):
        if not period:
            continue
        time, size, port = zip(*period)
        if port_old != port[port_idx]:
            #New client connection was established, re-initiate tracing
            start = end = None
            port_old = port
            port_idx = 0
        end = time[0]
        if start and end:
            axs[2].axvspan(start, end, color='red', alpha=0.2, label='Idle Period' if set_label else '_no_label')
            set_label = False
        axs[2].plot(time, size, label='Newcwv'if i == 0 else '_nolegend_', c='blue')
        start = time[-1]

    estimates = parse_dash_log.get_throughput_estimates(os.path.join(alg_path, 'dashjs_metrics.json'))['precise']
    first_ack = parse_kern_log.get_first_ack(kernel_log_path)
    
    estimates_bar = [((datetime.fromtimestamp(float(x) / 1000) - first_ack).total_seconds(), y / 1000) for x, y in estimates.items()]
    xs, ys = zip(*estimates_bar)
    axs[3].bar(xs, ys)
    w = 10
    # n = math.ceil((max(ys) - min(ys))/w)
    max_bw = max(max(dist_reno), max(ys))
    bins = np.arange(0, max_bw + 10, 10)
    print([dist_reno, ys])
    ax_dist.hist([dist_reno, ys], bins=bins, label=['reno', 'newcwv'], density=True)
    ax_dist.legend()
    ax_dist.set_xlabel("Bandwidth")
    ax_dist.set_ylabel("%age distribution")
    # from matplotlib.ticker import PercentFormatter
    # ax_dist.get_yaxis().set_major_formatter(PercentFormatter(.1))
    # y_ticks = ax_dist.get_yticks()
    # print(y_ticks)
    # ax_dist.set_yticks([y* 100 for y in y_ticks])
    # ax_dist.set_yticklabels([float(y) * 100 for y in y_ticks])
    # axs[3].scatter([10 for _ in range(len(ys))], ys)
    # axs[3].hist(ys)

    cwnd_max = max(axs[0].get_ylim()[1], axs[2].get_ylim()[1])
    axs[0].set_ylim(top=cwnd_max)
    axs[2].set_ylim(top=cwnd_max)

    tput_max = max(axs[1].get_ylim()[1], axs[3].get_ylim()[1])
    axs[1].set_ylim(top=tput_max)
    axs[3].set_ylim(top=tput_max)

    axs[0].set_ylabel("CWND\n(# of Packets)")
    axs[2].set_ylabel("CWND\n(# of Packets)")

    axs[1].set_ylabel("Throughput\n(Mbps)")
    axs[3].set_ylabel("Throughput\n(Mbps)")

    # plt.xlim(500, 520)
    # plt.xlim(0, 100)
    # plt.ylim(0, 1500)
    axs[0].legend()
    axs[2].legend()
    plt.gcf().set_size_inches(30, 4)
    plt.xlim(0, plt.xlim()[1])

    plt.xlabel("Time (s)")

    save_path = os.path.join(root, f'cwnd_evolution_{number}.png')
    save_path = os.path.join('/', 'vagrant', 'img', f'cwnd_evolution_{number}.pdf')
    plt.savefig(save_path)

    fig_dist.savefig(os.path.join('/', 'vagrant', 'img', f'bw_dist_{number}.pdf'))
    


def plot_metrics(root, links, algs, numbers):
    metric_names = ['Average Bitrate',
                        'Average Oscillations',
                        'Throughput Precise',
                        'Throughput Safe']
    EXTENSION = 'png'

    plt.clf()
    BAR_WIDTH = .35
    plt.gcf().set_size_inches(3.2, 3)

    metrics = {}

    tmp = {alg: {} for alg in algs}

    bitrates = []
    oscillations = []
    throughput_precise = []
    throughput_safe = []
    thr_precise = []
    thr_safe = []
    for link in links:
        for alg in algs:
            for number in numbers:
                path = os.path.join(root, link, f'{number}_{alg}')

                access_log = os.path.join(path, 'nginx_access.log')
                values = parse_access_log.get_qualities(access_log)
                times, qualities = zip(*values)
                avg_bitrate = parse_access_log.calculate_avg_bitrate(qualities, QUALITY_TO_BPS_3S)
                avg_oscillation = parse_access_log.calculate_avg_oscillation(qualities, QUALITY_TO_BPS_3S)
                bitrates.append(avg_bitrate / 1_000_000)
                oscillations.append(avg_oscillation / 1_000_000)

                metrics_path = os.path.join(path, 'dashjs_metrics.json')
                estimates = parse_dash_log.get_throughput_estimates(metrics_path)
                (_, precise), (_, safe) = estimates.items()
                precise_list = list(precise.values())
                safe_list = list(safe.values())

                ## matching debug format
                precise_list = [el[0] for el in precise_list]
                ######

                precise_avg = np.average(precise_list)
                safe_avg = np.average(safe_list)
                throughput_precise.append(precise_avg)
                throughput_safe.append(safe_avg)
                thr_precise.extend([x / 1000 for x in precise_list]) # Mbps
                thr_safe.extend([x / 1000 for x in safe_list]) # Mbps

            # Out of simulations calculate the average of the averages
            tmp[alg] = {'Average Bitrate': bitrates,
                        'Average Oscillations': oscillations,
                        'Throughput Precise': thr_precise,
                        'Throughput Safe': thr_safe,
                        }

            bitrates = []
            oscillations = []
            throughput_precise = []
            throughput_safe = []
            thr_precise = []
            thr_safe = []

        # Went through all algorithms, record stats    
        metrics[link] = tmp
        tmp = {}

    # print(metrics)

    for link in links:
        for mname in metric_names:
            plt.ylabel(f'{mname} (Mbps)')
            data = []
            for alg in algs:
                data.append(metrics[link][alg][mname])
            plt.boxplot(data)
            plt.xticks(range(1, len(algs) + 1), algs)
            
            if link == 'DSL':
                y_top = 15
                link_cap = 10
            elif link == 'FTTC':
                y_top = 60
                link_cap = 50
            elif link == 'FTTP':
                y_top = 200
                link_cap = 145

            if mname == 'Average Oscillations':
                y_top = 1
            
            if mname == 'Average Bitrate' and link == 'FTTP':
                y_top = 60

            # plt.ylim(top = y_top)
            if mname.startswith('Throughput'):
                plt.axhline(y=link_cap, label='Link Capacity')
                plt.legend()

            # plt.ylim(bottom=0)
            plt.gcf().set_size_inches(3.2, 3)

            mname = mname.replace(' ', '_')
            plt.savefig(f'img/{mname}_{link}.{EXTENSION}', bbox_inches='tight')
            plt.clf()

    # plt.ylabel('Safe Bandwidth (Mbps)')
    # plt.boxplot([metrics['FTTP']['reno']['Throughput Safe'], metrics['FTTP']['vreno']['Throughput Safe'], metrics['FTTP']['newcwv']['Throughput Safe']])
    # plt.xticks(range(1,4), ['Reno', 'vReno', 'New CWV'])
    # plt.ylim(top=160, bottom=0)

    # plt.savefig('thr_safe.png', bbox_inches='tight')
    # plt.clf()

    # plt.ylabel('Measured Bandwidth (Mbps)')
    # plt.boxplot([metrics['FTTP']['reno']['Throughput Precise'], metrics['FTTP']['vreno']['Throughput Precise'], metrics['FTTP']['newcwv']['Throughput Precise']])
    # plt.xticks(range(1,4), ['Reno', 'vReno', 'New CWV'])
    # plt.ylim(top=160, bottom=0)

    # plt.savefig('thr_precise.png', bbox_inches='tight')
    # plt.clf()

    # kernel_log_path = os.path.join(dir_path, 'kern.log')
    # cwnds = parse_kern_log.get_cwnds(kernel_log_path, video_only=False, disconnect=-1)

    return
    index = np.arange(len(metrics))

    link_labels = []

    for i, link in enumerate(metrics):
        reno_br = metrics[link]['vreno']['Bitrate'] / 1_000_000 # Make that in Mb
        newcwv_br = metrics[link]['newcwv']['Bitrate'] / 1_000_000 # Make that Mb
        plt.bar(i, reno_br, BAR_WIDTH, color='green', label='Reno' if i == 0 else '_no_label')
        plt.bar(i+BAR_WIDTH, newcwv_br, BAR_WIDTH, color='blue', label='New CWV' if i == 0 else '_no_label')
        link_labels.append(link)

    plt.xticks(index + BAR_WIDTH / 2, link_labels)
    # plt.xticklabels()
    plt.ylabel("Mbps")
    plt.legend()
    save_path = os.path.join(root, f'average_bitrate.{EXTENSION}')
    plt.savefig(save_path, bbox_inches='tight')

    plt.clf()

    link_labels = []

    for i, link in enumerate(metrics):
        reno_br = metrics[link]['vreno']['Oscillations'] / 1_000_000 # Make that in Mb
        newcwv_br = metrics[link]['newcwv']['Oscillations'] / 1_000_000 # Make that Mb
        plt.bar(i, reno_br, BAR_WIDTH, color='green', label='Reno' if i == 0 else '_no_label')
        plt.bar(i+BAR_WIDTH, newcwv_br, BAR_WIDTH, color='blue', label='New CWV' if i == 0 else '_no_label')
        link_labels.append(link)

    plt.xticks(index + BAR_WIDTH / 2, link_labels)
    # plt.xticklabels()
    plt.ylabel("Mbps")
    plt.legend()
    save_path = os.path.join(root, f'average_oscillations.{EXTENSION}')
    plt.savefig(save_path, bbox_inches='tight')

    plt.clf()
    link_labels = []

    for i, link in enumerate(metrics):
        reno_br = metrics[link]['vreno']['Throughput Precise'] / 1_000 # Make that in Mb
        newcwv_br = metrics[link]['newcwv']['Throughput Precise'] / 1_000 # Make that Mb
        plt.bar(i, reno_br, BAR_WIDTH, color='green', label='Reno' if i == 0 else '_no_label')
        plt.bar(i+BAR_WIDTH, newcwv_br, BAR_WIDTH, color='blue', label='New CWV' if i == 0 else '_no_label')
        link_labels.append(link)

    plt.xticks(index + BAR_WIDTH / 2, link_labels)
    # plt.xticklabels()
    plt.ylabel("Mbps")
    plt.legend()
    save_path = os.path.join(root, f'calculated_throughput.{EXTENSION}')
    plt.savefig(save_path, bbox_inches='tight')

    plt.clf()
    link_labels = []

    for i, link in enumerate(metrics):
        reno_br = metrics[link]['vreno']['Throughput Safe'] / 1_000 # Make that in Mb
        newcwv_br = metrics[link]['newcwv']['Throughput Safe'] / 1_000 # Make that Mb
        plt.bar(i, reno_br, BAR_WIDTH, color='green', label='Reno' if i == 0 else '_no_label')
        plt.bar(i+BAR_WIDTH, newcwv_br, BAR_WIDTH, color='blue', label='New CWV' if i == 0 else '_no_label')
        link_labels.append(link)

    plt.xticks(index + BAR_WIDTH / 2, link_labels)
    # plt.xticklabels()
    plt.ylabel("Mbps")
    plt.legend()
    save_path = os.path.join(root, f'calculated_safe_throughput.{EXTENSION}')
    plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    # plot_metrics('/vagrant/logs/newcwv/test2', links=['FTTP'], algs=['newcwv', 'vreno'], numbers=range(1, 11))
    # for i in range(3, 6):
    #     plot_cwnd_evolution('/vagrant/logs/tmp/curtis/DSL', i)
    # plot_cwnd_evolution('/vagrant/logs/newcwv/FTTP', 1)
    std_deviation('/vagrant/logs/newcwv/test2/', ['FTTP'], ['newcwv', 'vreno'], range(1, 11))
