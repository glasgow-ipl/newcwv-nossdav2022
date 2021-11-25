import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import os
import numpy as np
import sys
import json
import glob
import argparse

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import parse_access_log
from constants import QUALITY_TO_BPS_3S_IETF
import parse_dash_log


def plot_boxplot(metric_name, data_aggregate, algs, clients, extension, ylabel=None):
    axs = []

    max_y = 0
    for idx, name in enumerate(data_aggregate[metric_name].keys()):
        if idx == 1:
            plt.ylabel(ylabel if ylabel else f'{metric_name} (Mbps)')
        ax = plt.subplot(1, 3, idx+1)
        ax.boxplot(data_aggregate[metric_name][name])
        if max_y < max(ax.get_ylim()):
            max_y = max(ax.get_ylim())
            max_y += .05 * max_y
        ax.set_title(name)
        plt.xticks(range(1, len(algs) + 1), algs)
        axs.append(ax)

    for ax in axs:
        ax.set_ylim(bottom=0, top=max_y)

    save_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures')
    plt.gcf().set_size_inches(8, 3)
    fig_name = os.path.join(save_path, f'{metric_name.replace(" ", "_")}_{clients}_clients.{extension}')
    print(f"Saving {fig_name}")
    plt.savefig(fig_name, bbox_inches='tight')
    plt.clf()
    

def plot_stall_histogram(metric_name, data_aggregate, clients, extension):
    axs = []
    max_y = 0
    for idx, link in enumerate(['DSL', 'FTTC', 'FTTP']):
        ax = plt.subplot(1, 3, idx+1)
        ax.set_title(link)

        newcwv_all = np.array(data_aggregate[metric_name][link][0])
        reno_all = np.array(data_aggregate[metric_name][link][1])
        bin_l = min(min(newcwv_all), min(reno_all)) * .9
        bin_h = max(max(newcwv_all), max(reno_all)) * 1.1

        newcwv = np.extract(newcwv_all > 0, newcwv_all)
        print(f"Removed {len(newcwv_all) - len(newcwv)} newcwv elements")
        reno = np.extract(reno_all > 0, reno_all)
        print(f"Removed {len(reno_all) - len(reno)} nreno elements")


        leap = 2000
        
        bins = np.arange(bin_l, bin_h, leap)
        bins = list(bins)
        ax.hist(newcwv, bins=bins, alpha=.7, label='newcwv')

        ax.hist(reno, bins=bins, color='red', alpha=.7, label='vreno')

        print(newcwv)
        print(reno)
        ax.set_xlabel("Time (ms)")
        if ax.get_ylim()[1] > max_y:
            max_y = ax.get_ylim()[1]
        axs.append(ax)

    for ax in axs:
        ax.set_ylim(top=max_y)
    axs[0].set_ylabel("# of players")

    plt.gcf().set_size_inches(12, 3)
    plt.legend()
    fig_name = metric_name.replace(' ', '_')
    save_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures')
    figname = os.path.join(save_path, f'{fig_name}_{clients}_clients.{extension}')
    print(f"saving {figname}")
    plt.savefig(figname, bbox_inches='tight')
    plt.clf()


def plot_histogram(metric_name, data_aggregate, clients, extension):
    for idx, link in enumerate(['DSL', 'FTTC', 'FTTP']):
        ax = plt.subplot(1, 3, idx+1)
        ax.set_title(link)

        if idx == 0:
            ax.set_ylabel("Percentage Distrubution")

        newcwv = np.array(data_aggregate[metric_name][link][0])
        reno = np.array(data_aggregate[metric_name][link][1])
        bin_l = min(min(newcwv), min(reno)) * .9
        bin_h = max(np.percentile(newcwv, 99.9), np.percentile(reno, 99.9)) * 1.1

        leap = .1
        
        bins = np.arange(bin_l, bin_h, leap)
        bins = list(bins)
        ax.hist(newcwv, bins=bins, alpha=.7, density=True, label='newcwv')

        ax.hist(reno, bins=bins, color='red', alpha=.7, density=True, label='vreno')

        print(max(newcwv), np.percentile(newcwv, 99.9), max(reno), np.percentile(reno, 99.9))

        ax.get_yaxis().set_major_formatter(PercentFormatter(1 / leap))
        ax.set_xlabel("Bandwidth (Mbps)")

    plt.gcf().set_size_inches(12, 3)
    plt.legend()
    fig_name = metric_name.replace(' ', '_')
    save_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures')
    figname = os.path.join(save_path, f'{fig_name}_{clients}_clients.{extension}')
    print(f"saving {figname}")
    plt.savefig(figname, bbox_inches='tight')
    plt.clf()


