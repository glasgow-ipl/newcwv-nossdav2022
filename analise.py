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
	qualities = []
	chunks = []
	with open(fname) as f:
		for i, line in enumerate(f):
			if not line.strip():
				continue
			if i % 2 == 0:
				parse_tcpinfo(line)
			else:
				print "line", line
				time, quality, chunk = parse_videoinfo(line)
				times += [time]
				qualities += [quality]
				chunks += [chunk]

				if int(chunk) == 100:
					break

	return times, qualities, chunks


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

def main():

	opts, _ = getopt.getopt(sys.argv[1:], "", ['fname=', 'save', 'noshow', 'out='])
	opts_d = {k:v for (k,v) in opts}

	print opts_d

	show = not ('--noshow' in opts_d)
	save = '--save' in opts_d
	data_file = opts_d['--fname'] if '--fname' in opts_d else 'cubic_1_half_1.out2'	
	out_file = optd_d['--out'] if '--out' in opts_d else 'plot.out'	

	times, qualities, chunks = parse_file(data_file)


	fig, ax1 = plt.subplots()

	ax1.plot(times, chunks, 'r')

	ax2 = ax1.twinx()

	ax2.plot(times, qualities, 'b')

	fig.tight_layout()

	if show:
		plt.show()
	if save:	
		plt.savefig('DASH_CC_effect.pdf')

if __name__ == '__main__':
	main()

