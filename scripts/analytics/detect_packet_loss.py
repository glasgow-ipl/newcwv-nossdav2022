import os
import subprocess

def get_lost_packets(pcap_path):
    out = subprocess.run(f'tcpdump -n -r {pcap_path}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    records = out.stdout.decode().split('\n')

    server_records = [x for x in records if '10.0.0.1.80 > ' in x and 'length 0' not in x]

    seqs = {}
    for rec in server_records:
        client_port = get_client_port(rec)
        seq = get_seq_number(rec)
        seqs[(client_port, seq)] = seqs.get((client_port, seq), 0) + 1


    lost_seqs = {k: v for k, v in seqs.items() if v > 1}

    return _get_lost_packets(server_records, lost_seqs)


def _get_lost_packets(server_records, lost_seqs):
    lost_pairs, _ = zip(*lost_seqs)

    lost_packets = []
    loss_times = []

    for rec in server_records:
        client_port = get_client_port(rec)
        seq = get_seq_number(rec)
        check_key = (client_port, seq)
        if lost_seqs.get(check_key, 0) > 1:
            lost_packets.append(rec)
            lost_seqs[check_key] = lost_seqs[check_key] - 1
            loss_times.append(get_timestamp(rec))
        
    # print(loss_times)
    
    return loss_times


def get_client_port(pcap_line):
    return int(pcap_line.split('> ')[1].split(': ')[0].split('.')[-1])


def get_seq_number(pcap_line):
    return int(pcap_line.split('seq ')[1].split(':')[0])


def get_timestamp(pcap_line):
    return pcap_line.split(' ')[0]

def foo():
    print('hi')

if __name__ == '__main__':
    get_lost_packets('/vagrant/logs/tmp/server.pcap')
