import os
import subprocess
import datetime
import matplotlib.pyplot as plt


def plot_ack_info(pcap_file):
    ack_info = get_ack_info(pcap_file=pcap_file)

    times, acks = zip(*ack_info)
    plt.scatter(times, acks)

    plt.xlim(left=102, right=104)

    figname = '/vagrant/img/test.png'
    print(f"Saving {figname}")
    plt.savefig(figname)


def get_ack_info(pcap_file):
    res = subprocess.Popen(f'tcpdump -ttttt -r {pcap_file}', shell=True, stdout=subprocess.PIPE)
    out, err = res.communicate()
    lines = out.decode().strip().split('\n')
    filtered = []
    for line in lines:
        tokens = line.split()
        sender = tokens[2]
        flags = tokens[6]
        if '10.0.0.1' in sender and 'S' not in flags and 'F' not in flags and 'seq' in line:
            filtered.append(line)
    
    time_ack = []
    for line in filtered:
        tokens = line.split()
        seq = tokens[8]
        seq = int(seq.split(':')[1][:-1])
        time_delta_str = tokens[0]
        hours, minutes, seconds = time_delta_str.split(':')
        seconds, microseconds = seconds.split('.')
        td = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), microseconds=int(microseconds))
        time_ack.append((td.total_seconds(), seq))

    return time_ack

if __name__ == '__main__':
    plot_ack_info('/vagrant/logs/clients/1/DSL/1_newcwv/server.pcap')