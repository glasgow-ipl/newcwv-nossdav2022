import os

# Force matplotlib to not use Xserver if there is no such
if not os.environ.get('DISPLAY'):
	import matplotlib
	matplotlib.use('Agg')
	
import matplotlib.pyplot as plt

# Current file format:
#
# time,quality,chunk_no
# app_limited: x, RCV_SSTRESH: y, SND_SSTRESH: z, SND_CWND: a, CPU_LOAD: b

def parse_tcpinfo(line):
	pass

def parse_videoinfo(line):
	print line
	time, quality, chunk = line.split(',')
	return int(float(time)), int(quality), int(chunk)


def parse_file(fname):
	times = []
	bandwidths = []
	chunks = []
	with open(fname) as f:
		for i, line in enumerate(f):
			if not line.strip():
				continue
			if i % 2 == 1:
				parse_tcpinfo(line)
			else:
				print "line", line
				time, quality, chunk = parse_videoinfo(line)
				times += [time]
				i = resolutions.index(str(quality))
				bandwidth = bitrates[i] * 10**5
				bandwidths += [bandwidth]
#				qualities += [quality]
				chunks += [chunk]

				if int(chunk) == 100:
					break

	return times, bandwidths, chunks


'''
plt.plot(times, chunks, 'r', label='reno')
times, chunks = parse_times('cubic.out')
#print times, chunks
plt.plot(times, chunks, 'b', label='cubic')
plt.xlabel('time')
plt.ylabel('DASH chunk')
plt.legend()
'''

import sys
import getopt

available_bitrates = [86000, 156000, 281000, 437000, 5*10**5, 827000, 1*10**6]  #+ [1604000]

bandwidth_limits = [(0, 1*10**6), (80, 1*10**6), (80, .5*10**6), (140, .5*10**6), (140, 1*10**6), (200, 1*10**6)]

bw_l = [(0, 1000000), (200, 1000000)]

resolutions=['360', '480', '720', '1080']#, '2560x1440']
bitrates=[1.5, 4, 7.5, 12]#, 24]

def main():
	opts, _ = getopt.getopt(sys.argv[1:], "", ['fname=', 'save', 'noshow', 'out='])
	opts_d = {k:v for (k,v) in opts}

	print opts_d

	show = not ('--noshow' in opts_d)
	save = '--save' in opts_d
	data_file = opts_d['--fname'] if '--fname' in opts_d else 'cubic_1_half_1.out2'	
	out_file = optd_d['--out'] if '--out' in opts_d else 'plot.out'	

	times, qualities, chunks = parse_file(data_file)


	fig, ax1= plt.subplots()

	#ax1.plot(times, chunks, 'r', label='chunk #')
	ax1.set_xlabel('time')
	ax1.set_ylabel('cwnd')

	ax2 = ax1.twinx()

	print times, qualities
	ax2.plot(times, qualities, 'b', marker='o', label='requested bit-rate')
	ax2.set_yticks(available_bitrates)
	ax2.set_ylabel('bit-rate')

	limit_opts = {'color': 'green', 'ls': '--', 'lw': 1, 'label': 'bandwidth limit'}

	ax2.axhline(1*10**6, xmax=.4, **limit_opts)
	ax2.axhline(.5*10**6, xmin=.4, xmax=.7, **limit_opts)
	ax2.axhline(1*10**6, xmin=.7, xmax=1, **limit_opts)

	#ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	#plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	fig.legend(bbox_to_anchor=(0.5, 1), loc='upper center', ncol=3)	
	fig.tight_layout()

	print("save %s" % save)

	if show:
		plt.show()
	if save:
		print 'saving'	
		plt.savefig('results/DASH_CC_effect.pdf', bbox_inches='tight')

if __name__ == '__main__':
	main()

