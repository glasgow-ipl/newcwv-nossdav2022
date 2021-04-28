import os
import numpy as np
import matplotlib.pyplot as plt

import parse_dash_log
import parse_access_log
import constants

def get_avg_total_stall_time_sim(sim_root, alg_name):
    dirs = os.listdir(sim_root)
    total_stalls = []
    for dir_name in dirs:
        if alg_name in dir_name:
            dash_log_file = os.path.join(sim_root, dir_name, 'dashjs_metrics.json')
            stall_time = parse_dash_log.get_total_stall_time(dash_log_file)
            total_stalls.append(stall_time)

    return np.average(total_stalls)


def get_avg_startup_delay_sim(sim_root, alg_name):
    dirs = os.listdir(sim_root)
    startup_delays = []
    for dir_name in dirs:
        if alg_name in dir_name:
            dash_log_file = os.path.join(sim_root, dir_name, 'dashjs_metrics.json')
            startup_delay = parse_dash_log.get_startup_delay(dash_log_file)
            startup_delays.append(startup_delay)
    
    return np.average(startup_delays)


def get_avg_avg_bitrate(sim_root, alg_name):
    dirs = os.listdir(sim_root)
    avg_bitrates = []
    for dir_name in dirs:
        if alg_name in dir_name:
            access_log_file = os.path.join(sim_root, dir_name, 'nginx_access.log')
            time_qualities = parse_access_log.get_qualities(access_log_file)
            _, qualities = zip(*time_qualities)
            avg_bitrate = parse_access_log.calculate_avg_bitrate(qualities, constants.QUALITY_TO_BPS_3S)
            avg_bitrates.append(avg_bitrate)

    return np.average(avg_bitrates)


def get_avg_bitrate_oscillation(sim_root, alg_name):
    dirs = os.listdir(sim_root)
    bitrate_oscs = []
    for dir_name in dirs:
        if alg_name in dir_name:
            access_log_file = os.path.join(sim_root, dir_name, 'nginx_access.log')
            time_qualities = parse_access_log.get_qualities(access_log_file)
            _, qualities = zip(*time_qualities)
            bitrate_osc = parse_access_log.calculate_avg_oscillation(qualities, constants.QUALITY_TO_BPS_3S)
            bitrate_oscs.append(bitrate_osc)
    
    return np.average(bitrate_oscs)


def gen_dash_metrics_table(doc_root, sim_numbers, alg_names):
    rows = []
    for sn in sim_numbers:
        print(f'working on {sn}')
        avg_bitrates = [int(sn)]
        for alg in alg_names:
            path = os.path.join(doc_root, sn)
            avg_bitrates.append(get_avg_avg_bitrate(path, alg) / 1000)
        bitrate_oscs = [int(sn)]
        for alg in alg_names:
            path = os.path.join(doc_root, sn)
            bitrate_oscs.append(get_avg_bitrate_oscillation(path, alg) / 1000)
        total_stalls = [int(sn)]
        for alg in alg_names:
            path = os.path.join(doc_root, sn)
            total_stalls.append(get_avg_total_stall_time_sim(path, alg))
        startup_delays = [int(sn)]
        for alg in alg_names:
            path = os.path.join(doc_root, sn)
            startup_delays.append(get_avg_startup_delay_sim(path, alg))

        rows.extend(' & '.join([f'{el:.2f}' for el in x]) for x in [avg_bitrates, bitrate_oscs, total_stalls, startup_delays])


    table_content = '\n'.join(rows)
#    print(table_content)
    return rows

def get_avg_bitrate_f_stalls(doc_root, sim_numbers, alg_names):
    bitrate_stalls = []

    for sn in sim_numbers:
        for alg in alg_names:
            path = os.path.join(doc_root, sn)
            avg_bitrate = get_avg_avg_bitrate(path, alg) / 1000 # bps
            stall_time = get_avg_total_stall_time_sim(path, alg) # s
            bitrate_stalls.append((avg_bitrate, stall_time))
        
    return bitrate_stalls


def plot_bitrate_f_stalls(doc_root, sim_numbers):

    bitrate_stalls_bbr = get_avg_bitrate_f_stalls(doc_root, sim_numbers, ['bbr'])

    bitrate, stalls = zip(*bitrate_stalls_bbr)
    plt.scatter(bitrate, stalls, c='r', label='bbr')
    for i in range(bitrate_stalls_bbr):
        plt.annotate(str(i+1), (bitrate[i], stalls[i]))


    bitrate_stalls_cubic = get_avg_bitrate_f_stalls(doc_root, sim_numbers, ['cubic'])

    bitrate, stalls = zip(*bitrate_stalls_cubic)
    plt.scatter(bitrate, stalls, c='g', label='cubic')
    for i in range(bitrate_stalls_bbr):
        plt.annotate(str(i+1), (bitrate[i], stalls[i]))


    bitrate_stalls_reno = get_avg_bitrate_f_stalls(doc_root, sim_numbers, ['reno'])

    bitrate, stalls = zip(*bitrate_stalls_reno)
    plt.scatter(bitrate, stalls, c='b', label='reno')
    for i in range(bitrate_stalls_bbr):
        plt.annotate(str(i+1), (bitrate[i], stalls[i]))

    save_path = '.'
    plt.savefig(os.path.join(save_path, 'fig.png'))
    

if __name__ == '__main__':
    sim_runs = [str(x+1) for x in range(12)]
    rows = gen_dash_metrics_table('/vagrant/logs/dash_if/no_loss/abrThroughput/', sim_runs, ['bbr', 'cubic', 'reno'])
    headers = ['Average Bit-rate (kbps)', 'Bit-rate Oscillation (kbps)', 'Total Stall Time (s)', 'Start-up Delay (ms)']
    for idx, row in enumerate(rows):
        print(headers[idx % len(headers)] + ' & ' + row + ' \\\\' + ('\\midrule' if (idx + 1) % len(headers) == 0 else ''))


 
