import os

#TODO: Should really make a use of a built-in xml library for this
def process_mpds(meta):
	resolutions = meta['resolutions']
	prefix = meta['prefix']
	media_prefix = meta['media_prefix']
	stiched_mpds = []	
	
	for i, resolution in enumerate(resolutions):
		width, height = resolution.split('x')
		#<Representation id="0" mimeType="video/mp4" codecs="avc1.64001f" bandwidth="1409668" width="640" height="360" frameRate="60/1">
		
		segment_dir = os.path.join(prefix, height, 'out')
		# Get the bandwidth, currently got no better way of doing this
		with open(os.path.join(segment_dir, 'output.mpd'), 'r') as f:
			content = f.read()
			bandwidth = content.split('bandwidth="')[1].split('"')[0]
			seg_duration = content.split('duration="')[1].split('"')[0]

		representation_tag = '\t'*3 + '<Representation id="%s" mimeType="video/mp4" codecs="avc1.64001f" bandwidth="%s" width="%s" height="%s" frameRate="60/1">\n' % (i, bandwidth, width, height)		
		stiched_mpds.append(representation_tag)
		print (representation_tag) 

		media_url = media_prefix if media_prefix else segment_dir

		media_url = os.path.join(media_url, height, 'out')

		files = sorted(os.listdir(segment_dir))
		
		# Duration should NOT be a hardcoded value!
		# Duration is the length of each individual segment duration (math.ciel(mediaPresentationDuration / # of segments))
		segmentlist_tag = '\t'*4 + ('<SegmentList timescale="1000000" duration="%s" startNumber="1">\n' % seg_duration)  
		stiched_mpds.append(segmentlist_tag)
		print (segmentlist_tag)

		initseg_tag = '\t'*5 + '<Initialization sourceURL="' + media_url + '/0-init.m4s" />\n'
		stiched_mpds.append(initseg_tag)		
		print (initseg_tag)

		
		for f in files:
			if f.startswith('0') and 'init' not in f: # if the file is video and is not the initial segment
				seg_path = os.path.join(media_url, f)
				segment_tag = '\t'*5 + '<SegmentURL media="' + seg_path + '" />\n'
				stiched_mpds.append(segment_tag)
				#print ()

#				print("%s/%s" % (segment_dir, f))
		# close segment_list tag
		stiched_mpds.append('\t'*4 + '</SegmentList>\n')
		# close representation tag
		stiched_mpds.append('\t'*3 + '</Representation>\n')
	
	# Make a string out of the stiched_mpds list
	stiched_mpds = ''.join(x for x in stiched_mpds)
	mpd_path = '%sbbb.mpd' % prefix
	with open(mpd_path, 'w') as f:
		# Put all tags prior to the <representation> tag in the mpd
		f.write('''<?xml version="1.0" encoding="utf-8"?>
<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="urn:mpeg:dash:schema:mpd:2011"
	xmlns:xlink="http://www.w3.org/1999/xlink"
	xsi:schemaLocation="urn:mpeg:DASH:schema:MPD:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd"
	profiles="urn:mpeg:dash:profile:isoff-live:2011"
	type="static"
	mediaPresentationDuration="PT10M34.5S"
	minBufferTime="PT10.0S">
	<ProgramInformation>
		<Title>Big Buck Bunny, Sunflower version</Title>
	</ProgramInformation>
	<Period id="0" start="PT0.0S">
		<AdaptationSet id="0" contentType="video" segmentAlignment="true" bitstreamSwitching="true" frameRate="60/1" lang="und">\n''') # opening tags

		f.write(stiched_mpds)

		f.write('\t'*2 + '''</AdaptationSet>
	</Period>
</MPD>''') # closing tags

	print('file saved to: %s' % mpd_path)
