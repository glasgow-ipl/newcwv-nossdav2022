import matplotlib.pyplot as plt
import os
import numpy as np
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import parse_access_log
from constants import QUALITY_TO_BPS_3S_IETF
import parse_dash_log


def plot_data(root, links, algs, numbers, extension = 'png'):
    metric_names = ['Average Bitrate',
                        'Average Oscillations',
                        'Throughput Precise',
                        'Throughput Safe']

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
                avg_bitrate = parse_access_log.calculate_avg_bitrate(qualities, QUALITY_TO_BPS_3S_IETF)
                avg_oscillation = parse_access_log.calculate_avg_oscillation(qualities, QUALITY_TO_BPS_3S_IETF)
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
                # y_top = 15
                link_cap = 10
            elif link == 'FTTC':
                # y_top = 60
                link_cap = 50
            elif link == 'FTTP':
                # y_top = 200
                link_cap = 145

            # if mname == 'Average Oscillations':
            #     y_top = 1
            
            # if mname == 'Average Bitrate' and link == 'FTTP':
            #     y_top = 60

            print(mname,  plt.gca().get_ylim())
            plt.ylim(bottom=0)
            # if y_top:
            #     plt.ylim(top=y_top)
            #     y_top = None

            # plt.ylim(top = y_top)
            if mname.startswith('Throughput'):
                plt.axhline(y=link_cap, label='Link Capacity')
                plt.legend()

            # plt.ylim(bottom=0)
            plt.gcf().set_size_inches(3.2, 3)

            mname = mname.replace(' ', '_')
            save_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures')
            plt.savefig(os.path.join(save_path, f'{mname}_{link}.{extension}'), bbox_inches='tight')
            plt.clf()

if __name__ == '__main__':
    plot_data(root='/vagrant/logs/newcwv/test2', links=['DSL', 'FTTP', 'FTTC'], algs=['newcwv', 'vreno'], numbers=range(1, 11), extension='pdf')
