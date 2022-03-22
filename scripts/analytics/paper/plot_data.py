from matplotlib import ticker
import matplotlib.pyplot as plt

plt.rc('font',**{'family':'Times New Roman', 'size': 15})
plt.rc('axes', axisbelow=True)
plt.rcParams['pdf.fonttype'] = 42

from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import os
import numpy as np
import sys
import json

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import parse_access_log
from constants import QUALITY_TO_BPS_3S_IETF

def plot_boxplot_multiple(*, metric_name, data, algs, links, extension, format_percent=False, y_label=''):
    x_labels_dic = {'newcwv': 'New CWV', 'vreno': 'CWV'}

    agg = {alg: [] for alg in algs}
    x_labels = []
    agg = {l: {c: {alg: [] for alg in algs} for c in data.keys()} for l in links}
    for c, link_aggregate in data.items():
        for link in links:
            for alg in algs:
                plot_data = link_aggregate[link][alg][metric_name]
                x_labels.append(f'{c} client(s)')
                agg[link][c][alg].append(plot_data)

    max_y = 0
    fig, axs = plt.subplots(nrows=len(links), ncols=len(data.keys()))
    axs: Axes
    for i, link in enumerate(agg):
        for j, clients in enumerate(agg[link]): 
            for pos, (alg, data) in enumerate(agg[link][clients].items()):
                ax = axs[i, j] if len(links) > 1 else axs[j]
                ax: Axes
                ax.boxplot(data, positions=2*np.arange(1, len(data) + 1) - pos, labels=[x_labels_dic[alg] for _ in range(len(data))])
                # ax.set_xticks(rotation=90)
                ax.tick_params(axis='x', rotation=15)
                ax.set_title(f'{clients} client(s) {link}')
                max_y = max(max_y, ax.get_ylim()[1])

                if i == 0 and j == 0:
                    ax.set_ylabel(y_label)

    for i, link in enumerate(agg):
        for j, clients in enumerate(agg[link]): 
            ax = axs[i, j] if len(links) > 1 else axs[j]
            ax.set_ylim(0, max_y + .1*max_y)
            if metric_name.lower() == 'rebuffer ratio':
                ax.get_yaxis().set_major_formatter(PercentFormatter(1))
    
    # newcwv = plt.boxplot(agg['newcwv'], medianprops={'color': 'red'}, boxprops={'color': 'red'}, positions=2*np.arange(1, len(agg['newcwv']) + 1) - 1)
    # reno = plt.boxplot(agg['vreno'], medianprops={'color': 'blue'}, boxprops={'color': 'blue'}, positions=(2*np.arange(1, len(agg['vreno']) + 1)))
    # for i, alg in enumerate(algs):
    #     plt.boxplot(agg[alg], positions=[2*x - i for x in range(1, len(agg[alg])+1)])
    
    # plt.legend([newcwv['boxes'][0], reno['boxes'][0]], ['New CWV', 'Reno'])
    # plt.xticks([i+1 for i in range(len(x_labels))], x_labels, rotation=75)
    # _, max_y = plt.ylim()
    # plt.ylim(bottom=0, top=max_y + .1*max_y)
    # print(max_y + .1*max_y)
    # if not y_label:
    #     plt.ylabel(f'{metric_name} (kbps)')
    # else:
    #     plt.ylabel(y_label)

    # for ax in axs:
    #     ax.get_yaxis().set_major_formatter(PercentFormatter(1))

    save_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', f"{metric_name.replace(' ', '_')}.{extension}")
    print(f"Saving {save_path}")
    fig.set_size_inches(15, 3)
    fig.savefig(save_path, bbox_inches='tight')
    # plt.clf()


