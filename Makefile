out_dir:=/vagrant/data
bbb_hd:=${out_dir}/bbb_sunflower_2160p_60fps_normal.mp4
root:=/vagrant

BW_SETTINGS := $(shell seq 1 117)

BW_RUNS = $(foreach bw_set, $(BW_SETTINGS), ${root}/logs/bw_cubic_${bw_set}/nginx_access.log)

NETWORK_PROFILES = 1 2 3 4 5 6 7 8 9 10 11 12

RUN_NUMBERS  = 1 2 3 4 5 6 7 8 9 10
CONG_ALGS = bbr cubic reno
NGINX_LOGS   = $(foreach alg, $(CONG_ALGS), $(foreach profile, $(NETWORK_PROFILES), $(foreach run, $(RUN_NUMBERS), ${root}/logs/$(profile)/$(run)_$(alg)/nginx_access.log)))
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
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action encode --source ${bbb_hd} --extra_arg 0 --segment_duration 1
	@echo 'Encoder executed'


#encoder 480
${out_dir}/480/bbb_480_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 480 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action encode --source ${bbb_hd} --extra_arg 1 --segment_duration 1
	@echo 'Encoder executed'


#encoder 720
${out_dir}/720/bbb_720_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 720 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action encode --source ${bbb_hd} --extra_arg 2 --segment_duration 1
	@echo 'Encoder executed'


#encoder 1080
${out_dir}/1080/bbb_1080_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 1080 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action encode --source ${bbb_hd} --extra_arg 3 --segment_duration 1
	@echo 'Encoder executed'


#encoder 360 DASH-IF
${out_dir}/dash-if/360/bbb_360_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 360 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action encode --source ${bbb_hd} --extra_arg 0 --segment_duration 3 --use_yt_bitrates False
	@echo 'Encoder executed'


#encoder 480 DASH-IF
${out_dir}/dash-if/480/bbb_480_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 480 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action encode --source ${bbb_hd} --extra_arg 1 --segment_duration 3 --use_yt_bitrates False
	@echo 'Encoder executed'


#encoder 720 DASH-IF
${out_dir}/dash-if/720/bbb_720_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 720 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action encode --source ${bbb_hd} --extra_arg 2 --segment_duration 3 --use_yt_bitrates False
	@echo 'Encoder executed'


#encoder 1080 DASH-IF
${out_dir}/dash-if/1080/bbb_1080_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 1080 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action encode --source ${bbb_hd} --extra_arg 3 --segment_duration 3 --use_yt_bitrates False
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


#segmenter 360 DASH-IF
${out_dir}/dash-if/360/out/output.mpd: ${out_dir}/dash-if/360/bbb_360_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 360'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action segment --source ${bbb_hd} --extra_arg 640x360
	@echo 'Done segmenting'


#segmenter 480 DASH-IF
${out_dir}/dash-if/480/out/output.mpd: ${out_dir}/dash-if/480/bbb_480_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 480'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action segment --source ${bbb_hd} --extra_arg 854x480
	@echo 'Done segmenting'


#segmenter 720 DASH-IF
${out_dir}/dash-if/720/out/output.mpd: ${out_dir}/dash-if/720/bbb_720_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 720'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action segment --source ${bbb_hd} --extra_arg 1280x720
	@echo 'Done segmenting'


#segmenter 1080 DASH-IF
${out_dir}/dash-if/1080/out/output.mpd: ${out_dir}/dash-if/1080/bbb_1080_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 1080'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action segment --source ${bbb_hd} --extra_arg 1920x1080
	@echo 'Done segmenting'
	
# # # # # # # # #
# MPD generator #
# # # # # # # # #


stage1-mpd: ${out_dir}/bbb.mpd
	@echo 'Generating mpd'

stage1-dash-if-mpd: ${out_dir}/dash-if/bbb.mpd
	@echo 'Generating dash-if MPD'


#MPD generator
${out_dir}/bbb.mpd: ${out_dir}/360/out/output.mpd ${out_dir}/480/out/output.mpd ${out_dir}/720/out/output.mpd ${out_dir}/1080/out/output.mpd ${root}/scripts/video_processing/video_driver.py ${root}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action mpd --source ${bbb_hd} --media_prefix ../data

#MPD generator
${out_dir}/dash-if/bbb.mpd: ${out_dir}/dash-if/360/out/output.mpd ${out_dir}/dash-if/480/out/output.mpd ${out_dir}/dash-if/720/out/output.mpd ${out_dir}/dash-if/1080/out/output.mpd ${root}/scripts/video_processing/video_driver.py ${root}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action mpd --source ${bbb_hd} --media_prefix ../data/dash-if


stage2-test: ${root}/scripts/experiment_test.py
	@echo 'Running unit tests'
	cd ${root}/scripts && sudo python experiment_test.py


stage2-simulation: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd
	@echo 'Running simulation'
	cd ${root}/scripts && sudo python mn_script.py


${root}/logs:
	@echo 'creating logs'
	mkdir $@


${root}/data:
	@echo 'Creating Data directory'
	mkdir $@


${root}/logs/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_1.json


${root}/logs/1/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_1.json

${root}/logs/2/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_2.json

${root}/logs/3/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_3.json

${root}/logs/4/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_4.json

${root}/logs/5/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_5.json

${root}/logs/6/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_6.json

${root}/logs/7/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_7.json

${root}/logs/8/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_8.json

${root}/logs/9/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_9.json

${root}/logs/10/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_10.json

${root}/logs/11/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_11.json

${root}/logs/12/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_12.json


${root}/logs/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_1.json


${root}/logs/1/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_1.json

${root}/logs/2/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_2.json

${root}/logs/3/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_3.json

${root}/logs/4/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_4.json

${root}/logs/5/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_5.json

${root}/logs/6/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_6.json

${root}/logs/7/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_7.json

${root}/logs/8/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_8.json

${root}/logs/9/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_9.json

${root}/logs/10/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_10.json

${root}/logs/11/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_11.json

${root}/logs/12/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_12.json


${root}/logs/1/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_1.json

${root}/logs/2/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_2.json

${root}/logs/3/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_3.json

${root}/logs/4/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_4.json

${root}/logs/5/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_5.json

${root}/logs/6/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_6.json

${root}/logs/7/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_7.json

${root}/logs/8/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_8.json

${root}/logs/9/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_9.json

${root}/logs/10/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_10.json

${root}/logs/11/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_11.json

${root}/logs/12/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_12.json



${root}/logs/bw_cubic_%/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	#cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/scripts/bws/network_config_${*}.json


${root}/doc/%/fig.pdf: ${root}/logs/%/nginx_access.log ${root}/scripts/net_utils.py | ${root}/doc
	@echo $@
	python3 /vagrant/scripts/net_utils.py --source $(<D)

stage3-run: ${NGINX_LOGS}
	@echo 'Running experiments'

stage3-diff_bw: ${BW_RUNS}
	@echo ${BW_RUNS}

stage3-plot: ${OUTPUT_PLOTS}
	@echo 'Generating plots'


stage3-plot-all: ${root}/scripts/net_utils.py
	@echo 'plotting data'
	python3 /vagrant/scripts/net_utils.py --all


${root}/doc:
	@echo 'Creating doc directory'
	mkdir $@

test:
	@echo $(NGINX_LOGS)
