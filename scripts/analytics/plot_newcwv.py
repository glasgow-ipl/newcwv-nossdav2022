# from . import parse_dash_log
# from . import parse_access_log
# from . import parse_kern_log
from numpy.lib.function_base import average
import parse_access_log
import parse_kern_log
import parse_dash_log
from constants import QUALITY_TO_BPS_3S
import numpy as np
import os

import matplotlib.pyplot as plt

def plot_cwnd_evolution(root, number):
    plt.clf()
    fig, axs = plt.subplots(2, sharex=True, sharey=True)

    alg_path = os.path.join(root, f'{number}_vreno')
    kernel_log_path = os.path.join(alg_path, 'kern.log')

    res = parse_kern_log.get_cwnds_disconnected(kernel_log_path, video_only=False, disconnect=-1)
    
    start = end = None
    set_label = True
    for i, period in enumerate(res):
        time, size = zip(*period)
        end = time[0]
        if start and end:
            axs[0].axvspan(start, end, color='red', alpha=0.2, label='Idle Period' if set_label else '_no_label')
            set_label = False
        axs[0].plot(time, size, label='Reno'if i == 0 else '_nolegend_', c='blue')
        start = time[-1]


    alg_path = os.path.join(root, f'{number}_newcwv')
    kernel_log_path = os.path.join(alg_path, 'kern.log')

    res = parse_kern_log.get_cwnds_disconnected(kernel_log_path, video_only=False, disconnect=-1)

    start = end = None
    set_label = True
    for i, period in enumerate(res):
        time, size = zip(*period)
        end = time[0]
        # print(end)
        if start and end:
            axs[1].axvspan(start, end, color='red', alpha=0.2, label='Idle Period' if set_label else '_no_label')
            set_label = False
        axs[1].plot(time, size, label='Newcwv'if i == 0 else '_nolegend_', c='blue')
        start = time[-1]

    # plt.xlim(left=250, right=300)
    save_path = os.path.join(root, f'cwnd_evolution_{number}.png')
    plt.savefig(save_path)


def plot_metrics(root, links, algs, numbers):
    EXTENSION = 'pdf'

    plt.clf()
    BAR_WIDTH = .35
    plt.gcf().set_size_inches(3.2, 3)

    metrics = {}

    tmp = {alg: {} for alg in algs}

    bitrates = []
    oscillations = []
    throughput_precise = []
    throughput_safe = []
    for link in links:
        for alg in algs:
            for number in numbers:
                path = os.path.join(root, link, f'{number}_{alg}')

                access_log = os.path.join(path, 'nginx_access.log')

                values = parse_access_log.get_qualities(access_log)
                times, qualities = zip(*values)
                avg_bitrate = parse_access_log.calculate_avg_bitrate(qualities, QUALITY_TO_BPS_3S)
                avg_oscillation = parse_access_log.calculate_avg_oscillation(qualities, QUALITY_TO_BPS_3S)
                bitrates.append(avg_bitrate)
                oscillations.append(avg_oscillation)

                metrics_path = os.path.join(path, 'dashjs_metrics.json')
                estimates = parse_dash_log.get_throughput_estimates(metrics_path)
                (_, precise), (_, safe) = estimates.items()
                precise_list = list(precise.values())
                safe_list = list(safe.values())
                precise_avg = np.average(precise_list)
                safe_avg = np.average(safe_list)
                throughput_precise.append(precise_avg)
                throughput_safe.append(safe_avg)

            # Out of simulations calculate the average of the averages
            tmp[alg] = {'Bitrate': np.average(bitrates),
                        'Oscillations': np.average(oscillations),
                        'Throughput Precise': np.average(throughput_precise),
                        'Throughput Safe': np.average(throughput_safe)
                        }
            bitrates = []
            oscillations = []
            throughput_precise = []
            throughput_safe = []

        # Went through all algorithms, record stats    
        metrics[link] = tmp
        tmp = {}

    print(metrics)
    # kernel_log_path = os.path.join(dir_path, 'kern.log')
    # cwnds = parse_kern_log.get_cwnds(kernel_log_path, video_only=False, disconnect=-1)

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
    plot_metrics('/vagrant/logs/tmp/curtis', links=['DSL', 'FTTC'], algs=['vreno', 'newcwv'], numbers=range(3, 6))
    # for i in range(3, 6):
    #     plot_cwnd_evolution('/vagrant/logs/tmp/curtis/DSL', i)