def plot_rebuffer_ratio(*, metric_name, data, algs, links, extension, format_percent=False, y_label=''):
    title_map = {'newcwv': 'New CWV', 'vreno': 'CWV'}
    plt.rc('font',**{'size': 20})

    agg = {l: {c: {alg: [] for alg in algs} for c in data.keys()} for l in links}
    for c, link_aggregate in data.items():
        for link in links:
            for alg in algs:
                plot_data = link_aggregate[link][alg][metric_name]
                agg[link][c][alg].append(plot_data)
    
    fig, axs = plt.subplots(len(links), len(algs))
    max_y = 0
    for i, alg in enumerate(links):
        for j, alg in enumerate(algs):
            plot_data = []
            for c in data.keys():
                plot_data.append((c, agg[link][c][alg][0]))
            ax = axs[i, j] if len(links) > 1 else axs[j]
            clients, rebuffer_data = zip(*plot_data)
            ax.boxplot(rebuffer_data, labels=clients)
            max_y = max(max_y, ax.get_ylim()[1])
            print(alg, clients, [np.mean(d)* 100 for d in rebuffer_data])
                
    for i, _link in enumerate(links):
        for j, alg in enumerate(algs): 
            ax = axs[i, j] if len(links) > 1 else axs[j]
            ax.set_ylim(0, max_y + .1*max_y)
            if metric_name.lower() == 'rebuffer ratio':
                ax.get_yaxis().set_major_formatter(PercentFormatter(1))
            
            if j == 0:
                ax.set_ylabel('Rebuffer Ratio')
            else:
                ax.set_yticks([])
            if i == len(links) - 1:
                ax.set_xlabel('# Clients')
            if i == 0:
                ax.set_title(title_map[alg])

    save_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures')
    fig_name = os.path.join(save_path, f'{metric_name.replace(" ", "_")}.{extension}')
    fig.set_size_inches(8.5, 3)
    print(f"Saving {fig_name}")
    fig.savefig(fig_name, bbox_inches='tight')
    print(f"Font restored")
    plt.rc('font',**{'size': 15})

def plot_line_errorbar(*, metric_name, data, algs, links, extension, format_percent=False, y_label=''):

    agg = {l: {c: {alg: [] for alg in algs} for c in data.keys()} for l in links}
    for c, link_aggregate in data.items():
        for link in links:
            for alg in algs:
                plot_data = link_aggregate[link][alg][metric_name]
                agg[link][c][alg].append(plot_data)


    for link, data_aggregate in agg.items():
        for clients, alg_info in data_aggregate.items():
            for alg, d in alg_info.items():
                print(f"{clients} clients, {link}-{alg} {d}")

    plt.clf()
    for link in links:
        for alg in algs:
            x = []
            y = []
            y_err = []
            for c in data.keys():
                print(f"{link} {alg} {c}")
                x.append(int(c))
                y.append(np.median(agg[link][c][alg][0]))
                y_err.append(np.std(agg[link][c][alg][0]))
            plt.errorbar(x, y, y_err, label=f'{link}-{alg}')
    
    plt.legend(loc='upper left')
    plt.xticks([int(clients) for clients in data.keys()])
    plt.xlabel("Number of clients")
    plt.ylabel('Mbps')
    figure_name = 'doc/paper/figures/average_oscillations_errorbar.pdf'
    plt.savefig(figure_name, bbox_inches='tight')


def plot_boxplot(metric_name, data_aggregate, algs, clients, extension, ylabel=None, format_percent=False, xticks=None):
    axs = []

    if xticks:
        algs = xticks
    
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

    for i, ax in enumerate(axs):
        ax.set_ylim(bottom=0, top=max_y)
        if format_percent:
            ax.get_yaxis().set_major_formatter(PercentFormatter(1))
        if i != 0:
            ax.set_yticklabels([])

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


