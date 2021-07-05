ROOT:=/vagrant

DASH_ALG=abrThroughput
MPD_LOCATION=data/ietf/bbb.mpd
OUT_DIR=${ROOT}/data
IGNORE_LINK_LOSS=0

REPEAT = 3
RUNS = $(shell seq 1 ${REPEAT})
ALGS = reno vreno newcwv
LINKS = FTTP DSL FTTC

LOGS = $(foreach link, ${LINKS}, $(foreach alg, ${ALGS}, $(foreach run_instance, ${RUNS}, ${ROOT}/logs/newcwv/${link}/${run_instance}_${alg}/nginx_access.log)))

# Encoding video

#setup
${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4:
	@echo 'running setup'
	wget http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_2160p_60fps_normal.mp4 -P ${OUT_DIR}
	@echo 'Video downloaded successfully'


################
# Encoder
################

####### IETF

#encoder 480 3s
${OUT_DIR}/ietf/480/bbb_480_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 480 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/ietf --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 0 --segment_duration 3 --use_dataset 2
	@echo 'Encoder executed'

#encoder 720 3s
${OUT_DIR}/ietf/720/bbb_720_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 720 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/ietf --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 1 --segment_duration 3 --use_dataset 2
	@echo 'Encoder executed'

#encoder 1080 3s
${OUT_DIR}/ietf/1080/bbb_1080_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 1080 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/ietf --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 2 --segment_duration 3 --use_dataset 2
	@echo 'Encoder executed'

#encoder 2160 3s
${OUT_DIR}/ietf/2160/bbb_2160_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 2160 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/ietf --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 3 --segment_duration 3 --use_dataset 2
	@echo 'Encoder executed'

###############

#encoder 360 3s
${OUT_DIR}/3s/360/bbb_360_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 360 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 0 --segment_duration 3
	@echo 'Encoder executed'


#encoder 480 3s
${OUT_DIR}/3s/480/bbb_480_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 480 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 1 --segment_duration 3
	@echo 'Encoder executed'


#encoder 720 3s
${OUT_DIR}/3s/720/bbb_720_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 720 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 2 --segment_duration 3
	@echo 'Encoder executed'


#encoder 1080 3s
${OUT_DIR}/3s/1080/bbb_1080_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 1080 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 3 --segment_duration 3
	@echo 'Encoder executed'

#encoder 1440 3s
${OUT_DIR}/3s/1440/bbb_1440_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 1440 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 4 --segment_duration 3
	@echo 'Encoder executed'

#encoder 2160 3s
${OUT_DIR}/3s/2160/bbb_2160_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 2160 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 5 --segment_duration 3
	@echo 'Encoder executed'

###############
# Segmenter
###############

####### IETF

#segmenter 480 3s
${OUT_DIR}/ietf/480/out/output.mpd: ${OUT_DIR}/ietf/480/bbb_480_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 480'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/ietf --action segment --extra_arg 720x480
	@echo 'Done segmenting'

#segmenter 720 3s
${OUT_DIR}/ietf/720/out/output.mpd: ${OUT_DIR}/ietf/720/bbb_720_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 720'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/ietf --action segment --extra_arg 1280x720
	@echo 'Done segmenting'

#segmenter 1080 3s
${OUT_DIR}/ietf/1080/out/output.mpd: ${OUT_DIR}/ietf/1080/bbb_1080_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 1080'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/ietf --action segment --extra_arg 1920x1080
	@echo 'Done segmenting'

#segmenter 2160 3s
${OUT_DIR}/ietf/2160/out/output.mpd: ${OUT_DIR}/ietf/2160/bbb_2160_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 2160'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/ietf --action segment --extra_arg 3840x2160
	@echo 'Done segmenting'

###################

#segmenter 360 3s
${OUT_DIR}/3s/360/out/output.mpd: ${OUT_DIR}/3s/360/bbb_360_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 360'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action segment --extra_arg 640x360
	@echo 'Done segmenting'


#segmenter 480 3s
${OUT_DIR}/3s/480/out/output.mpd: ${OUT_DIR}/3s/480/bbb_480_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 480'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action segment --extra_arg 854x480
	@echo 'Done segmenting'


#segmenter 720 3s
${OUT_DIR}/3s/720/out/output.mpd: ${OUT_DIR}/3s/720/bbb_720_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 720'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action segment --extra_arg 1280x720
	@echo 'Done segmenting'


#segmenter 1080 3s
${OUT_DIR}/3s/1080/out/output.mpd: ${OUT_DIR}/3s/1080/bbb_1080_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 1080'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action segment --extra_arg 1920x1080
	@echo 'Done segmenting'

#segmenter 1440 3s
${OUT_DIR}/3s/1440/out/output.mpd: ${OUT_DIR}/3s/1440/bbb_1440_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 1440'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action segment --extra_arg 2560x1440
	@echo 'Done segmenting'

#segmenter 2160 3s
${OUT_DIR}/3s/2160/out/output.mpd: ${OUT_DIR}/3s/2160/bbb_2160_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 12160
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action segment --extra_arg 3840x2160
	@echo 'Done segmenting'


####### IETF

####################
#MPD generator 3s
####################

${OUT_DIR}/3s/bbb.mpd: ${OUT_DIR}/3s/360/out/output.mpd ${OUT_DIR}/3s/480/out/output.mpd ${OUT_DIR}/3s/720/out/output.mpd ${OUT_DIR}/3s/1080/out/output.mpd ${OUT_DIR}/3s/1440/out/output.mpd ${OUT_DIR}/3s/2160/out/output.mpd ${ROOT}/scripts/video_processing/video_driver.py ${ROOT}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/3s --action mpd --media_prefix ../3s

####### IETF

${OUT_DIR}/ietf/bbb.mpd: ${OUT_DIR}/ietf/480/out/output.mpd ${OUT_DIR}/ietf/720/out/output.mpd ${OUT_DIR}/ietf/1080/out/output.mpd ${OUT_DIR}/ietf/2160/out/output.mpd  ${ROOT}/scripts/video_processing/video_driver.py ${ROOT}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/ietf --action mpd --media_prefix ../ietf --use_dataset 2

stage1-mpd-3s: ${OUT_DIR}/3s/bbb.mpd
	@echo 'Generating mpd'

stage1-mpd-ietf: ${OUT_DIR}/ietf/bbb.mpd
	@echo 'Generating mpd'

#############
# Simulation
#############

logs: ${LOGS}

## DSL

${ROOT}/logs/newcwv/DSL/%_vreno/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg vreno --network_model /vagrant/network_models/links/DSL.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/DSL/%_newcwv/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/links/DSL.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/DSL/%_reno/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/links/DSL.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

## FTTC

${ROOT}/logs/newcwv/FTTC/%_vreno/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg vreno --network_model /vagrant/network_models/links/FTTC.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/FTTC/%_newcwv/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/links/FTTC.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/FTTC/%_reno/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/links/FTTC.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

## FTTP

${ROOT}/logs/newcwv/FTTP/%_vreno/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg vreno --network_model /vagrant/network_models/links/FTTP.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/FTTP/%_newcwv/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/links/FTTP.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/FTTP/%_reno/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg reno --network_model /vagrant/network_models/links/FTTP.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs:
	mkdir ${ROOT}/logs
