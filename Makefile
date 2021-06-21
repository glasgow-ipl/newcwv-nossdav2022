out_dir:=/vagrant/data
bbb_hd:=${out_dir}/bbb_sunflower_2160p_60fps_normal.mp4
bbb_360=${out_dir}/
root:=/vagrant

DASH_ALG='abrDynamic'
MPD_LOCATION='data/dash-if/bbb.mpd'

BW_SETTINGS := $(shell seq 1 117)

BW_RUNS = $(foreach bw_set, $(BW_SETTINGS), ${root}/logs/bw_cubic_${bw_set}/nginx_access.log)

ABR_ALGS = abrThroughput abrDynamic abrBola

NETWORK_PROFILES = 1 2 3 4 5 6 7 8 9 10 11 12

RUN_NUMBERS  = 1 2 3 4 5 6 7 8 9 10
CONG_ALGS = bbr cubic reno
NGINX_LOGS   = $(foreach alg, $(CONG_ALGS), $(foreach profile, $(NETWORK_PROFILES), $(foreach run, $(RUN_NUMBERS), ${root}/logs/$(profile)/$(run)_$(alg)/nginx_access.log)))
OUTPUT_PLOTS = $(foreach alg, $(CONG_ALGS), $(foreach run, $(RUN_NUMBERS), ${root}/doc/$(run)_$(alg)/fig.pdf))



NGINX_LOGS_DASH_IF_LOSS = $(foreach abrAlg, $(ABR_ALGS), $(foreach alg, $(CONG_ALGS), $(foreach profile, $(NETWORK_PROFILES), $(foreach run, $(RUN_NUMBERS), ${root}/logs/dash_if/loss/$(abrAlg)/$(profile)/$(run)_$(alg)/nginx_access.log))))
OUTPUT_PLOTS_LOSS = $(foreach abrAlg, $(ABR_ALGS), $(foreach alg, $(CONG_ALGS), $(foreach profile, $(NETWORK_PROFILES), $(foreach run, $(RUN_NUMBERS), ${root}/doc/dash_if/loss/$(abrAlg)/$(profile)/$(run)_$(alg)/plot.pdf))))

IGNORE_LINK_LOSS = 0

#setup
${bbb_hd}:
	@echo 'running setup'
	wget http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_2160p_60fps_normal.mp4 -P ${out_dir}
	@echo 'Video downloaded successfully'

${bbb_360}:
	@echo 'Downloading Bib Buck Bunny 360 p'
	wget http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_2160p_60fps_normal.mp4 -P ${out_dir}
	@echo 'Download finished successfully'

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


#encoder 360 3s
${out_dir}/3s/360/bbb_360_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 360 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action encode --source ${bbb_hd} --extra_arg 0 --segment_duration 3
	@echo 'Encoder executed'


#encoder 480 3s
${out_dir}/3s/480/bbb_480_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 480 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action encode --source ${bbb_hd} --extra_arg 1 --segment_duration 3
	@echo 'Encoder executed'


#encoder 720 3s
${out_dir}/3s/720/bbb_720_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 720 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action encode --source ${bbb_hd} --extra_arg 2 --segment_duration 3
	@echo 'Encoder executed'


#encoder 1080 3s
${out_dir}/3s/1080/bbb_1080_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 1080 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action encode --source ${bbb_hd} --extra_arg 3 --segment_duration 3
	@echo 'Encoder executed'

#encoder 1440 3s
${out_dir}/3s/1440/bbb_1440_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 1440 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action encode --source ${bbb_hd} --extra_arg 4 --segment_duration 3
	@echo 'Encoder executed'

#encoder 2160 3s
${out_dir}/3s/2160/bbb_2160_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 2160 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action encode --source ${bbb_hd} --extra_arg 5 --segment_duration 3
	@echo 'Encoder executed'

#encoder 360 DASH-IF
${out_dir}/dash-if/360/bbb_360_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 360 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action encode --source ${bbb_hd} --extra_arg 0 --segment_duration 3 --use_yt_bitrates 0
	@echo 'Encoder executed'


#encoder 480 DASH-IF
${out_dir}/dash-if/480/bbb_480_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 480 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action encode --source ${bbb_hd} --extra_arg 1 --segment_duration 3 --use_yt_bitrates 0
	@echo 'Encoder executed'


