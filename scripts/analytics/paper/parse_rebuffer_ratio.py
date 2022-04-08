import os
import glob
import json
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import parse_dash_log

import argparse

def parse_rebuffer_ratio(root, links, algs, numbers):
    metrics = {}

    tmp = {alg: {} for alg in algs}

    delays = []

    for link in links:
        for alg in algs:
            for number in numbers:
                path = os.path.join(root, link, f'{number}_{alg}')
                metrics_pattern = os.path.join(path, 'dashjs_metrics*.json')
                metric_files = glob.glob(metrics_pattern)

                for metrics_path in metric_files:
                    delays.append(parse_dash_log.get_delay(metrics_path) / parse_dash_log.get_playtime(metrics_path) )

            tmp[alg] = {
                        'Rebuffer Ratio': delays,
                        }

            delays = []

        # Went through all algorithms, record stats    
        metrics[link] = tmp
        tmp = {}

    metrics['clients'] = len(metric_files)

    tmp_path = os.path.join('/', 'vagrant', 'doc', 'paper', 'figures', 'tmp', str(metrics['clients']))
    os.makedirs(tmp_path, exist_ok=True)
    tmp_path = os.path.join(tmp_path, 'rebuffer_ratio.json')
    with open(tmp_path, 'w') as f:
        json.dump(metrics, f, indent=4)

    print(f"Parsed data saved {tmp_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    
    parser.add_argument('--links', nargs='+', required=True)
    parser.add_argument('--algs', nargs='+', required=True)
    
    # Required for parsing the data
    parser.add_argument('--root')
    parser.add_argument('--runs', nargs='+', type=int)

    args = parser.parse_args()

    root = args.root
    links = args.links
    algs = args.algs
    numbers = args.runs

    parse_rebuffer_ratio(root=root, links=links, algs=algs, numbers=numbers)
