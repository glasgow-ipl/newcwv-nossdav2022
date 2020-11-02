out_dir:=/vagrant/data
bbb_hd:=${out_dir}/bbb_sunflower_2160p_60fps_normal.mp4
root:=/vagrant

RUN_NUMBERS  = 1 2 3 4 5 6 7 8 9 10
CONG_ALGS = bbr cubic reno
NGINX_LOGS   = $(foreach alg, $(CONG_ALGS), $(foreach run, $(RUN_NUMBERS), ${root}/logs/$(run)_$(alg)/nginx_access.log))
OUTPUT_PLOTS = $(foreach alg, $(CONG_ALGS), $(foreach run, $(RUN_NUMBERS), ${root}/doc/$(run)_$(alg)/fig.pdf))

#setup
${bbb_hd}:
	@echo 'running setup'
	wget http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_2160p_60fps_normal.mp4 -P ${out_dir}
	@echo 'Video downloaded successfully'

# # # # # # #
# encoder   #
# # # # # # #


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


# # # # # # #
# Segmenter #
# # # # # # #


#segmenter 360
${out_dir}/360/out/output.mpd: ${out_dir}/360/bbb_360_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 360'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action segment --source ${bbb_hd} --extra_arg 640x360
	@echo 'Done segmenting'


#segmenter 480
${out_dir}/480/out/output.mpd: ${out_dir}/480/bbb_480_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 480'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action segment --source ${bbb_hd} --extra_arg 854x480
	@echo 'Done segmenting'


#segmenter 720
${out_dir}/720/out/output.mpd: ${out_dir}/720/bbb_720_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 720'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action segment --source ${bbb_hd} --extra_arg 1280x720
	@echo 'Done segmenting'


#segmenter 1080
${out_dir}/1080/out/output.mpd: ${out_dir}/1080/bbb_1080_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 1080'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action segment --source ${bbb_hd} --extra_arg 1920x1080
	@echo 'Done segmenting'

# # # # # # # # #
# MPD generator #
# # # # # # # # #


stage1-mpd: ${out_dir}/bbb.mpd
	@echo 'Generating mpd'


#MPD generator
${out_dir}/bbb.mpd: ${out_dir}/360/out/output.mpd ${out_dir}/480/out/output.mpd ${out_dir}/720/out/output.mpd ${out_dir}/1080/out/output.mpd ${root}/scripts/video_processing/video_driver.py ${root}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action mpd --source ${bbb_hd} --media_prefix ../data


stage2-test: ${root}/scripts/experiment_test.py
	@echo 'Running unit tests'
	cd ${root}/scripts && sudo python experiment_test.py


stage2-simulation: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd
	@echo 'Running simulation'
	cd ${root}/scripts && sudo python mn_script.py


${root}logs:
	@echo 'creating logs'
	mkdir $@


${root}/data:
	@echo 'Creating Data directory'
	mkdir $@


${root}/logs/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr


${root}/logs/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic


${root}/logs/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno

${root}/doc/%/fig.pdf: ${root}/logs/%/nginx_access.log ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6 | ${root}/doc
	@echo $@
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --source $(<D)


stage3-plot: ${OUTPUT_PLOTS}
	@echo 'Generating plots'


stage3-plot-all: ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6
	@echo 'plotting data'
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --all


${root}/doc:
	@echo 'Creating doc directory'
	mkdir $$@
	
