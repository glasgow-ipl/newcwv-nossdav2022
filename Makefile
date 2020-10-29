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

#encoder 360
${out_dir}/360/bbb_360_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 360 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action encode --source ${bbb_hd} --extra_arg 0
	@echo 'Encoder executed'

#encoder 480
${out_dir}/480/bbb_480_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 480 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action encode --source ${bbb_hd} --extra_arg 1
	@echo 'Encoder executed'

#encoder 720
${out_dir}/720/bbb_720_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 720 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action encode --source ${bbb_hd} --extra_arg 2
	@echo 'Encoder executed'

#encoder 1080
${out_dir}/1080/bbb_1080_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 1080 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action encode --source ${bbb_hd} --extra_arg 3
	@echo 'Encoder executed'


#segmenter 360
${out_dir}/360/out/output.mpd: ${out_dir}/360/bbb_360_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'truncating 360'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action segment --source ${bbb_hd} --extra_arg 640x360
	@echo 'Qualities truncated'

#segmenter 480
${out_dir}/480/out/output.mpd: ${out_dir}/480/bbb_480_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'truncating 480'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action segment --source ${bbb_hd} --extra_arg 854x480
	@echo 'Qualities truncated'

#segmenter 720
${out_dir}/720/out/output.mpd: ${out_dir)/720/bbb_720_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'truncating 720'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action segment --source ${bbb_hd} --extra_arg 1280x720
	@echo 'Qualities truncated'

#segmenter 1080
${out_dir}/1080/out/output.mpd: ${out_dir}/1080/bbb_1080_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'truncating 1080'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action segment --source ${bbb_hd} --extra_arg 1920x1080
	@echo 'Qualities truncated'

stage1-mpd: ${out_dir}/bbb.mpd
	@echo 'Generating mpd'

#MPD generator
${out_dir}/bbb.mpd: ${out_dir}/360/out/output.mpd ${out_dir}/480/out/output.mpd ${out_dir}/720/out/output.mpd ${out_dir}/1080/out/output.mpd ${root}/scripts/video_processing/video_driver.py ${root}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action mpd --source ${bbb_hd} --media_prefix ../data

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
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --all

doc:
	@echo 'Creating doc directory'
	mkdir $@
	