#encoder 720 DASH-IF
${out_dir}/dash-if/720/bbb_720_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 720 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action encode --source ${bbb_hd} --extra_arg 2 --segment_duration 3 --use_yt_bitrates 0
	@echo 'Encoder executed'


#encoder 1080 DASH-IF
${out_dir}/dash-if/1080/bbb_1080_60.mp4: ${bbb_hd} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 1080 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action encode --source ${bbb_hd} --extra_arg 3 --segment_duration 3 --use_yt_bitrates 0
	@echo 'Encoder executed'


#encoder 200 newcwv
${out_dir}/newcwv/200/bbb_200_60.mp4: ${bbb_360} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 200 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action encode --source ${bbb_hd} --extra_arg 0 --segment_duration 2 --use_yt_bitrates 0 --newcwv
	@echo 'Encoder executed'

#encoder 250 newcwv
${out_dir}/newcwv/250/bbb_250_60.mp4: ${bbb_360} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 250 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action encode --source ${bbb_hd} --extra_arg 1 --segment_duration 2 --use_yt_bitrates 0 --newcwv
	@echo 'Encoder executed'

#encoder 300 newcwv
${out_dir}/newcwv/300/bbb_300_60.mp4: ${bbb_360} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 300 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action encode --source ${bbb_hd} --extra_arg 2 --segment_duration 2 --use_yt_bitrates 0 --newcwv
	@echo 'Encoder executed'

#encoder 400 newcwv
${out_dir}/newcwv/400/bbb_400_60.mp4: ${bbb_360} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 400 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action encode --source ${bbb_hd} --extra_arg 3 --segment_duration 2 --use_yt_bitrates 0 --newcwv
	@echo 'Encoder executed'

#encoder 500 newcwv
${out_dir}/newcwv/500/bbb_500_60.mp4: ${bbb_360} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 500 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action encode --source ${bbb_hd} --extra_arg 4 --segment_duration 2 --use_yt_bitrates 0 --newcwv
	@echo 'Encoder executed'

#encoder 600 newcwv
${out_dir}/newcwv/600/bbb_600_60.mp4: ${bbb_360} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 600 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action encode --source ${bbb_hd} --extra_arg 5 --segment_duration 2 --use_yt_bitrates 0 --newcwv
	@echo 'Encoder executed'

#encoder 700 newcwv
${out_dir}/newcwv/700/bbb_700_60.mp4: ${bbb_360} ${root}/scripts/video_processing/encoder.py ${root}/scripts/video_processing/video_driver.py
	@echo 'running 700 encoder'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action encode --source ${bbb_hd} --extra_arg 6 --segment_duration 2 --use_yt_bitrates 0 --newcwv
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


#segmenter 360 3s
${out_dir}/3s/360/out/output.mpd: ${out_dir}/3s/360/bbb_360_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 360'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action segment --source ${bbb_hd} --extra_arg 640x360
	@echo 'Done segmenting'


#segmenter 480 3s
${out_dir}/3s/480/out/output.mpd: ${out_dir}/3s/480/bbb_480_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 480'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action segment --source ${bbb_hd} --extra_arg 854x480
	@echo 'Done segmenting'


#segmenter 720 3s
${out_dir}/3s/720/out/output.mpd: ${out_dir}/3s/720/bbb_720_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 720'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action segment --source ${bbb_hd} --extra_arg 1280x720
	@echo 'Done segmenting'


#segmenter 1080 3s
${out_dir}/3s/1080/out/output.mpd: ${out_dir}/3s/1080/bbb_1080_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 1080'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action segment --source ${bbb_hd} --extra_arg 1920x1080
	@echo 'Done segmenting'

#segmenter 1440 3s
${out_dir}/3s/1440/out/output.mpd: ${out_dir}/3s/1440/bbb_1440_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 1440'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action segment --source ${bbb_hd} --extra_arg 2560x1440
	@echo 'Done segmenting'

#segmenter 2160 3s
${out_dir}/3s/2160/out/output.mpd: ${out_dir}/3s/2160/bbb_2160_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 12160
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action segment --source ${bbb_hd} --extra_arg 3840x2160
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


#segmenter newcwv
${out_dir}/newcwv/200/out/output.mpd: ${out_dir}/newcwv/200/bbb_200_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 200'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action segment --source ${bbb_hd} --extra_arg 480x200 --newcwv
	@echo 'Done segmenting'