def plot_cdf(metric_name, data_aggregate, clients, extension):
    for idx, link in enumerate(['DSL', 'FTTC', 'FTTP']):
        ax = plt.subplot(1, 3, idx+1)
        ax.set_title(link)

        newcwv = np.array(data_aggregate[metric_name][link][0])
        reno = np.array(data_aggregate[metric_name][link][1])
        bin_l = min(min(newcwv), min(reno)) * .9
        bin_h = max(np.percentile(newcwv, 99.9), np.percentile(reno, 99.9)) * 1.1

        leap = .1
        
        bins = np.arange(bin_l, bin_h, leap)
        bins = list(bins)

        count, bins_count = np.histogram(newcwv, 100)
        pdf = count / sum(count)
        cdf = np.cumsum(pdf)
        ax.plot(bins_count[1:], cdf, label='newcwv')

        count, bins_count = np.histogram(reno, 100)
        pdf = count / sum(count)
        cdf = np.cumsum(pdf)
        ax.plot(bins_count[1:], cdf, label='reno', color='red')
        ax.axvline(0.44, linestyle='--', c='brown', label='480p')
        ax.axvline(2.64, linestyle='--', c='b', label='720p')
        ax.axvline(4.82, linestyle='--', c='g', label='1080p')

        ax.set_ylim(bottom=0, top=1)
        ax.set_xlim(left=0, right=bin_h)

        # ax.hist(newcwv, bins=bins, alpha=.7, cumulative=True, histtype='step', label='newcwv')
        # ax.hist(reno, bins=bins, color='red', alpha=.7, cumulative=True, histtype='step', label='vreno')
        
        ax.set_xlabel("Bandwidth (Mbps)")
        if idx == 0:
            ax.set_ylabel("CDF")

    plt.gcf().set_size_inches(12, 3)
    plt.legend()
    fig_name = metric_name.replace(' ', '_')
    save_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures')
    figname = os.path.join(save_path, f'{fig_name}_{clients}_clients_cdf.{extension}')
    print(f"saving {figname}")
    plt.savefig(figname, bbox_inches='tight')
    plt.clf()


def plot_data(*, links, algs, extension = 'png', clients=0, target='all'):
    if not clients:
        print('Client argument must be supplied and different from 0', file=sys.stderr)
        sys.exit(1)
    metric_names = ['Average Bitrate',
                        'Average Oscillations',
                        'Throughput Precise',
                        'Throughput Safe',
                        'Rebuffer Ratio']

    tmp_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', 'tmp', str(clients))
    tmp_path = os.path.join(tmp_path, 'parsed_data.json')
    print(f"Using file {tmp_path}")
    with open(tmp_path, 'r') as f:
        metrics = json.load(f)
        print("Parsed data loaded")
        


    clients = metrics['clients']    

    combined = {}
    for link in links:
        for mname in metric_names:
            data = []
            for alg in algs:
                data.append(metrics[link][alg][mname])

            aggregate = combined.get(mname, {})
            aggregate[link] = data
            combined[mname] = aggregate

    if target.lower() == 'throughput precise' or target.lower() == 'all':
        # plot_histogram('Throughput Precise', data_aggregate=combined, clients=clients, extension=extension)
        plot_cdf('Throughput Precise', data_aggregate=combined, clients=clients, extension=extension)
    if target.lower() == 'throughput safe' or target.lower() == 'all':
        # plot_histogram('Throughput Safe', data_aggregate=combined, clients=clients, extension=extension)
        plot_cdf('Throughput Safe', data_aggregate=combined, clients=clients, extension=extension)
    if target.lower() == 'average bitrate' or target.lower() == 'all':
        plot_boxplot('Average Bitrate', combined, algs, clients, extension)
    if target.lower() == 'average oscillations' or target.lower() == 'all':
        plot_boxplot('Average Oscillations', combined, algs, clients, extension)
    if target.lower() == 'rebuffer ratio' or target.lower() == 'all':
        plot_boxplot('Rebuffer Ratio', combined, algs, clients, extension, ylabel='Rebuffer Ratio')


