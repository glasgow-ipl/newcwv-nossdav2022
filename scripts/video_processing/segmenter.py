import os
from utils import check_and_create

def _segment(in_source, dst_dir):
	print('in:%s out:%s' % (in_source, dst_dir))
	os.system("ffmpeg -i " + in_source + " -codec copy -f dash -min_seg_duration 30 -use_template 0 -use_timeline 0 -init_seg_name '$RepresentationID$-init.m4s' -media_seg_name '$RepresentationID$-$Number%05d$.m4s' " + dst_dir + "/output.mpd")


def main_segment(meta, resolution):
	prefix = meta['prefix']
	framerate = meta['framerate']

	quality = resolution.split('x')[1]
	#dst = res + '/out'
	in_source = ('%s%s/bbb_%s_%s.mp4' % (prefix, quality, quality, framerate) )				
	check_and_create('%s%s/out' % (prefix, quality) )
	out_dir = '%s%s/out' % (prefix, quality)
	_segment(in_source, out_dir)