${out_dir}/newcwv/250/out/output.mpd: ${out_dir}/newcwv/250/bbb_250_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 250'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action segment --source ${bbb_hd} --extra_arg 480x250 --newcwv
	@echo 'Done segmenting'

${out_dir}/newcwv/300/out/output.mpd: ${out_dir}/newcwv/300/bbb_300_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 300'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action segment --source ${bbb_hd} --extra_arg 480x300 --newcwv
	@echo 'Done segmenting'

${out_dir}/newcwv/400/out/output.mpd: ${out_dir}/newcwv/400/bbb_400_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 400'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action segment --source ${bbb_hd} --extra_arg 480x400 --newcwv
	@echo 'Done segmenting'

${out_dir}/newcwv/500/out/output.mpd: ${out_dir}/newcwv/500/bbb_500_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 500'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action segment --source ${bbb_hd} --extra_arg 480x500 --newcwv
	@echo 'Done segmenting'

${out_dir}/newcwv/600/out/output.mpd: ${out_dir}/newcwv/600/bbb_600_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 600'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action segment --source ${bbb_hd} --extra_arg 480x600 --newcwv
	@echo 'Done segmenting'

${out_dir}/newcwv/700/out/output.mpd: ${out_dir}/newcwv/700/bbb_700_60.mp4 ${root}/scripts/video_processing/segmenter.py ${root}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 700'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action segment --source ${bbb_hd} --extra_arg 480x700 --newcwv
	@echo 'Done segmenting'

# # # # # # # # #
# MPD generator #
# # # # # # # # #


stage1-mpd: ${out_dir}/bbb.mpd
	@echo 'Generating mpd'

stage1-mpd-3s: ${out_dir}/3s/bbb.mpd
	@echo 'Generating mpd'
	
stage1-dash-if-mpd: ${out_dir}/dash-if/bbb.mpd
	@echo 'Generating dash-if MPD'

stage1-newcwv: ${out_dir}/newcwv/bbb.mpd
	@echo 'Generating newcwv MPD'

#MPD generator
${out_dir}/bbb.mpd: ${out_dir}/360/out/output.mpd ${out_dir}/480/out/output.mpd ${out_dir}/720/out/output.mpd ${out_dir}/1080/out/output.mpd ${root}/scripts/video_processing/video_driver.py ${root}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir} --action mpd --source ${bbb_hd} --media_prefix ../data

#MPD generator 3s
${out_dir}/3s/bbb.mpd: ${out_dir}/3s/360/out/output.mpd ${out_dir}/3s/480/out/output.mpd ${out_dir}/3s/720/out/output.mpd ${out_dir}/3s/1080/out/output.mpd ${out_dir}/3s/1440/out/output.mpd ${out_dir}/3s/2160/out/output.mpd ${root}/scripts/video_processing/video_driver.py ${root}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/3s --action mpd --source ${bbb_hd} --media_prefix ../3s

#MPD generator DASH-IF
${out_dir}/dash-if/bbb.mpd: ${out_dir}/dash-if/360/out/output.mpd ${out_dir}/dash-if/480/out/output.mpd ${out_dir}/dash-if/720/out/output.mpd ${out_dir}/dash-if/1080/out/output.mpd ${root}/scripts/video_processing/video_driver.py ${root}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/dash-if --action mpd --source ${bbb_hd} --media_prefix ../dash-if

#MPD generator newcwv
${out_dir}/newcwv/bbb.mpd: ${out_dir}/newcwv/200/out/output.mpd ${out_dir}/newcwv/250/out/output.mpd ${out_dir}/newcwv/300/out/output.mpd ${out_dir}/newcwv/400/out/output.mpd ${out_dir}/newcwv/500/out/output.mpd ${out_dir}/newcwv/600/out/output.mpd ${out_dir}/newcwv/700/out/output.mpd ${root}/scripts/video_processing/video_driver.py ${root}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${root}/scripts/video_processing/video_driver.py --prefix ${out_dir}/newcwv --action mpd --source ${bbb_hd} --media_prefix ../newcwv --newcwv

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
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_1.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)