def parse_data(root, links, algs, numbers):
    metrics = {}

    tmp = {alg: {} for alg in algs}

    bitrates = []
    oscillations = []
    throughput_precise = []
    throughput_safe = []
    thr_precise = []
    thr_safe = []
    delays = []
    
    for link in links:
        for alg in algs:
            for number in numbers:
                path = os.path.join(root, link, f'{number}_{alg}')

                access_log = os.path.join(path, 'nginx_access.log')
                quality_aggregate = parse_access_log.get_qualities(access_log)
                avg_bitrates = []
                avg_oscillations = []
                for _client, trace in quality_aggregate.items():
                    _times, qualities = zip(*[value for _key, value in sorted(trace.items())])
                    # print(f"Average bitrate for {_client} is {parse_access_log.calculate_avg_bitrate(qualities, QUALITY_TO_BPS_3S_IETF)}")
                    # print(f"Average Osc of client {_client} is {parse_access_log.calculate_avg_oscillation(qualities, QUALITY_TO_BPS_3S_IETF)}")
                    avg_bitrates.append(parse_access_log.calculate_avg_bitrate(qualities, QUALITY_TO_BPS_3S_IETF))
                    avg_oscillations.append(parse_access_log.calculate_avg_oscillation(qualities, QUALITY_TO_BPS_3S_IETF))

                # print(avg_bitrates)
                avg_bitrate = np.average(avg_bitrates)
                # print(avg_bitrate)
                avg_oscillation = np.average(avg_oscillations)
                bitrates.append(avg_bitrate / 1_000_000)
                # print(bitrates)
                oscillations.append(avg_oscillation / 1_000_000)

                metrics_pattern = os.path.join(path, 'dashjs_metrics*.json')
                metric_files = glob.glob(metrics_pattern)

                for metrics_path in metric_files:
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
                    
                    delays.append(parse_dash_log.get_delay(metrics_path) / parse_dash_log.get_playtime(metrics_path) )

            print(f"Delays: {delays}")
            # Out of simulations calculate the average of the averages
            tmp[alg] = {'Average Bitrate': bitrates,
                        'Average Oscillations': oscillations,
                        'Throughput Precise': thr_precise,
                        'Throughput Safe': thr_safe,
                        'Rebuffer Ratio': delays,
                        }

            bitrates = []
            oscillations = []
            throughput_precise = []
            throughput_safe = []
            thr_precise = []
            thr_safe = []
            delays = []

        # Went through all algorithms, record stats    
        metrics[link] = tmp
        tmp = {}

    metrics['clients'] = len(metric_files)

    tmp_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', 'tmp', str(metrics['clients']))
    os.makedirs(tmp_path, exist_ok=True)
    tmp_path = os.path.join(tmp_path, 'parsed_data.json')
    with open(tmp_path, 'w') as f:
        json.dump(metrics, f, indent=4)
        print("Parsed data saved")


def main():
    root = '/vagrant/logs/clients/5'
    links = ['DSL', 'FTTC', 'FTTP']
    algs = ['newcwv', 'vreno']
    numbers = range(1, 11)
    extension = 'png'
    clients = 5
    parse_data(root=root, links=links, algs=algs, numbers=numbers)
    plot_data(links, algs, extension, clients=clients, target='all')



if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
        sys.exit(0)

    parser = argparse.ArgumentParser(description="")
    
    parser.add_argument('--links', nargs='+', required=True)
    parser.add_argument('--algs', nargs='+', required=True)
    
    # Required for parsing the data
    parser.add_argument('--root')
    parser.add_argument('--runs', nargs='+', type=int)

    parser.add_argument('--parse', type=int, default=0)
    parser.add_argument('--extension', default='pdf')
    parser.add_argument('--target', type=str.lower, choices=['all', 'none', 'average bitrate', 'average oscillations', 'throughput safe', 'throughput precise', 'rebuffer ratio'], default='all')
    parser.add_argument('--clients', type=int, default=0)

    args = parser.parse_args()

    root = args.root
    links = args.links
    algs = args.algs
    numbers = args.runs
    extension = args.extension
    target = args.target

    if args.parse:
        parse_data(root, links, algs, numbers)
    if args.target.lower() != 'none':
        plot_data(links=links, algs=algs, extension=extension, clients=args.clients, target=target)
