import os
import subprocess

def get_lost_packets(pcap_path):
    out = subprocess.run(f'tcpdump -n -r {pcap_path}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    records = out.stdout.decode().split('\n')

    server_records = [x for x in records if '10.0.0.1.80 > ' in x and 'length 0' not in x]

    seqs = {}
    for rec in server_records:
        client_port = get_port(rec, 1)
        seq = get_seq_number(rec)
        seqs[(client_port, seq)] = seqs.get((client_port, seq), 0) + 1


    lost_seqs = {k: v for k, v in seqs.items() if v > 1}

    return _get_lost_packets(server_records, lost_seqs)


def _get_lost_pahackets(server_records, lost_seqs):
    lost_pairs, _ = zip(*lost_seqs)

    lost_packets = []
    loss_times = []

    for rec in server_records:
        client_port = get_port(rec, 1)
        seq = get_seq_number(rec)
        check_key = (client_port, seq)
        if lost_seqs.get(check_key, 0) > 1:
            lost_packets.append(rec)
            lost_seqs[check_key] = lost_seqs[check_key] - 1
            loss_times.append(get_timestamp(rec))
        
    # print(loss_times)
    
    return loss_times


def get_port(pcap_line, idx):
    return int(pcap_line.split('> ')[idx].split(': ')[0].split('.')[-1])


def get_seq_number(pcap_line):
    return int(pcap_line.split('seq ')[1].split(':')[0])


def get_timestamp(pcap_line):
    return pcap_line.split(' ')[0]

def get_active_periods(pcap_file):
    out = subprocess.run(f'tshark -t a -Y http -r  {pcap_file}', shell=True, stdout=subprocess.PIPE)

    not_found_quota = 1 # Browser request favicon. We do not have one. Ignore the first 404 response

    req = {}

    downloads = []

    records = out.stdout.decode().strip().split('\n')
    for rec in records:
        if 'favicon.ico' in rec: # We do not care about this request
            continue
        if 'HTTP/1.1 404' in rec:
            if not_found_quota:
                not_found_quota -= 1
                continue
            else:
                raise Exception("Analysing HTTP traffic: Too many 404s")
        tokens = rec.split()
        method = tokens[7]
        timestamp = tokens[1]
        if method == 'GET':
            if req:
                raise Exception("Analysing HTTP traffic: Got two consecutive HTTP GETs")
            req = {'target': tokens[8], 'start': timestamp}
        elif '200 OK' in rec:
            # This is a reconstructed packet for the previous get request, record that
            req['end'] = timestamp
            downloads.append(req)
            req = {}

    return downloads


def get_client_connection_ports(pcap_path):
    client_ports = set()
    out = subprocess.run(f'tcpdump -n -r {pcap_path}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    records = out.stdout.decode().split('\n')

    server_records = [x for x in records if 'HTTP: GET ' in x and '.m4s'  in x]

    for rec in server_records:
        client_ports.add(get_port(rec, 0))
    
    return sorted(client_ports)

if __name__ == '__main__':
    # get_lost_packets('/vagrant/logs/tmp/server.pcap')
    # get_active_periods('/vagrant/logs/tmp/no_loss/sample/1/1_reno/server.pcap')
    get_client_connection_ports('/vagrant/logs/tmp/newcwv/newcwv_newcwvh2/server.pcap')