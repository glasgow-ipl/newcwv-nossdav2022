import csv


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

if __name__ == '__main__':
    get_cwnds('/vagrant/logs/tmp/no_loss/sample/nginx_access.log')