import os
import json
import glob
import sys
import numpy as np

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import count_lost_packets
import parse_access_log
import parse_dash_log
from constants import QUALITY_TO_BPS_3S_IETF, VIDEO_CACHED_RESPONSE_MS


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

    drop_data = {}
    
    for link in links:
        for alg in algs:
            for number in numbers:
                path = os.path.join(root, link, f'{number}_{alg}')

                # client_aggregate = drop_data.get(number, {})
                link_aggregate = drop_data.get(link, {})
                alg_aggregate = link_aggregate.get(alg, {i: 0 for i in range(700)})

                dropped_packets_server = count_lost_packets.count_lost_packets(path)
                for id_seq, (dropped_timestamps, occurence) in dropped_packets_server.items():
                    # the first _occurence_ packet were lost, record them with their timestamps
                    for i, relative_time in enumerate(dropped_timestamps):
                        if i == occurence:
                            break
                        drop_count = alg_aggregate.get(relative_time, 0)
                        alg_aggregate[relative_time] = drop_count + 1
                
                link_aggregate[alg] = alg_aggregate
                # client_aggregate[link] = link_aggregate
                drop_data[link] = link_aggregate
                

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
                    precise_list = [el[0] for el in precise_list if el[-2] > VIDEO_CACHED_RESPONSE_MS]
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

    metrics['dropped_packets'] = drop_data
    metrics['clients'] = len(metric_files)

    tmp_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', 'tmp', str(metrics['clients']))
    os.makedirs(tmp_path, exist_ok=True)
    tmp_path = os.path.join(tmp_path, 'parsed_data.json')
    with open(tmp_path, 'w') as f:
        json.dump(metrics, f, indent=4)

    print(f"Parsed data saved {tmp_path}")
