import json


def get_cwnd(fpath):
    cwnd = []
    with open(fpath) as f:
        iperf_json = json.load(f)

    for stream_info in iperf_json['intervals']:
        stream_info = stream_info['streams'][0]
        cwnd.append(int(stream_info['snd_cwnd']))

    return cwnd

if __name__ == '__main__':
    get_cwnd('/vagrant/logs/10-12-1307/')
