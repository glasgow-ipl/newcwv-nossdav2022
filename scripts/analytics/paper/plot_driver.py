import argparse
from plot_data import plot_data_multiple
from parse_data import parse_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    
    parser.add_argument('--links', nargs='+', required=True)
    parser.add_argument('--algs', nargs='+', required=True)
    
    # Required for parsing the data
    parser.add_argument('--root')
    parser.add_argument('--runs', nargs='+', type=int)

    parser.add_argument('--parse', type=int, default=0)
    parser.add_argument('--extension', default='pdf')
    parser.add_argument('--link_agg', type=str)
    parser.add_argument('--target', type=str.lower, choices=['all', 'none', 'average bitrate', 'average oscillations', 'rebuffer ratio', 'throughput', 'bitrate_derivatives', 'throughput agg'], default='all')
    parser.add_argument('--clients', type=int, default=0)

    parser.add_argument('--clients_combined', nargs='+')

    args = parser.parse_args()

    root = args.root
    links = args.links
    algs = args.algs
    numbers = args.runs
    extension = args.extension
    target = args.target
    link_agg = args.link_agg

    if args.parse:
        parse_data(root, links, algs, numbers)
    if args.target.lower() != 'none':
        plot_data_multiple(links=links, algs=algs, extension=extension, clients=args.clients, clients_combined=args.clients_combined, target=target, link_agg=link_agg)
