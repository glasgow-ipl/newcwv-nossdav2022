import os
import sys
import numpy as np
import glob


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


import count_lost_packets
import json


def parse_dropped_packets(root, links, algs, numbers, out_dir=None):
    metrics = {}

    tmp = {alg: {} for alg in algs}

    dropped_packets = {link: {alg: {run: {} for run in numbers} for alg in algs} for link in links}

    for link in links:
        for alg in algs:
            for number in numbers:
                path = os.path.join(root, link, f'{number}_{alg}')
                server_packets = count_lost_packets.count_all_packets(path)

                all_packets = len(server_packets)
                num_lost_packets = sum([1 for _, (_, occurence) in server_packets.items() if occurence != 0])
                
                dropped_packets[link][alg][int(number)] = {'all': all_packets, 'lost': num_lost_packets}

                metrics_pattern = os.path.join(path, 'dashjs_metrics*.json')
                metric_files = glob.glob(metrics_pattern)


    metrics['dropped_packets'] = dropped_packets
    metrics['clients'] = len(metric_files)

    if not out_dir:
        # Get the directory tree after logs/
        appendix = root.split('logs' + os.path.sep, maxsplit=2)[1]
        out_dir = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', 'parsed_data', appendix)

    save_path = os.path.join(out_dir, str(metrics['clients']))
    os.makedirs(save_path, exist_ok=True)
    save_path = os.path.join(save_path, 'dropped_packets.json')
    with open(save_path, 'w') as f:
        json.dump(metrics, f, indent=4)

    print(f"Parsed data saved {save_path}")


if __name__ == '__main__':
    root = '/vagrant/logs/newcwv/clients/1/abr/abrThroughput'
    links = ['1_400']
    algs = ['newcwv', 'vreno']
    numbers = [1, 2, 3]
    out_dir = '/vagrant/doc/paper/figures/parsed_data/newcwv'

    parse_dropped_packets(root=root, links=links, algs=algs, numbers=numbers, out_dir=out_dir)