${root}/logs/1/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_1.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/2/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_2.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/3/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_3.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/4/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_4.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/5/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_5.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/6/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_6.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/7/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_7.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/8/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_8.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/9/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_9.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/10/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_10.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/11/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_11.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/12/%_bbr/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg bbr --network_model /vagrant/network_models/dash_if/network_config_12.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)


${root}/logs/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_1.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG)  --ignore_link_loss $(IGNORE_LINK_LOSS)


${root}/logs/1/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_1.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/2/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_2.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/3/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_3.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/4/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_4.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/5/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_5.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/6/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_6.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/7/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_7.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/8/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_8.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/9/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_9.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/10/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_10.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/11/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_11.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/12/%_reno/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/dash_if/network_config_12.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)


${root}/logs/1/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_1.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/2/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_2.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/3/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_3.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/4/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_4.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/5/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_5.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/6/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_6.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/7/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_7.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/8/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_8.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/9/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_9.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/10/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_10.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/11/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_11.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/12/%_cubic/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_12.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)



${root}/logs/bw_cubic_%/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	#cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/scripts/bws/network_config_${*}.json


${root}/doc/%/fig.pdf: ${root}/logs/%/nginx_access.log ${root}/scripts/net_utils.py | ${root}/doc
	@echo $@
	python3 /vagrant/scripts/net_utils.py --source $(<D)

${root}/doc/dash_if/loss/%/plot.pdf: ${root}/logs/dash_if/loss/%/nginx_access.log
	python3 /vagrant/scripts/analytics/plot_packet_loss.py --source $(<D)	

stage3-run: ${NGINX_LOGS}
	@echo 'Running experiments'

stage3-diff_bw: ${BW_RUNS}
	@echo ${BW_RUNS}

stage3-plot: ${OUTPUT_PLOTS}
	@echo 'Generating plots'


stage3-plot-all: ${root}/scripts/net_utils.py
	@echo 'plotting data'
	python3 /vagrant/scripts/net_utils.py --all

stage3-plot-dash-if-loss: ${OUTPUT_PLOTS_LOSS}
	@echo 'plotting dash-if loss'

${root}/doc:
	@echo 'Creating doc directory'
	mkdir $@

test:
	# @echo $(NGINX_LOGS)
	$(eval DASH_ALG='abrDynamic')
	@echo $(DASH_ALG)

rule_cwv:
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/newcwv_newcwvh_05_17 --cong_alg newcwv --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location data/newcwv/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/newcwv_newcwvh2_05_17 --cong_alg newcwv --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location data/newcwv/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/newcwv_newcwvh3_05_17 --cong_alg newcwv --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location data/newcwv/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/newcwv_newcwvh4_05_17 --cong_alg newcwv --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location data/newcwv/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/newcwv_newcwvh5_05_17 --cong_alg newcwv --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location data/newcwv/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/newcwv_newcwvh6_05_17 --cong_alg newcwv --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location data/newcwv/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1



rule_cwv_reno:
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/newcwv_renoh_05_17 --cong_alg vreno --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location data/newcwv/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/newcwv_renoh2_05_17 --cong_alg vreno --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location data/newcwv/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/newcwv_renoh3_05_17 --cong_alg vreno --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location data/newcwv/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/newcwv_renoh4_05_17 --cong_alg vreno --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location data/newcwv/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1


simulate_wget:
	cd scripts/scratch && sudo python mn_sim.py --log_dir /vagrant/logs/ff_sim_05_14 --cong_alg newcwv

rule_cwv_fcc:
	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/fcc/newcwv_newcwvh_patched3 --cong_alg newcwv --network_model /vagrant/network_models/fcc/network_config_42.json --mpd_location data/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1
#	cd scripts && sudo python mn_script.py --log_dir /vagrant/logs/fcc/newcwv_renoh2_ripped --cong_alg vreno --network_model /vagrant/network_models/fcc/network_config_42.json --mpd_location data/bbb.mpd --dash_alg abrThroughput --ignore_link_loss 1

/vagrant/logs/cwv_ver/2s/newcwv1/kern.log: 
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case 2sec --disable_rto_reset 0
/vagrant/logs/cwv_ver/2s/newcwv2/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case 2sec --disable_rto_reset 0
/vagrant/logs/cwv_ver/2s/newcwv3/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case 2sec --disable_rto_reset 0