def plot_cdf_multiple_link_agg(*, metric_names, data, links, algs, clients, extension, link_agg=None):
    alg_mapping = {'newcwv': 'New CWV', 'vreno': 'CWV'}
    fig, axs = plt.subplots(1, len(clients))

    line_styles = {'Throughput Safe': 'solid', 'Throughput Precise': 'dashdot'}
    colours = {'newcwv': 'red', 'vreno': 'blue'}

    max_x = 0
    for i, client in enumerate(clients):
        for alg, stats in data[client][link_agg].items():
            plot_data = []
            for metric in metric_names:
                plot_data.append((alg, metric, np.array(stats[metric])))
                
            bin_l = min([min(x[2]) for x in plot_data]) * .9
            bin_h = max([np.percentile(x[2], 99.9) for x in plot_data]) * 1.1
            leap = .1

            _bins = np.arange(bin_l, bin_h, leap)

            ax = axs[i]
            ax.set_title(f"{client} client(s)")
            for item in plot_data:
                alg, metric, raw_data = item
                metric_display = 'Instantaneous' if metric.split()[1] == 'Safe' else 'Smoothened'
                count, bins_count = np.histogram(raw_data, 100, range=(bin_l, bin_h))
                pdf = count / sum(count)
                cdf = np.cumsum(pdf)
                ax.plot(bins_count[1:], cdf, 
                label=f'{alg_mapping[alg]} {metric_display}' if i == 0 else '_no_label_', linestyle=line_styles[metric], c=colours[alg], lw=2)
            
            if i == 0:
                ax.set_ylabel('CDF')
            ax.set_xlabel("Bandwidth (Mbps)")
            max_x = max(max_x, ax.get_xlim()[1])

    for i, ax in enumerate(axs):
        ax.set_xlim(left=0, right=max_x)
        ax.axvline(0.44, c='brown',  label='480p' if i==0 else '_no_label', linestyle='dotted')
        ax.axvline(2.64, c='green',  label='720p' if i==0 else '_no_label', linestyle='dotted')
        ax.axvline(4.82, c='purple', label='1080p' if i==0 else '_no_label', linestyle='dotted')

    fig_name = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', f'Throughput_{link_agg}.{extension}')
    fig.legend(bbox_to_anchor=(.73, -0.1), ncol=4)
    fig.set_size_inches(20, 3)
    print(f"Saving {fig_name}")
    fig.savefig(fig_name, bbox_inches='tight')

    return
    for idx, link in enumerate(links):
        ax = plt.subplot(1, 4, idx+1)
        ax.set_title(link)

        plot_data = []
        for alg, stats in data[clients][link].items():
            for metric in metric_names:
                tmp = np.array(stats[metric])
                plot_data.append((alg, metric, tmp))
        
        bin_l = min([min(x[2]) for x in plot_data]) * .9
        bin_h = max([np.percentile(x[2], 99.9) for x in plot_data]) * 1.1
        leap = .1

        bins = np.arange(bin_l, bin_h, leap)

        line_styles = {'Throughput Safe': '--', 'Throughput Precise': ':'}
        colours = {'newcwv': 'red', 'vreno': 'blue'}
        for item in plot_data:
            alg, metric, raw_data = item
            metric_display = 'Instantaneous' if metric.split()[1] == 'Safe' else 'Smoothened'
            count, bins_count = np.histogram(raw_data, 100, range=(bin_l, bin_h))
            pdf = count / sum(count)
            cdf = np.cumsum(pdf)
            ax.plot(bins_count[1:], cdf, label=f'{alg_mapping[alg]} {metric_display}', linestyle=line_styles[metric], c=colours[alg])

        ax.set_ylim(bottom=0)
        ax.axvline(0.44, c='brown',  label='480p')
        ax.axvline(2.64, c='green',  label='720p')
        ax.axvline(4.82, c='purple', label='1080p')

        link_cap = 0
        if link == 'DSL':
            link_cap = 10
        elif link == 'FTTC':
            link_cap = 50
        elif link == 'FTTP':
            link_cap = 145

        ax.axvline(link_cap, c='black', label='Link Cpacity')

        ax.set_xlabel("Bandwidth (Mbps)")
        if idx == 0:
            ax.set_ylabel("CDF")

    plt.gcf().set_size_inches(13, 2)
    ax.legend(loc='upper center', bbox_to_anchor=(-0.2, -0.3), ncol=4)
    save_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', f'Throughput_{clients}_clients.{extension}')
    print(f'Saving {save_path}...')
    plt.savefig(save_path, bbox_inches='tight')
    plt.clf()

