import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from parse_dash_log import get_throughput_estimates

def process_outliers():
    for run_num in range(1, 8):
        sim_name = f'{run_num}_newcwv'
        print(sim_name)
        dash_log = os.path.join('/', 'vagrant', 'logs', 'newcwv', 'DSL', sim_name, 'dashjs_metrics.json')
        estimates = get_throughput_estimates(dash_log)
        (_, precise), (_, safe_dic) = estimates.items()

        safe_dic = [(i, k, v / 1000) for i, (k, v) in enumerate(safe_dic.items()) if v / 1000 < 4]
        print(safe_dic)

def foo():
    links = [ 'FTTP']
    algs = ['vreno', 'newcwv']
    runs = range(1,10)
    root = '/vagrant/logs/newcwv/test2'
    for i, link in enumerate(links):
        stats = {}
        for alg in algs:
            print(alg)
            bandwidth_aggr = []
            for run in runs:
                metrics_path = os.path.join(root, link, f'{run}_{alg}', 'dashjs_metrics.json')
                bandwidth = get_throughput_estimates(metrics_path)['precise']

                (_time, values) = zip(*bandwidth.items())

                #####
                values = [x[0] for x in values]
                #########

                print(f'{run}_{alg}')
                print(max(values))
                # bandwidth_mbps = [v[0] / 1000 for v in values]
                # bandwidth_aggr += bandwidth_mbps

def verify_bandwidth():
    import subprocess
    import json

    out = subprocess.run('tshark  -t a -Y http -T json -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.seq -e tcp.ack -e tcp.len -e http.request.uri -e http.response.code -e http.content_length -r /vagrant/logs/newcwv/test2/FTTP/5_vreno/client.pcap > tmp.json', shell=True, stdout=subprocess.PIPE)
    print('done processing')
    print(out.stdout)

    with open('tmp.json') as f:
        j = json.load(f)

    current_seq = 1
    target_seq = 1

    byte_size = 0
    receive = False
    send_ts = None

    req_resp = {}

    for item in j:
        content = item['_source']['layers']
        # print(content)
        # print(current_seq)
        if 'http.request.uri' in content:
            key = content['http.request.uri'][0]
        if 'http.response.code' in content:
            if int(content['http.response.code'][0]) != 200:
                key = None # This request was unsuccessful
            else:
                current_seq = int(content['tcp.seq'][0])
                byte_size = int(content['http.content_length'][0])
                send_ts = float(content['frame.time_relative'][0])
                target_seq = current_seq + byte_size
                receive = True
        if receive and content['ip.src'][0] == '10.0.0.1':
            current_seq += int(content['tcp.len'][0])
            if current_seq > target_seq:
                print(f'{key} received in frame {content["frame.number"][0]}')
                if not key or 'init.m4s' in key:
                    continue # Dashjs ignores these and sometimes they are delivered too fast causing a time of 0
                transfer_time = float(content['frame.time_relative'][0]) - send_ts
                req_resp[key] = {'bytes': byte_size, 'transfer_time': transfer_time, 'estimated_bandwidth': (byte_size * 8 / transfer_time) / 1_000_000}

    import pprint
    pprint.pprint(req_resp)

if __name__ == '__main__':
    # process_outliers()
    foo()
    # verify_bandwidth()