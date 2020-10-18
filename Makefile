out_dir:=/vagrant/data
bbb_hd:=${out_dir}/bbb_sunflower_2160p_60fps_normal.mp4
root:=/vagrant

#experiment: bbb_sunflower_2160p_60fps_normal.mp4
#	@echo 'starting experiment'

#setup
${bbb_hd}:
	@echo 'running setup'
	wget http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_2160p_60fps_normal.mp4 -P ${out_dir}
	@echo 'Video downloaded successfully'

#encoder
${out_dir}/360/bbb_360_60.mp4 ${out_dir}/480/bbb_480_60.mp4 ${out_dir}/720/bbb_720_60.mp4 ${out_dir}/1080/bbb_1080_60.mp4: ${bbb_hd}
	@echo 'running encoder'
	python encoder.py --prefix ${out_dir} --action encode --source ${bbb_hd}
	@echo 'Encoder executed'

#segmenter
${out_dir}/360/out/output.mpd ${out_dir}/480/out/output.mpd ${out_dir}/720/out/output.mpd ${out_dir}/1080/out/output.mpd: ${out_dir}/360/bbb_360_60.mp4 ${out_dir}/480/bbb_480_60.mp4 ${out_dir)/720/bbb_720_60.mp4 ${out_dir}/1080/bbb_1080_60.mp4 
	@echo 'truncating'
	python encoder.py --prefix ${out_dir} --action truncate --source ${bbb_hd}
	@echo 'Qualities truncated'

stage1-mpd: ${out_dir}/bbb.mpd data
	@echo 'Generating mpd'


#MPD generator
${out_dir}/bbb.mpd: ${out_dir}/360/out/output.mpd ${out_dir}/480/out/output.mpd ${out_dir}/720/out/output.mpd ${out_dir}/1080/out/output.mpd
	@echo 'stitching mpds'
	python encoder.py --prefix ${out_dir} --action mpd --source ${bbb_hd}

stage2-test: ${root}/scripts/experiment_test.py
	@echo 'Running unit tests'
	cd ${root}/scripts && sudo python experiment_test.py

stage2-simulation: ${root}/scripts/mn_script.py logs
	@echo 'Running simulation'
	cd ${root}/scripts && sudo python mn_script.py

logs:
	@echo 'creating logs'
	mkdir $@

data:
	@echo 'Creating Data directory'
	mkdir $@

stage3-plot: ${root}/scripts/net_utils.py doc
	@echo 'plotting data'
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py

doc:
	@echo 'Creating doc directory'
	mkdir $@
	