def plot_cdf_multiple(*, metric_names, data, links, algs, clients, extension, link_agg=None):
    alg_mapping = {'newcwv': 'New CWV', 'vreno': 'Reno'}
    for idx, link in enumerate(links):
        ax = plt.subplot(1, 4, idx+1)
        ax.set_title(link)

        plot_data = []
        for alg, stats in data[clients][link].items():
            for metric in metric_names:
                tmp = np.array(stats[metric])
                plot_data.append((alg, metric, tmp))
        
        bin_l = min([min(x[2]) for x in plot_data]) * .9
        bin_h = max([np.percentile(x[2], 99.9) for x in plot_data]) * 1.1
        leap = .1

        bins = np.arange(bin_l, bin_h, leap)

        line_styles = {'Throughput Safe': '--', 'Throughput Precise': ':'}
        colours = {'newcwv': 'red', 'vreno': 'blue'}
        for item in plot_data:
            alg, metric, raw_data = item
            metric_display = 'Instantaneous' if metric.split()[1] == 'Safe' else 'Smoothened'
            count, bins_count = np.histogram(raw_data, 100, range=(bin_l, bin_h))
            pdf = count / sum(count)
            cdf = np.cumsum(pdf)
            ax.plot(bins_count[1:], cdf, label=f'{alg_mapping[alg]} {metric_display}', linestyle=line_styles[metric], c=colours[alg])

        ax.set_ylim(bottom=0)
        ax.axvline(0.44, c='brown',  label='480p')
        ax.axvline(2.64, c='green',  label='720p')
        ax.axvline(4.82, c='purple', label='1080p')

        link_cap = 0
        if link == 'DSL':
            link_cap = 10
        elif link == 'FTTC':
            link_cap = 50
        elif link == 'FTTP':
            link_cap = 145

        ax.axvline(link_cap, c='black', label='Link Cpacity')

        ax.set_xlabel("Bandwidth (Mbps)")
        if idx == 0:
            ax.set_ylabel("CDF")

    plt.gcf().set_size_inches(13, 2)
    ax.legend(loc='upper center', bbox_to_anchor=(-0.2, -0.3), ncol=4)
    save_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', f'Throughput_{clients}_clients.{extension}')
    print(f'Saving {save_path}...')
    plt.savefig(save_path, bbox_inches='tight')
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
        plot_cdf('Throughput Precise', data=combined, clients=clients, extension=extension)
    if target.lower() == 'throughput safe' or target.lower() == 'all':
        # plot_histogram('Throughput Safe', data_aggregate=combined, clients=clients, extension=extension)
        plot_cdf('Throughput Safe', data=combined, clients=clients, extension=extension)
    if target.lower() == 'average bitrate' or target.lower() == 'all':
        plot_boxplot('Average Bitrate', combined, algs, clients, extension, xticks=['New CWV', 'Reno'])
    if target.lower() == 'average oscillations' or target.lower() == 'all':
        plot_boxplot('Average Oscillations', combined, algs, clients, extension, xticks=['New CWV', 'Reno'])
    if target.lower() == 'rebuffer ratio' or target.lower() == 'all':
        plot_boxplot('Rebuffer Ratio', combined, algs, clients, extension, ylabel='Rebuffer Ratio', format_percent=True, xticks=['New CWV', 'Reno'])


