import glob
import json
import numpy as np


def main():
    data_files = glob.glob('doc/paper/figures/tmp/*/*.json')

    metric_names = ['Average Bitrate',
                        'Average Oscillations',
                        'Throughput Precise',
                        'Throughput Safe',
                        'Rebuffer Ratio']

    links = ['DSL', 'FTTC', 'FTTP']
    algs = ['newcwv', 'vreno']

    table_data = {}

    for data_file in sorted(data_files): 
        print(f"File {data_file}")
        with open(data_file, 'r') as f:
            metrics = json.load(f)

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


        data_aggregate = combined
        metric_names = ['Rebuffer Ratio', 'Average Bitrate', 'Average Oscillations', 'Throughput Precise', 'Throughput Safe']
        
        # Boxplot
        for metric_name in metric_names:
            for name in data_aggregate[metric_name].keys():
                newcwv, reno = data_aggregate[metric_name][name]
                for idx, data in enumerate([newcwv, reno]):
                    table_data[(metric_name, name, clients, algs[idx])] = {}
                    table_data[(metric_name, name, clients, algs[idx])]["Mean"] = np.mean(data)
                    table_data[(metric_name, name, clients, algs[idx])]["Standard Deviation"] = np.std(data)
                    table_data[(metric_name, name, clients, algs[idx])]["99 Percentile"] = np.percentile(data, 99)

    clients = [1, 2, 3, 5]
    algs = ['newcwv', 'vreno']
    col_headers = ['Mean', "Standard Deviation", "99 Percentile"]
    print(r'''\begin{table}[]
            \begin{tabular}{llllll}
                Link & Clients & Algorithm & Mean & std & 99 \\''')
    for metric_name in metric_names:
        for link in links:
            for client in clients:
                for alg in algs:
                        print(f'{metric_name} & {link} & {client} & {alg} & ', end='')
                        print(' & '.join(f'{table_data[(metric_name, link, client, alg)][ch]:.3f}' for ch in col_headers), end='')
                        print(' \\\\')
                print('\\midrule')
    print('''\end{tabular}
        \end{table}
            ''')

if __name__ == '__main__':
    main()