/vagrant/logs/cwv_ver/2s/reno1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case 2sec --disable_rto_reset 0
/vagrant/logs/cwv_ver/2s/reno2/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case 2sec --disable_rto_reset 0
/vagrant/logs/cwv_ver/2s/reno3/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case 2sec --disable_rto_reset 0

/vagrant/logs/cwv_ver/tc/tc5/newcwv1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case tc5 --disable_rto_reset 1

/vagrant/logs/cwv_ver/tc/tc5/newcwv2/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case tc5 --disable_rto_reset 1

/vagrant/logs/cwv_ver/tc/tc5/reno1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case tc5 --disable_rto_reset 1

/vagrant/logs/cwv_ver/tc/tc5/reno2/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case tc5 --disable_rto_reset 1

/vagrant/logs/cwv_ver/tc/0/tc5/newcwv1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case tc5 --disable_rto_reset 0

/vagrant/logs/cwv_ver/tc/0/tc5/newcwv2/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case tc5 --disable_rto_reset 0

/vagrant/logs/cwv_ver/tc/0/tc5/reno1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case tc5 --disable_rto_reset 0

/vagrant/logs/cwv_ver/tc/0/tc5/reno2/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case tc5 --disable_rto_reset 0


rule_new:
	sudo python scripts/scratch/mn_example.py --logdir /vagrant/logs/tmp/newcwv1 --cong_alg newcwv

/vagrant/logs/cwv_ver/tc/2sec/newcwv1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case 2sec --disable_rto_reset 0

/vagrant/logs/cwv_ver/tc/2sec/reno1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case 2sec --disable_rto_reset 0

rule_cwv_42: ${root}/logs/new_cwv/reno1/nginx_access.log ${root}/logs/new_cwv/newcwv1/nginx_access.log ${root}/logs/new_cwv/reno2/nginx_access.log ${root}/logs/new_cwv/newcwv2/nginx_access.log

/vagrant/logs/cwv_ver/tc/2sec/short/newcwv1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case 2sec --disable_rto_reset 0

/vagrant/logs/cwv_ver/tc/2sec/short/reno1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case 2sec --disable_rto_reset 0


${root}/logs/new_cwv/reno1/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg vreno --network_model /vagrant/network_models/fcc/network_config_42.json --mpd_location data/bbb.mpd --dash_alg abrThroughput --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/new_cwv/newcwv1/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/fcc/network_config_42.json --mpd_location data/bbb.mpd --dash_alg abrThroughput --ignore_link_loss $(IGNORE_LINK_LOSS)


${root}/logs/new_cwv/reno2/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg vreno --network_model /vagrant/network_models/fcc/network_config_42.json --mpd_location data/bbb.mpd --dash_alg abrThroughput --ignore_link_loss $(IGNORE_LINK_LOSS)

${root}/logs/new_cwv/newcwv2/nginx_access.log: ${root}/scripts/mn_script.py ${out_dir}/bbb.mpd | ${root}/logs
	@echo $@
	cd ${root}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/fcc/network_config_42.json --mpd_location data/bbb.mpd --dash_alg abrThroughput --ignore_link_loss $(IGNORE_LINK_LOSS)

/vagrant/logs/cwv_ver/tc/2sec/short/newcwv2/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case 2sec --disable_rto_reset 0

/vagrant/logs/cwv_ver/tc/2sec/short/reno2/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case 2sec --disable_rto_reset 0

2sec_short: /vagrant/logs/cwv_ver/tc/2sec/short/newcwv1/kern.log /vagrant/logs/cwv_ver/tc/2sec/short/reno1/kern.log /vagrant/logs/cwv_ver/tc/2sec/short/newcwv2/kern.log /vagrant/logs/cwv_ver/tc/2sec/short/reno2/kern.log


720: /vagrant/logs/cwv_ver/tc/2sec/720/newcwv1/kern.log /vagrant/logs/cwv_ver/tc/2sec/720/reno1/kern.log 

/vagrant/logs/cwv_ver/tc/2sec/720/newcwv1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg newcwv --case 2sec --disable_rto_reset 0

/vagrant/logs/cwv_ver/tc/2sec/720/reno1/kern.log:
	sudo python scripts/scratch/mn_example.py --logdir ${@D} --cong_alg vreno --case 2sec --disable_rto_reset 0
	