def plot_data_multiple(*, links, algs, extension = 'png', clients=0, target='all', clients_combined=None, link_agg=None):
    if not clients and target == 'throughput':
        print('Client argument must be supplied and different from 0', file=sys.stderr)
        sys.exit(1)

    data_aggregate = {}
    for c in clients_combined:
        tmp_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', 'tmp', c)
        tmp_path = os.path.join(tmp_path, 'parsed_data.json')
        print(f"Using file {tmp_path}")
        with open(tmp_path, 'r') as f:
            metrics = json.load(f)
            print("Parsed data loaded")
        data_aggregate[c] = metrics


    if target.lower() == 'throughput' or target.lower() == 'all':
        if target.lower() == 'all':
            for c in data_aggregate:
                plot_cdf_multiple(metric_names=['Throughput Precise', 'Throughput Safe'], data=data_aggregate, links=links, algs=algs, clients=str(c), extension=extension)    
        else:    
            plot_cdf_multiple(metric_names=['Throughput Precise', 'Throughput Safe'], data=data_aggregate, links=links, algs=algs, clients=str(clients), extension=extension)

    if target.lower() == 'average bitrate' or target.lower() == 'all':
        plot_boxplot_multiple(metric_name='Average Bitrate', data=data_aggregate, links=links, algs=algs, extension=extension)
    if target.lower() == 'average oscillations' or target.lower() == 'all':
        plot_boxplot_multiple(metric_name='Average Oscillations', data=data_aggregate, links=links, algs=algs, extension=extension, y_label="Mbps")
        plot_line_errorbar(metric_name='Average Oscillations', data=data_aggregate, links=links, algs=algs, extension=extension, y_label="Mbps")
    if target.lower() == 'rebuffer ratio' or target.lower() == 'all':
        plot_rebuffer_ratio(metric_name='Rebuffer Ratio', data=data_aggregate, links=links, algs=algs, extension=extension, format_percent=True, y_label='Rebuffer Ratio')
    if target.lower() == 'bitrate_derivatives':
        #TODO: Data parsing and plotting happening at the same time. Need to separate them
        plot_bitrate_distribution(log_root='/vagrant/logs/clients', links=links, client_runs=clients_combined, extension=extension)
    if target.lower() == 'throughput agg' or target.lower() == 'all':
        plot_cdf_multiple_link_agg(metric_names=['Throughput Precise', 'Throughput Safe'], data=data_aggregate, links=links, algs=algs, clients=clients_combined, extension=extension, link_agg=link_agg)


