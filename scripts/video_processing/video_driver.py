from threading import Thread
import os
import time
import sys
import argparse

from mpd_generator import process_mpds
from encoder import encode
from segmenter import main_segment

# ffmpeg -i ../bbb_fragmented.mp4 -vf scale=%s -b:v %sM -bufsize %sM -c:v libx264 -x264opts 'keyint=30:min-keyint=30:no-scenecut' -crf 0 -preset veryslow -c:a copy %s/bbb_%s_%s.mp4

# ffmpeg -i bbb_360_60.mp4 -codec copy -f dash -use_template 0 -min_seg_duration 30 -use_timeline 0 -init_seg_name '$RepresentationID$-init.m4s' -media_seg_name '$RepresentationID$-$Time$.m4s' out/output.mpd

# The 2nd command would chunk the file into m4s segments, where each starts with an I-frame. Size of segments is not consistent!
# the -min_seg_duration flag, forces segments to be split on every I-frame. The intention of this flag is NOT this and it is DEPRECATED! read more on this

resolutions=['640x360', '854x480', '1280x720', '1920x1080']#, '2560x1440']
bitrates=[1.5, 4, 7.5, 12]#, 24]

source = 'bbb_sunflower_2160p_60fps_normal.mp4'
prefix = '/vagrant/'
framerate = 60
media_prefix = None

def check_and_create(dir_path):
	print ("Checking: %s" % dir_path)
	if not os.path.isdir(dir_path):
		print ('Destination directory: %s does not exist, creating one' % dir_path)
		os.mkdir(dir_path)
	else:
		print ('Found directory: %s ' % dir_path)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Video utility script')
	parser.add_argument('--prefix', '-p', help='Prefix')

	parser.add_argument('--source', '-s', help='Mp4 video source')

	parser.add_argument('--fps', help="Frames per second to use for re-encoding")

	parser.add_argument('--media_prefix', help='prefix to be used for media segments path')

	parser.add_argument('--action', required=True, help='Action to be performed by the script. Possible actions are: encode, segment, and mpd (to generate an MPD file)')

	parser.add_argument('--extra_arg', help="Additional arguments to pass for encoder and segmenter actions to pick the correct representation")

	args = parser.parse_args()
	
	if args.prefix:
		if not args.prefix.endswith('/'):
			prefix = args.prefix + '/'
		else:
			prefix = args.prefix
	else:
		print ("No prefix given")
	if args.source:
		source = args.source 
	if args.fps:
		framerate = args.fps
	if args.media_prefix:
		media_prefix = args.media_prefix

	meta = {}
	meta['media_prefix'] = media_prefix
	meta['framerate'] = framerate
	meta['source'] = source
	meta['bitrates'] = bitrates
	meta['resolutions'] = resolutions
	meta['prefix'] = prefix

	print ('Running "%s" script with arguemnts: prefix(%s) source(%s) fps(%s)' % (args.action, prefix, source, framerate))
	if args.action == 'segment':
		if not args.extra_arg:
			print("Segment action requires an extra srgument to pick representation")
			sys.exit(1)

		resolution = args.extra_arg
		main_segment(meta, resolution)

	elif args.action == 'encode':
		if not args.extra_arg:
			print("Segment action requires an extra srgument to pick representation")
			sys.exit(1)

		idx = args.extra_arg
		idx = int(idx)
		print(f"Encoding {resolutions[idx]}")
		encode(meta, idx)
		print(f"Done encoding {resolutions[idx]}")
	
	elif args.action == 'mpd':
		process_mpds(meta)
	else:
		print("Unknown action requested. Specify one of: segment, encode, or mpd")

