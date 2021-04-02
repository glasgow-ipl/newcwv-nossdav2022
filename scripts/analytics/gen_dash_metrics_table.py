import os
import numpy as np

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
            avg_bitrate = parse_access_log.calculate_avg_bitrate(access_log_file)
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
    
    for sn in sim_numbers:
        avg_bitrates = [sn]
        for alg in alg_names:
            path = os.path.join(doc_root, sn)
            avg_bitrates.append(get_avg_avg_bitrate(path, alg))
        bitrate_oscs = [sn]
        for alg in alg_names:
            path = os.path.join(doc_root, sn)
            bitrate_oscs.append(get_avg_bitrate_oscillation(path, alg))
        total_stalls = [sn]
        for alg in alg_names:
            path = os.path.join(doc_root, sn)
            total_stalls.append(get_avg_total_stall_time_sim(path, alg))
        startup_delays = [sn]
        for alg in alg_names:
            path = os.path.join(doc_root, sn)
            startup_delays.append(get_avg_startup_delay_sim(path, alg))

    table_rows = [' & '.join(x) for x in [avg_bitrates, bitrate_oscs, total_stalls, startup_delays]]
    table_content = '\n'.join(table_rows)
    print(table_content)
    return table_content

if __name__ == '__main__':
    pass