def plot_bitrate_distribution(log_root, client_runs, links, extension):
    quality_indexes = {k: i for i, k in enumerate(QUALITY_TO_BPS_3S_IETF.keys())}
    quality_distribution_alg_link_clients = {}

    clients = os.listdir(log_root)
    for num_clients in clients:
        client_root = os.path.join(log_root, num_clients)
        links = sorted(os.listdir(client_root))
        quality_distribution_alg_link = quality_distribution_alg_link_clients.get(num_clients, {})
        for link in links:
            link_root = os.path.join(client_root, link)
            runs = sorted(os.listdir(link_root))
            quality_distribution_alg = quality_distribution_alg_link.get(link, {})
            for run in runs:
                access_log = os.path.join(link_root, run, 'nginx_access.log')
                quality_report = parse_access_log.get_qualities(access_log)
                if 'newcwv' in run:
                    quality_distribution = quality_distribution_alg.get('newcwv', {})
                else:
                    quality_distribution = quality_distribution_alg.get('reno', {})

                for _client, report in quality_report.items():
                    items = list(report.items())
                    previous = quality_indexes[items[0][1][1]]
                    for _chunk, (_time, quality) in items[1:]:
                        current = quality_indexes[quality] 
                        offset =  current - previous
                        previous = current
                        quality_distribution[offset] = quality_distribution.get(offset, 0) + 1
            
                if 'newcwv' in run:
                    quality_distribution_alg['newcwv'] = quality_distribution
                else:
                    quality_distribution_alg['reno'] = quality_distribution

            quality_distribution_alg_link[link] = quality_distribution_alg

        quality_distribution_alg_link_clients[num_clients] = quality_distribution_alg_link


    fig, axs = plt.subplots(1, 4)
    axs_list = []
    client_runs = ['1', '2', '3', '5']
    links = ['DSL']
    algs = ["reno", "newcwv"]
    WIDTH = .4
    y_min = 100
    y_max = 0
    for i, client in enumerate(client_runs):
        for j, link in enumerate(links):
            y_lim = 0
            for k, alg in enumerate(algs):
                # plot_dic = {k: v for k, v in quality_distribution_alg_link_clients[client][link][alg].items() if k != 0}
                plot_dic = quality_distribution_alg_link_clients[client][link][alg]
                if plot_dic:
                    labels, heights = zip(*plot_dic.items())
                else:
                    labels = []
                    heights = []
                all_elements = sum(quality_distribution_alg_link_clients[client][link][alg].values())
                positions = np.array(labels)
                if k == 0:
                    positions = positions + WIDTH / 2
                else:
                    positions = positions - WIDTH / 2
                
                ax = axs[i] if len(links) == 1 else axs[j, i]

                label_map = {'reno': 'CWV', 'newcwv': 'New CWV'}
                heights = [100 * h / all_elements for h in heights]
                ax.bar(positions, heights, width=WIDTH, label=label_map[alg] if i==1 and j==0 else '_no_label')
                ax.set_title(f'{link} {client} Clients')
                ax.set_xlim(-3, 3)
                ax.set_xticks(np.arange(-2, 3))

                if i == 0:
                    ax.set_ylabel('Fraction of chunks')
                if j == len(links) - 1:
                    ax.set_xlabel('Representation Change')

                ax.set_yscale('log')
                # ax.set_ylim(top= 100)
                y_min = min(y_min, ax.get_ylim()[0])
                y_max = max(y_max, ax.get_ylim()[1])
                axs_list.append(ax)
                
    for i, ax in enumerate(axs_list):
        ax.set_ylim(bottom=y_min, top=100)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y:g}%'))
        if i != 0 and i != 1:
            ax.set_yticks([])
    
    fig.legend(bbox_to_anchor=(0.65, -0.1), ncol=2)
    fig.set_size_inches(15, 3)
    fig_name = f'/vagrant/doc/paper/figures/bitrate_derivative_distribution.{extension}'
    print(f"Saving {fig_name}")
    fig.savefig(fig_name, bbox_inches='tight')


def plot_packet_loss(root):
    clients_combined = ['1', '2', '3', '5']
    link_types = ['DSL', 'FTTC', 'FTTP']
    # if not clients and target == 'throughput':
    #     print('Client argument must be supplied and different from 0', file=sys.stderr)
    #     sys.exit(1)

    data_aggregate = {}
    for c in clients_combined:
        tmp_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', 'tmp', c)
        tmp_path = os.path.join(tmp_path, 'parsed_data.json')
        print(f"Using file {tmp_path}")
        with open(tmp_path, 'r') as f:
            metrics = json.load(f)
            print("Parsed data loaded")
        data_aggregate[c] = metrics['dropped_packets']

        # print(data_aggregate.items())
        # fig, axs = plt.subplots(1, 3)
        # for key in clients_combined:
        #     for link in link_types:
    plt.plot(data_aggregate['1']['DSL']['newcwv'].values(), color='r', alpha=.5, label='New CWV')
    plt.plot(data_aggregate['1']['DSL']['vreno'].values(), color='b', alpha =.5, label='Reno')

    # plt.xlim(left=100, right=110)
    fig_name = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', 'test.png')
    plt.legend()
    print(f"saved {fig_name}")
    plt.savefig(fig_name)

        

def main():
    root = '/vagrant/logs/clients/5'
    links = ['DSL', 'FTTC', 'FTTP']
    algs = ['newcwv', 'vreno']
    numbers = range(1, 11)
    extension = 'png'
    clients = 5
    clients_combined = ['1', '2', '3', '5']
    # parse_data(root=root, links=links, algs=algs, numbers=numbers)
    # plot_data(links=links, algs=algs, extension=extension, clients=clients, target='rebuffer ratio')
    plot_data_multiple(links=links, algs=algs, extension=extension, clients=clients, target='throughput', clients_combined=clients_combined)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        plot_bitrate_distribution('/vagrant/logs/clients')
        exit()
        main()
        sys.exit(0)