import csv
import functools
import numpy as np
import constants


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
    quality_dic = {}

    with open(access_log_path) as f:
        skip = True
        reader = csv.reader(f)
        for rec in reader:
            if 'init' in rec[2]:
                skip = False
            if skip:
                continue
            if 'favicon.ico' in rec[2]:
                continue # in case favico request comes after video has started being downloaded
            quality = int(rec[2].split('/out')[0].split('/')[-1])
            chunk = rec[2].split('/out')[1].split('-')[1].split('.')[0]
            timestamp = float(rec[1].strip())

            if chunk == 'init':
                continue
            else:
                # Ensures that if a follow-up request for the same chunk is made, we will record that
                quality_dic[int(chunk)] = (timestamp, quality)


    time_quality = [value for _key, value in sorted(quality_dic.items())]

    return time_quality


def calculate_avg_bitrate(qualities, q_kbps_lookup):
    '''Calculates average bitrate, given a list of qualities and a lookup dictionary with quality -> kbps mapping'''
    q_kbps = [q_kbps_lookup[q] for q in qualities]
    return np.average(q_kbps)


def calculate_avg_oscillation(qualities, q_kbps_lookup):
    q_kbps = [q_kbps_lookup[q] for q in qualities]
    avg_osc = functools.reduce(lambda i, j: abs(i - j), q_kbps) / (len(q_kbps) - 1)
    return avg_osc


if __name__ == '__main__':
    # get_cwnds('/vagrant/logs/tmp/no_loss/sample/1/1_reno/nginx_access.log')
    qualities = get_qualities('/vagrant/logs/tmp/no_loss/sample/1/1_reno/nginx_access.log')
    qualities = np.array(qualities)
    qualities = qualities[:,1]
    print(f'{calculate_avg_bitrate(qualities, constants.QUALITY_TO_BPS_3S) / 1000:.3f}')
    print(f'{calculate_avg_oscillation(qualities, constants.QUALITY_TO_BPS_3S) / 1000:.3f}')
