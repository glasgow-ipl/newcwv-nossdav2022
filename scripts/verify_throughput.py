import math
import json
from pprint import pprint
import subprocess
import sys

import datetime


def main():
    estimates = {}

    try:
        with open('/vagrant/logs/tmp/pd.txt') as f:
            lines = f.readlines()

            for i, line in enumerate(lines):
                line = line.strip()
                if 'Content-Length' in line:
                    line = line.replace('\\r', '').replace('\\n', '')
                    content_length = int(line.split(': ')[1])
                    # print(lines[i + 7])
                    time = float(lines[i + 7].strip().split(": ")[1].split()[0])
                    # print(lines[i + 13])
                    uri = lines[i + 13].strip()[len('request uri: '):-1]
                    uri = uri.strip()
                    tput = round(content_length * 8 / (time * 1000))
                    print (uri, time, content_length, tput)
                    estimates[uri] = { 'local': [time, content_length, tput], 'remote': ''}
    except:
        pass

    # print(estimates)

    with open('/vagrant/logs/tmp/dashjs_estimates.json') as f:
        estimates_remote = json.load(f)

        for estimate in estimates_remote['estimates']:
            uri = estimate.split('for: ')[1].split(' is')[0]
            if '635.m4s' in uri:
                continue
            # print(list(estimates.keys())[:10])
            # print(uri)
            # print(uri in estimates)
            time, length, tput = estimate.split('is ')[1].split()
            estimates[uri]['remote'] = [time, length, tput]

    # for k in list(estimates.items())[:10]:
    #     print(k)

    with open('/vagrant/logs/tmp/result.json', 'w') as f:
        json.dump(estimates, f)


def calculate_throughput(server_pcap_loc, init_time=None, interval=1):
    res = subprocess.run(f'tcpdump -n -r {server_pcap_loc}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    records = res.stdout.decode().split('\n')

    server_records = [x for x in records if '10.0.0.1.80 > ' in x and 'length 0' not in x]

    fmt = '%H:%M:%S.%f'

    tput = {}

    if not init_time:
        print("Warning, no initial time set to calculate tput")
        sys.exit(1)
    # init_time = datetime.datetime.strptime(init_time, fmt)

    for rec in server_records:
        timestmp = rec.split(' ', 1)[0]
        data_len = int(rec.split('length ')[1].split(':')[0])
        data_len *= 8 # Make data in bits
        data_len = data_len / interval # Make data in units per interval
        tput_delta = (datetime.datetime.strptime(timestmp, fmt) - init_time).total_seconds()
        tput_key = tput_delta / interval
        tput_key = int(tput_key) # remove fractional part
        tput_key += 1
        transferred = tput.get(tput_key, 0)
        tput[tput_key] = transferred + data_len

    # tput = {k: v*8 for k, v in tput.items()} # Make throughput in bits per second

    # loss_deltas = [(datetime.datetime.strptime(x, fmt) - init_time).total_seconds()

    return tput

if __name__ == '__main__':
    # main()
    calculate_throughput('/vagrant/logs/clients/2/DSL/1_newcwv/server.pcap')
