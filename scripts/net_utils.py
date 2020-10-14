import csv
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
import numpy as np

def count_oscillations(values): # returns the number of oscillations in the value list (cwnd)
    changes = 0
    if(len(values) < 2):
        return 0
    direction = int(values[1] > values[0]) # 1 - increasing, 0 - decreasing
     
    for idx in range(1, len(values) - 1):
        if direction:
            if values[idx][1] > values[idx + 1][1]:
                direction = not direction
                changes += 1
                print(values[idx][1], values[idx+1][1])
        else:
            if values[idx][1] < values[idx + 1][1]:
                direction = not direction
                changes += 1
                print(values[idx][1], values[idx+1][1])
        
    return changes


def plot_cwnd(cwnd_info, bw_changes):
    cwnd_info = np.array(cwnd_info)#, dtype=np.dtype('float64,int'))
    # time = 
    time = cwnd_info[:,0]
    cwnd = cwnd_info[:,1]

    fig, ax = plt.subplots()

    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))

    # For the minor ticks, use no labels; default NullFormatter.
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.xlim(right=max(time) + 5)

    plt.plot(time, cwnd)

    fig.set_size_inches((35, 5))
    plt.xticks(rotation=45)
    # plt.figure(figsize=(100,100))
    plt.savefig('fig2.png')

def get_cwnd(log_path):
    cwnd_time = []
    with open(log_path) as f:
        reader = csv.reader(f)
        # find the first video segment requested and treat it as start of time
        while True:
            rec = reader.__next__()
            if 'init' in rec[2]:
                time_init = float(rec[1])
                time_init = datetime.datetime.utcfromtimestamp(time_init)
                ms_delta = (time_init - time_init).total_seconds()
                cwnd = rec[6].strip()
                cwnd = int(cwnd[1:-1])
                cwnd_time.append((ms_delta, cwnd))
                break

        for line in reader:
            current_time = float(line[1])
            current_time = datetime.datetime.utcfromtimestamp(current_time)
            ms_delta = (current_time - time_init).total_seconds()
            cwnd = line[6].strip()
            cwnd = int(cwnd[1:-1]) # Remove the "" from the begining and the end of the cwnd value
            cwnd_time.append((ms_delta, cwnd))
    
    return cwnd_time

if __name__ == '__main__':
    cwnds = get_cwnd('/vagrant/logs/10-12-1307/nginx_access.log')
    print(len(cwnds))
    print(cwnds)
    print(count_oscillations(cwnds))
    plot_cwnd(cwnds)