import subprocess
import matplotlib.pyplot as plt
import json
import os

def plot_server_throughput(pcap_location):
    log_dir = os.path.dirname(pcap_location)
    json_file = os.path.join(log_dir, 'throughput.json')
    if os.path.exists(json_file):
        with open(json_file) as f:
            server_thr = json.load(f)
    else:
        server_thr = process_pcap(pcap_location)
    
    time, thr = zip(*server_thr.items())
    plt.plot(time, thr)
    plt.gcf().set_size_inches(40, 7)
    thr_report_loc = os.path.join(log_dir, 'thr.png')
    plt.savefig(thr_report_loc)


def process_pcap(pcap_location):
    # with open('/vagrant/logs/thr_vreno/server.pcap') as f:
    #     pass

    server_thr = {}

    out = subprocess.run(f'tcpdump -r {pcap_location}', shell=True, stdout=subprocess.PIPE)

    for line in out.stdout.decode().split('\n'):
        if '10.0.0.1.http >' in line:
            print(line)
            items = line.split()
            time = items[0]
            len_label = items.index('length')
            len_str = items[len_label + 1]
            # For HTTP packets, the HTTP header follows the length attribute and a column ":" is added after the length
            len_str = len_str[:-1] if len_str[-1] == ':' else len_str
            length = int(len_str) * 8 / 1_000_000 # we want values in Mbps
            time_sec = time.split('.')[0]
            server_thr[time_sec] = server_thr.get(time_sec, 0) + length

    print(sorted(server_thr.items()))

    log_dir = os.path.dirname(pcap_location)
    thr_json = os.path.join(log_dir, 'throughput.json')
    with open(thr_json, 'w') as f:
        json.dump(server_thr, f)

    return server_thr 

if __name__ == '__main__':
    plot_server_throughput('/vagrant/logs/curtis_test_inc2_ka/server.pcap')


