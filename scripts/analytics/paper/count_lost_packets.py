import matplotlib.pyplot as plt

plt.rc('font',**{'family':'Times New Roman', 'size': 14})
plt.rc('axes', axisbelow=True)
plt.rcParams['pdf.fonttype'] = 42

import os
import subprocess
import datetime
import glob

import plot_transmission_acks
import matplotlib.pyplot as plt

def get_video_packets(pcap_path):
    p = subprocess.Popen(f'tcpdump -n -r {pcap_path} -ttttt | grep "10.0.0.1.80 >" | grep seq', stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out: bytes
    lines = out.decode().split('\n')

    lines = lines[:-1] # discard the last (empty) line
    seqs = {}
    print(pcap_path)
    # print(lines[0])
    # init_timestamp = datetime.datetime.fromtimestamp(float(lines[0].split()[0]))
    # print(init_timestamp)
    for i, line in enumerate(lines):
        line = line.split()
        # timestamp = (datetime.datetime.fromtimestamp(float(line[0])) - init_timestamp).seconds
        time_delta_str = line[0]
        hours, minutes, seconds = time_delta_str.split(':')
        seconds, microseconds = seconds.split('.')
        timestamp = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), microseconds=int(microseconds)).total_seconds()


        receiver = line[4]
        seq = line[8]
        if ":" not in seq:
            # this is a setup packet
            continue
        key = f'{receiver} {seq}' # A combination of receiver and sequence numbers is unique for a packet
        if key not in seqs:
            seqs[key] = ([timestamp], 1)
        else:
            lost, count = seqs[key]
            lost.append(timestamp)
            seqs[key] = (lost, count + 1)
        
    return seqs


def count_all_packets(root):
    server_pcap_path = os.path.join(root, 'server.pcap')
    server_packets = get_video_packets(server_pcap_path)

    client_pattern = os.path.join(root, 'client*pcap')
    client_paths = glob.glob(client_pattern)

    
    for client_path in client_paths:
        client_ip = os.path.basename(client_path)[len('client_'):-len('.pcap')]
        client_packets = get_video_packets(client_path)
        for key, (timestamps, occurrence) in client_packets.items():
            packet_timestamps, server_occurrence = server_packets[key]
            server_packets[key] = (packet_timestamps, server_occurrence - occurrence)

    return server_packets

def count_lost_packets(root):
    server_packets = count_all_packets(root)

    import matplotlib.pyplot as plt
    send_info = server_packets.values()
    timestamp_send = {}
    for (timestamps, _) in send_info:
        for time in timestamps:
            timestamp_send[time] = timestamp_send.get(time, 0) + 1

    seconds, count = zip(*timestamp_send.items())

    server_packets = {key: (timestamps, occurrence) for key, (timestamps, occurrence) in server_packets.items() if occurrence != 0}

    ack_info = plot_transmission_acks.get_ack_info(os.path.join(root, 'server.pcap'))

    return server_packets


if __name__ == '__main__':
    plot_lost_packets('/vagrant/logs/clients/1/DSL/1_vreno')
    