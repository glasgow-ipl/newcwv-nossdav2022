import os
import constants
import parse_dash_log
import parse_access_log
import numpy as np
from matplotlib import pyplot as plt
# from . import parse_dash_log
# from . import parse_access_log
# from . import constants

def get_app_metrics(log_root, name_template, run_suffix):
    app_metrics_list = []
    for i in run_suffix:
        app_metrics = {}
        name = name_template + (str(i) if i else '')
        name_dashjs = os.path.join(log_root, name, 'dashjs_metrics.json')
        app_metrics['delay'] = parse_dash_log.get_startup_delay(name_dashjs)

        # dash log
        name_access_log = os.path.join(log_root, name, 'nginx_access.log')
        qualities = parse_access_log.get_qualities(name_access_log)
        _, qualities = zip(*qualities)
        app_metrics['avg_bitrate'] = parse_access_log.calculate_avg_bitrate(qualities, constants.QUALITY_TO_BPS_2S_NEWCWV)
        app_metrics['avg_oscillation'] = parse_access_log.calculate_avg_oscillation(qualities, constants.QUALITY_TO_BPS_2S_NEWCWV)
        app_metrics_list.append(app_metrics)

    return app_metrics_list

def plot_stats(log_root):
    BAR_WIDTH = .3
    fig, ax = plt.subplots(3, sharex=True)

    newcwv_app_list = get_app_metrics(log_root, 'newcwv_newcwvh', [0, 2, 3])
    reno_app_list = get_app_metrics(log_root, 'newcwv_renoh', [0, 2, 3])

    delays = [x['delay'] for x in reno_app_list]
    delays.append(np.average(delays))
    ax[0].bar(np.arange(len(delays)) + BAR_WIDTH, delays, width=BAR_WIDTH, label='Reno')

    delays = [x['delay'] for x in newcwv_app_list]
    delays.append(np.average(delays))
    ax[0].bar(np.arange(len(delays)), delays, width=BAR_WIDTH, label='New CWV')

    # ax[0].set_xlabel('Simulation #')
    ax[0].set_ylabel('Start-up delay (ms)')

    avg_bitrates = [x['avg_bitrate'] for x in reno_app_list]
    avg_bitrates.append(np.average(avg_bitrates))
    ax[1].bar(np.arange(len(avg_bitrates)) + BAR_WIDTH, avg_bitrates, width=BAR_WIDTH, label='Reno')

    avg_bitrates = [x['avg_bitrate'] for x in newcwv_app_list]
    avg_bitrates.append(np.average(avg_bitrates))
    ax[1].bar(np.arange(len(avg_bitrates)), avg_bitrates, width=BAR_WIDTH, label='New CWV')

    ax[1].set_ylabel('Average bitrates (bps)')

    avg_oscs = [x['avg_oscillation'] for x in reno_app_list]
    avg_oscs.append(np.average(avg_oscs))
    ax[2].bar(np.arange(len(avg_oscs)) + BAR_WIDTH, avg_oscs, width=BAR_WIDTH, label='Reno')

    avg_oscs = [x['avg_oscillation'] for x in newcwv_app_list]
    avg_oscs.append(np.average(avg_oscs))
    ax[2].bar(np.arange(len(avg_oscs)), avg_oscs, width=BAR_WIDTH, label='New CWV')

    ax[2].set_ylabel("Average Bit-rate Oscillation (bps)")

    plt.xlabel("Simulation #")
    labels = [str(i) for i in range(1, len(avg_bitrates))]
    labels.append('Average')
    ax[2].set_xticks(np.arange(len(avg_bitrates)) + BAR_WIDTH / 2)
    ax[2].set_xticklabels(labels)

    fig = plt.gcf()
    fig.set_size_inches((12, 10))

    plt.legend()
    plt.savefig('app_metrics.png', bbox_inches='tight')

if __name__ == '__main__':
    plot_stats('/vagrant/logs/tmp/newcwv/3_18')


