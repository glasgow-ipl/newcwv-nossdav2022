import csv
import functools
import numpy as np

quality_to_kbps_3s = {360: 1368193, 480: 3619359, 720: 6747721, 1080: 10660219}

def get_cwnds(access_log_path):
    ''' Returns a list of tuples containing unix timestamp and the measured CWND at that timestamp'''
    time_cwnd = []
    with open(access_log_path) as f:
        reader = csv.reader(f)
        for rec in reader:
            status = int(rec[3].strip())
            if status != 404: # ignore favicon request, as it usually comes from a different connection
                timestamp = float(rec[1].strip())
                cwnd = int(rec[6].strip()[1:-1])
                time_cwnd.append((timestamp, cwnd))
    
    return time_cwnd


def get_qualities(access_log_path):
    ''' Returns a list of tuples containing unix timestamp and the requested quality at that time e.g., 360, 480 etc'''
    time_quality = []
    with open(access_log_path) as f:
        skip = True
        reader = csv.reader(f)
        for rec in reader:
            if 'init' in rec[2]:
                skip = False
            if skip:
                continue
            quality = int(rec[2].split('/out')[0].split('/')[-1])
            timestamp = float(rec[1].strip())
            time_quality.append((timestamp, quality))

    return time_quality


def calculate_avg_bitrate(qualities, q_kbps_lookup):
    '''Calculates average bitrate, given a list of qualities and a lookup dictionary with quality -> kbps mapping'''
    q_kbps = [q_kbps_lookup[q] for q in qualities]
    return np.average(q_kbps)


def calculate_avg_oscillation(qualities, q_kbps_lookup):
    q_kbps = [q_kbps_lookup[q] for q in qualities]
    avg_osc = functools.reduce(lambda i, j: abs(i - j), q_kbps) / (len(q_kbps_lookup) - 1)
    return avg_osc


if __name__ == '__main__':
    # get_cwnds('/vagrant/logs/tmp/no_loss/sample/1/1_reno/nginx_access.log')
    qualities = get_qualities('/vagrant/logs/tmp/no_loss/sample/1/1_reno/nginx_access.log')
    qualities = np.array(qualities)
    qualities = qualities[:,1]
    print(f'{calculate_avg_bitrate(qualities, quality_to_kbps_3s):.4f}')
    print(f'{calculate_avg_oscillation(qualities, quality_to_kbps_3s):.4f}')
