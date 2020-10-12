import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
import os
import datetime
import csv
import sys
import numpy as np

root = os.path.join('/', 'vagrant')

def plot():
    log_root = os.path.join(root, 'logs')
    for path, dirs, files in os.walk(log_root):
        if all(x in files for x in ['events.log', 'nginx_access.log']):
            # Parse events log
            bw_change_times = []
            with open(os.path.join(path, 'events.log')) as f:
                    for line in f:
                        if 'changing BW' in line:
                            bw_change_times.append(datetime.datetime.strptime(line.split()[-1], "%m-%d-%H:%M:%S:%f"))

            with open(os.path.join(path, 'nginx_access.log')) as f:
                csv_reader = csv.reader(f)
                
                # Check nginx conf for access_log explaination
                plot_info = []
                init_time = None
                for time, request, status, rtt, rtt_var, cwnd,  _, _, _, _ in csv_reader:
                    if 'out' not in request:
                        continue
                    date_obj = datetime.datetime.strptime(time, "%d/%b/%Y:%H:%M:%S %z")
                    if not init_time:
                        init_time = date_obj
                    request = request.split()[1]
                    quality = request.split('/')[2]
                    chunk = request.split('/')[4][2:-4]
                    plot_info.append((int((date_obj - init_time).total_seconds()), str(quality)))
                    # print(init_time, date_obj, request, quality, chunk)

                plot_info = np.array(plot_info)
                # print(plot_info[:,0][-5:], plot_info[:,1][-5:])
                plt.scatter(plot_info[:,0], plot_info[:,1])
                for change_time in bw_change_times:
                    change_time = change_time.replace(year=init_time.year, month=init_time.month, day=init_time.day)
                    # print(datetime.datetime.strftime(init_time))
                    secs = (change_time - init_time.replace(tzinfo=None)).total_seconds()
                    print(secs)
                    plt.axvline(secs)

                # print(plot_info[:,0][-1])
                N = len(plot_info[:,0])
                print (N)
                plt.gca().margins(x=0)
                plt.gcf().canvas.draw()
                tl = plt.gca().get_xticklabels()
                maxsize = max([t.get_window_extent().width for t in tl])
                m = 0.02 # inch margin
                s = maxsize/plt.gcf().dpi*N+2*m
                margin = m/plt.gcf().get_size_inches()[0]

                plt.gcf().subplots_adjust(left=margin, right=1.-margin)
                plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])


                plt.savefig('fig.png')
                sys.exit(1)
            
            # print(type(f))
            # Parse access log

            # Plot

def big_xaxis():
    fig, ax = plt.subplots()

    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))

    # For the minor ticks, use no labels; default NullFormatter.
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.xlim(right=630)

    print(fig.get_size_inches())
    fig.set_size_inches((50, 5))
    # plt.figure(figsize=(100,100))
    plt.savefig('fig.png')

if __name__ == '__main__':
    # plot()
    big_xaxis()