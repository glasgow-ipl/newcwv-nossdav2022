import os
from utils import check_and_create

def encode(meta, idx):
	resolutions = meta['resolutions']
	prefix = meta['prefix']
	source = meta['source']
	bitrates = meta['bitrates']
	framerate = meta['framerate']
	segment_duration_frames = meta['segment_duration']

	quality = resolutions[idx].split('x')[1]
	destination = ( prefix if prefix else '' ) + '%s/bbb_%s_%s.mp4' % (quality, quality, framerate)
	print ('dest: %s' % destination)
	dst_dir = destination.rsplit('/', 1)[0]
	if dst_dir:
		check_and_create(dst_dir)

	print("Segmenting video in " + str(segment_duration_frames / 60) + " second long chunks")

	print(segment_duration_frames, type(segment_duration_frames))
	cmd = "ffmpeg -i " + source + " -vf scale=" + resolutions[idx] + " -b:v " + str(bitrates[idx]) + "M -bufsize " + str(bitrates[idx]/2) + "M -c:v libx264 -x264opts 'keyint=" + str(segment_duration_frames) + ":min-keyint=" + str(segment_duration_frames) + ":no-scenecut' -c:a copy " + destination
	print("Encoding %s: " % cmd)
	os.system(cmd)

	print ('Done encoding %sp' % quality) 


# def main_encode():
# 	for i in range(len(resolutions)):
# 		print('Starting %s thread' % resolutions[i])
# 		t = Thread(target=encode, args=(i,))
# 		t.start()

# 	print ('Started all threads')