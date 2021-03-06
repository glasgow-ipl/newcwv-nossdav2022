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


def parse_data(root, links, algs, numbers, out_dir=None):
    metrics = {}

    tmp = {alg: {} for alg in algs}

    bitrates = []
    oscillations = []
    throughput_precise = []
    throughput_safe = []
    thr_precise = []
    thr_safe = []
    delays = []

    dropped_packets = {link: {alg: {run: {} for run in numbers} for alg in algs} for link in links}

    for link in links:
        for alg in algs:
            for number in numbers:
                path = os.path.join(root, link, f'{number}_{alg}')
                server_packets = count_lost_packets.count_all_packets(path)

                all_packets = len(server_packets)
                num_lost_packets = sum([1 for _, (_, occurence) in server_packets.items() if occurence != 0])
                
                dropped_packets[link][alg][int(number)] = {'all': all_packets, 'lost': num_lost_packets}

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

    metrics['dropped_packets'] = dropped_packets
    metrics['clients'] = len(metric_files)

    if not out_dir:
        # Get the directory tree after logs/
        appendix = root.split('logs' + os.path.sep, maxsplit=2)[1]
        out_dir = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', 'parsed_data', appendix)

    os.makedirs(out_dir, exist_ok=True)
    save_path = os.path.join(out_dir, 'parsed_data.json')
    with open(save_path, 'w') as f:
        json.dump(metrics, f, indent=4)

    print(f"Parsed data saved {save_path}")

    quality_indexes = {k: i for i, k in enumerate(QUALITY_TO_BPS_3S_IETF.keys())}
    quality_distribution_alg_link = {}

    for link in links:
        for alg in algs:
            quality_distribution_alg = quality_distribution_alg_link.get(link, {})
            for number in numbers:
                path = os.path.join(root, link, f'{number}_{alg}')
                access_log = os.path.join(path, 'nginx_access.log')
                quality_report = parse_access_log.get_qualities(access_log)
                if alg == 'newcwv':
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
            
                if alg == 'newcwv':
                    quality_distribution_alg['newcwv'] = quality_distribution
                else:
                    quality_distribution_alg['reno'] = quality_distribution

                
            quality_distribution_alg_link[link] = quality_distribution_alg


    os.makedirs(out_dir, exist_ok=True)
    save_path = os.path.join(out_dir, 'quality_distribution.json')
    with open(save_path, 'w') as f:
        json.dump(quality_distribution_alg_link, f, indent=4)

    print(f"Parsed data saved {save_path}")
