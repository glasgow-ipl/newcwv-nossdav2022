ROOT:=/vagrant

DASH_ALG=abrThroughput
MPD_LOCATION=data/ietf/bbb.mpd
OUT_DIR=${ROOT}/data
IGNORE_LINK_LOSS=0

MPD_LOCATION_NEWCWV=data/newcwv/bbb.mpd

REPEAT = 10
RUNS = $(shell seq 1 ${REPEAT})
ALGS = vreno newcwv reno
LINKS = DSL FTTC FTTP

LOGS = $(foreach link, ${LINKS}, $(foreach alg, ${ALGS}, $(foreach run_instance, ${RUNS}, ${ROOT}/logs/newcwv/${link}/${run_instance}_${alg}/nginx_access.log)))

TEST_ALGS = newcwv vreno

CLIENTS = 1 2 3 5

TEST_LOGS = $(foreach link, ${LINKS}, $(foreach alg, ${TEST_ALGS}, $(foreach run_instance, $(shell seq 1 10), ${ROOT}/logs/newcwv/test2/${link}/${run_instance}_${alg}/nginx_access.log)))

CLIENTS = 1 2 3 5

MULTI_LOGS = $(foreach client, ${CLIENTS}, $(foreach link, ${LINKS}, $(foreach alg, ${TEST_ALGS}, $(foreach run_instance, ${RUNS}, ${ROOT}/logs/clients/${client}/${link}/${run_instance}_${alg}/nginx_access.log))))

MULTI_LOGS_DYNAMIC = $(foreach client, ${CLIENTS}, $(foreach link, ${LINKS}, $(foreach alg, ${TEST_ALGS}, $(foreach run_instance, ${RUNS}, ${ROOT}/logs/clients/dynamic/${client}/${link}/${run_instance}_${alg}/nginx_access.log))))

BWS = 10
RTTS = $(shell seq 20 10 200)

# Client loop should be ${CLIENTS}
MULTI_LOG_VARYING = $(foreach client, $(shell seq 1 1), $(foreach bw, ${BWS}, $(foreach rtt, ${RTTS}, $(foreach alg, ${TEST_ALGS}, $(foreach run_instance, $(shell seq 1 3), ${ROOT}/logs/clients/${client}/abr/abrThroughput/${bw}_${rtt}/${run_instance}_${alg}/nginx_access.log)))))

RTT_NEWCWV = 400
BW_NEWCWV = 1
LOGS_NEWCWV = $(foreach client, $(shell seq 1 1), $(foreach bw, ${BW_NEWCWV}, $(foreach rtt, ${RTT_NEWCWV}, $(foreach alg, ${TEST_ALGS}, $(foreach run_instance, $(shell seq 1 3), ${ROOT}/logs/newcwv/clients/${client}/abr/abrThroughput/${bw}_${rtt}/${run_instance}_${alg}/nginx_access.log)))))

# Encoding video

#setup
${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4:
	@echo 'running setup'
	wget http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_2160p_60fps_normal.mp4 -P ${OUT_DIR}
	@echo 'Video downloaded successfully'


################
# Encoder
################

####### NewCWV

#encoder 200 3s
${OUT_DIR}/newcwv/200/bbb_200_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 200 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 0 --segment_duration 3 --newcwv
	@echo 'Encoder executed'


#encoder 200 3s
${OUT_DIR}/newcwv/250/bbb_250_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 250 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 1 --segment_duration 3 --newcwv
	@echo 'Encoder executed'


#encoder 200 3s
${OUT_DIR}/newcwv/300/bbb_300_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 300 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 2 --segment_duration 3 --newcwv
	@echo 'Encoder executed'


#encoder 200 3s
${OUT_DIR}/newcwv/400/bbb_400_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 400 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 3 --segment_duration 3 --newcwv
	@echo 'Encoder executed'


#encoder 200 3s
${OUT_DIR}/newcwv/500/bbb_500_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 500 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 4 --segment_duration 3 --newcwv
	@echo 'Encoder executed'


#encoder 200 3s
${OUT_DIR}/newcwv/600/bbb_600_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 600 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 5 --segment_duration 3 --newcwv
	@echo 'Encoder executed'


#encoder 200 3s
${OUT_DIR}/newcwv/700/bbb_700_60.mp4: ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 ${ROOT}/scripts/video_processing/encoder.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'running 700 encoder'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action encode --source ${OUT_DIR}/bbb_sunflower_2160p_60fps_normal.mp4 --extra_arg 6 --segment_duration 3 --newcwv
	@echo 'Encoder executed'


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

####### Newcwv

#segmenter 480 3s
${OUT_DIR}/newcwv/200/out/output.mpd: ${OUT_DIR}/newcwv/200/bbb_200_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 200'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action segment --extra_arg _x200
	@echo 'Done segmenting'


#segmenter 480 3s
${OUT_DIR}/newcwv/250/out/output.mpd: ${OUT_DIR}/newcwv/250/bbb_250_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 250'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action segment --extra_arg _x250
	@echo 'Done segmenting'


#segmenter 480 3s
${OUT_DIR}/newcwv/300/out/output.mpd: ${OUT_DIR}/newcwv/300/bbb_300_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 300'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action segment --extra_arg _x300
	@echo 'Done segmenting'


#segmenter 480 3s
${OUT_DIR}/newcwv/400/out/output.mpd: ${OUT_DIR}/newcwv/400/bbb_400_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 400'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action segment --extra_arg _x400
	@echo 'Done segmenting'


#segmenter 480 3s
${OUT_DIR}/newcwv/500/out/output.mpd: ${OUT_DIR}/newcwv/500/bbb_500_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 500'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action segment --extra_arg _x500
	@echo 'Done segmenting'


#segmenter 480 3s
${OUT_DIR}/newcwv/600/out/output.mpd: ${OUT_DIR}/newcwv/600/bbb_600_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 600'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action segment --extra_arg _x600
	@echo 'Done segmenting'


#segmenter 480 3s
${OUT_DIR}/newcwv/700/out/output.mpd: ${OUT_DIR}/newcwv/700/bbb_700_60.mp4 ${ROOT}/scripts/video_processing/segmenter.py ${ROOT}/scripts/video_processing/video_driver.py
	@echo 'Segmenting 700'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action segment --extra_arg _x700
	@echo 'Done segmenting'


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
	@echo 'Segmenting 12160'
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

####### Newcwv

${OUT_DIR}/newcwv/bbb.mpd: ${OUT_DIR}/newcwv/200/out/output.mpd ${OUT_DIR}/newcwv/250/out/output.mpd ${OUT_DIR}/newcwv/300/out/output.mpd ${OUT_DIR}/newcwv/400/out/output.mpd ${OUT_DIR}/newcwv/500/out/output.mpd ${OUT_DIR}/newcwv/600/out/output.mpd ${OUT_DIR}/newcwv/700/out/output.mpd ${ROOT}/scripts/video_processing/video_driver.py ${ROOT}/scripts/video_processing/mpd_generator.py
	@echo 'stitching mpds'
	python3 ${ROOT}/scripts/video_processing/video_driver.py --prefix ${OUT_DIR}/newcwv --action mpd --media_prefix ../newcwv --newcwv


stage1-mpd-3s: ${OUT_DIR}/3s/bbb.mpd
	@echo 'Generating mpd'

stage1-mpd-ietf: ${OUT_DIR}/ietf/bbb.mpd
	@echo 'Generating mpd'

stage1-mpd-newcwv: ${OUT_DIR}/newcwv/bbb.mpd
	@echo 'Generating mpd'

#############
# Simulation
#############

logs: ${LOGS}

${ROOT}/logs:
	mkdir ${ROOT}/logs

${ROOT}/logs/clients/1/abr/abrThroughput/%/nginx_access.log:
	$(eval SIM_DIR = $(@D))
	$(eval CC_ALG = $(shell echo $(shell basename $(@D)) | cut -d'_' -f2))
	$(eval LINK_TYPE = $(shell basename `dirname $(@D)`))
	$(eval ABR_ALG = $(shell basename $(shell dirname `dirname $(@D)`)))
	$(eval CLIENT_NUM = $(shell basename $(shell dirname $(shell dirname $(shell dirname `dirname $(@D)`)))))
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir ${SIM_DIR} --cong_alg ${CC_ALG} --network_model /vagrant/network_models/custom_models/${LINK_TYPE}.json --mpd_location $(MPD_LOCATION) --dash_alg ${ABR_ALG} --ignore_link_loss $(IGNORE_LINK_LOSS) --clients ${CLIENT_NUM}


${ROOT}/logs/newcwv/clients/1/abr/abrThroughput/%/nginx_access.log:
	$(eval SIM_DIR = $(@D))
	$(eval CC_ALG = $(shell echo $(shell basename $(@D)) | cut -d'_' -f2))
	$(eval LINK_TYPE = $(shell basename `dirname $(@D)`))
	$(eval ABR_ALG = $(shell basename $(shell dirname `dirname $(@D)`)))
	$(eval CLIENT_NUM = $(shell basename $(shell dirname $(shell dirname $(shell dirname `dirname $(@D)`)))))
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir ${SIM_DIR} --cong_alg ${CC_ALG} --network_model /vagrant/network_models/newcwv/newcwv.json --mpd_location $(MPD_LOCATION_NEWCWV) --dash_alg ${ABR_ALG} --ignore_link_loss $(IGNORE_LINK_LOSS) --clients ${CLIENT_NUM}


varying_rtt: ${MULTI_LOG_VARYING}
	echo "Done"


newcwv_logs: ${LOGS_NEWCWV}
	echo "Done"


${ROOT}/logs/clients/dynamic/%_vreno/nginx_access.log:
	$(eval SIM_DIR = $(@D))
	$(eval LINK_TYPE = $(shell basename `dirname $(@D)`))
	$(eval CLIENT_NUM = $(shell basename $(shell dirname `dirname $(@D)`)))
	echo "SIM_DIR=${SIM_DIR}"
	echo "LINK_TYPE=${LINK_TYPE}"
	echo "CLIENTS=${CLIENT_NUM}"
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg vreno --network_model /vagrant/network_models/links/${LINK_TYPE}.json --mpd_location $(MPD_LOCATION) --dash_alg abrDynamic --ignore_link_loss $(IGNORE_LINK_LOSS) --clients ${CLIENT_NUM}


${ROOT}/logs/clients/dynamic/%_newcwv/nginx_access.log:
	$(eval SIM_DIR = $(@D))
	$(eval LINK_TYPE = $(shell basename `dirname $(@D)`))
	$(eval CLIENT_NUM = $(shell basename $(shell dirname `dirname $(@D)`)))
	echo "SIM_DIR=${SIM_DIR}"
	echo "LINK_TYPE=${LINK_TYPE}"
	echo "CLIENTS=${CLIENT_NUM}"
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/links/${LINK_TYPE}.json --mpd_location $(MPD_LOCATION) --dash_alg abrDynamic --ignore_link_loss $(IGNORE_LINK_LOSS) --clients ${CLIENT_NUM}


# ${ROOT}/logs/clients/%_vreno/nginx_access.log:
# 	$(eval SIM_DIR = $(@D))
# 	$(eval LINK_TYPE = $(shell basename `dirname $(@D)`))
# 	$(eval CLIENT_NUM = $(shell basename $(shell dirname `dirname $(@D)`)))
# 	echo "SIM_DIR=${SIM_DIR}"
# 	echo "LINK_TYPE=${LINK_TYPE}"
# 	echo "CLIENTS=${CLIENT_NUM}"
# 	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg vreno --network_model /vagrant/network_models/links/${LINK_TYPE}.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS) --clients ${CLIENT_NUM}


# ${ROOT}/logs/clients/%_newcwv/nginx_access.log:
# 	$(eval SIM_DIR = $(@D))
# 	$(eval LINK_TYPE = $(shell basename `dirname $(@D)`))
# 	$(eval CLIENT_NUM = $(shell basename $(shell dirname `dirname $(@D)`)))
# 	echo "SIM_DIR=${SIM_DIR}"
# 	echo "LINK_TYPE=${LINK_TYPE}"
# 	echo "CLIENTS=${CLIENT_NUM}"
# 	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/links/${LINK_TYPE}.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS) --clients ${CLIENT_NUM}


test: ${TEST_LOGS}
	echo "Raaan test succcesssfullly"


multi_log: ${MULTI_LOGS} ${MULTI_LOGS_DYNAMIC}
	echo "Completed"


single_run: ${ROOT}/logs/single/newcwv/nginx_access.log
	@echo "Single run executed successfully"


${ROOT}/logs/single/newcwv/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/links/FTTP.json --mpd_location $(MPD_LOCATION) --dash_alg ${DASH_ALG} --ignore_link_loss ${IGNORE_LINK_LOSS} --clients 2

############################
# Paper 
############################

MAKEFLAGS += --output-sync --warn-undefined-variables --no-builtin-rules --no-builtin-variables

# Remove output of failed commands, to avoid confusing later runs of make:
.DELETE_ON_ERROR:

# Remove obsolete old-style default suffix rules:
.SUFFIXES:

# List of targets that don't represent files:
.PHONY: all clean check-make git-revision check-downloads

# =================================================================================================
# Configuration for the project:

# The PDF files to build, each should have a corresponding .tex file:
PDF_FILES = doc/paper/papers/paper.pdf

# Paper BUILD dir
PAPER_BUILD = doc/paper

FIGURES_FOLDER = ${PAPER_BUILD}/figures

.PRECIOUS: ${FIGURES_FOLDER}/tmp/%/parsed_data.json

RAW_DATA = ${foreach client, ${CLIENTS}, ${FIGURES_FOLDER}/tmp/${client}/parsed_data.json}

RAW_DATA_NEWCWV = ${FIGURES_FOLDER}/parsed/newcwv/parsed_data.json

BITRATE_DERIVATIVE_DATA = ${foreach client, ${CLIENTS}, ${FIGURES_FOLDER}/tmp/${client}/quality_distribution.json}

REBUFFER_RATIO_DATA = ${foreach client, ${CLIENTS}, ${FIGURES_FOLDER}/tmp/${client}/rebuffer_ratio.json}

# Tools to build before the PDF files. This is a list of executable files in
# the bin/ directory:
TOOLS = 

FIGURES_TRANSPORT = $(foreach client, ${CLIENTS},  ${FIGURES_FOLDER}/Throughput_${client}_clients.pdf)

FIGURES_TRANSPORT = ${FIGURES_FOLDER}/Throughput_clients_DSL.pdf ${FIGURES_FOLDER}/Throughput_clients_FTTC.pdf ${FIGURES_FOLDER}/lost_packets_vreno.pdf ${FIGURES_FOLDER}/lost_packets_newcwv.pdf ${FIGURES_FOLDER}/lost_packets.pdf

FIGURES_APPLICATION = ${FIGURES_FOLDER}/Rebuffer_Ratio.pdf ${FIGURES_FOLDER}/bitrate_derivative_distribution.pdf


${FIGURES_FOLDER}/tmp/%/rebuffer_ratio.json: ${ROOT}/scripts/analytics/paper/parse_rebuffer_ratio.py
	/usr/bin/python3 /vagrant/scripts/analytics/paper/parse_rebuffer_ratio.py --root /vagrant/logs/clients/$* --algs newcwv vreno --runs ${shell seq 1 10} --links ${LINKS}


#TODO: Logs as a dependency here
# ${ROOT}/scripts/analytics/paper/plot_driver.py
${FIGURES_FOLDER}/tmp/%/parsed_data.json: ${ROOT}/scripts/analytics/paper/parse_data.py ${ROOT}/scripts/analytics/paper/count_lost_packets.py ${ROOT}/scripts/analytics/parse_access_log.py ${ROOT}/scripts/analytics/parse_dash_log.py
	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_driver.py --root /vagrant/logs/clients/$* --algs newcwv vreno --runs ${shell seq 1 10} --links ${LINKS} --parse 1 --target none


${FIGURES_FOLDER}/parsed/newcwv/parsed_data.json: ${ROOT}/scripts/analytics/paper/parse_data.py ${ROOT}/scripts/analytics/paper/count_lost_packets.py ${ROOT}/scripts/analytics/parse_access_log.py ${ROOT}/scripts/analytics/parse_dash_log.py
	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_driver.py --root /vagrant/logs/clients/$* --algs newcwv vreno --runs ${shell seq 1 10} --links ${LINKS} --parse 1 --target none


${FIGURES_FOLDER}/tmp/%/quality_distribution.json: ${ROOT}/scripts/analytics/paper/parse_data.py ${ROOT}/scripts/analytics/parse_access_log.py ${MULTI_LOGS}
	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_driver.py --root /vagrant/logs/clients/$* --algs newcwv vreno --runs ${shell seq 1 10} --links ${LINKS} --parse 1 --target none


#TODO need to fix parsed data dependency to allow for more clients
${FIGURES_FOLDER}/Average_Bitrate.pdf: ${RAW_DATA} ${ROOT}/scripts/analytics/paper/plot_driver.py ${ROOT}/scripts/analytics/paper/plot_data.py
	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_driver.py --algs newcwv vreno --links ${LINKS} --target "average bitrate" --clients_combined ${CLIENTS} --extension pdf


AVERAGE_OSCILLATIONS_LINKS = DSL FTTC
${FIGURES_FOLDER}/Average_Oscillations.pdf: ${RAW_DATA} ${ROOT}/scripts/analytics/paper/plot_driver.py ${ROOT}/scripts/analytics/paper/plot_data.py
	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_driver.py --algs newcwv vreno --links ${AVERAGE_OSCILLATIONS_LINKS} --target "average oscillations" --clients_combined ${CLIENTS} --extension pdf


REBUFFER_RATIO_LINKS = DSL
${FIGURES_FOLDER}/Rebuffer_Ratio.pdf: ${ROOT}/scripts/analytics/paper/plot_driver.py ${ROOT}/scripts/analytics/paper/plot_data.py ${REBUFFER_RATIO_DATA}
	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_driver.py --algs vreno newcwv --links ${REBUFFER_RATIO_LINKS} --target "rebuffer ratio" --clients_combined ${CLIENTS} --extension pdf


${FIGURES_FOLDER}/Throughput_%_clients.pdf: ${FIGURES_FOLDER}/tmp/%/parsed_data.json ${ROOT}/scripts/analytics/paper/plot_driver.py ${ROOT}/scripts/analytics/paper/plot_data.py
	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_driver.py --algs newcwv vreno --links ${LINKS} --target "throughput" --clients_combined ${CLIENTS} --clients $* --extension pdf


BITRATE_DERIVATIVE_LINKS = DSL
${FIGURES_FOLDER}/bitrate_derivative_distribution.pdf: ${ROOT}/scripts/analytics/paper/plot_driver.py ${ROOT}/scripts/analytics/paper/plot_data.py
	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_driver.py --algs newcwv vreno --links ${BITRATE_DERIVATIVE_LINKS} --target "bitrate_derivatives" --clients_combined ${CLIENTS} --extension pdf


${FIGURES_FOLDER}/Throughput_clients_%.pdf:
	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_driver.py --algs newcwv vreno --links ${LINKS} --target "throughput agg" --clients_combined ${CLIENTS} --link_agg $* --extension pdf	


${FIGURES_FOLDER}/lost_packets_vreno.pdf:
	/usr/bin/python3 ${ROOT}/scripts/analytics/paper/plot_lost_packets.py --root ${ROOT}/logs/clients/1/DSL/1_vreno


${FIGURES_FOLDER}/lost_packets_newcwv.pdf:
	/usr/bin/python3 ${ROOT}/scripts/analytics/paper/plot_lost_packets.py --root ${ROOT}/logs/clients/1/DSL/1_newcwv


${FIGURES_FOLDER}/lost_packets.pdf:
	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_lost_packets_aggregate.py --algs newcwv vreno --clients_combined 1 2 3 5

# ${FIGURES_FOLDER}/Average_Stalls_5_clients.pdf: ${FIGURES_FOLDER}/tmp/parsed_data.json
# 	/usr/bin/python3 /vagrant/scripts/analytics/paper/plot_data.py --algs newcwv vreno --links ${LINKS} --target "average stalls" --extension png

# figures: ${ROOT}/scripts/analytics/paper/plot_data.py ${TEST_LOGS}
# 	@echo 'Generating Figures'
# 	/usr/bin/python3 $<
# 	@echo 'Done'

# ${FIGURES}: figures

# Master build rule:
paper: ${FIGURES_APPLICATION} ${FIGURES_TRANSPORT} check-make git-revision $(TOOLS) $(PDF_FILES)

# Build a paper without pre-building the figures
paper-quick: check-make git-revision $(TOOLS)
	@sh   $(PAPER_BUILD)/bin/latex-build.sh doc/paper/papers/paper.tex
	@perl $(PAPER_BUILD)/bin/check-for-duplicate-words.perl doc/paper/papers/paper.tex
	@sh   $(PAPER_BUILD)/bin/check-for-todo.sh              doc/paper/papers/paper.tex
	cp $(PAPER_BUILD)/papers/paper.pdf $(PAPER_BUILD)/papers/paper_$(shell cat $(PAPER_BUILD)/git-revision).pdf

# =================================================================================================
# Project specific rules to download files:
#
# The bin/download.sh script can be used to download files if they don't exist
# or have changed on the server, as shown in the example below. The downloaded
# files should depend on the bin/download.sh script and on the check-downloads
# target. Each downloaded file must be added to $(DOWNLOADS) so the "download"
# and "clean" targets work.

index.html: bin/download.sh check-downloads
	@bin/download.sh https://csperkins.org/index.html $@

DOWNLOADS = index.html

# Rule to manually downloads. This shouldn't be referenced in other rules, they
# should depend on the downloaded files.
download: $(DOWNLOADS)

# This is marked as .PHONY above and must not depend on any real files. When
# make runs it will see this as being out-of-date, triggering the downloads.
check-downloads:

# =================================================================================================
# Project specific rules:
#
# Add rules to build $(TOOLS) here (there is a generic rule to build a single
# C source file into an executable below):



# Add rules to build the dependencies of $(PDF_FILES) here:



# =================================================================================================
# Generic rules:

# This Makefile requires GNU make:
check-make:
	$(if $(findstring GNU Make,$(shell $(MAKE) --version)),,$(error Not GNU make))

# Record the git revision for the repository. This is a real file but is marked
# as .PHONY above so the recipe always executes. The bin/git-revision.sh script
# only writes to the output file if the revision has changed.
git-revision: doc/paper/bin/git-revision.sh
	@sh $< $(PAPER_BUILD)/$(@)

# =================================================================================================
# Generic rules to build PDF files and figures:

# Pattern rules to build a PDF file. The assumption is that each PDF file 
# is built from the corresponding .tex file.
%.pdf: %.tex $(PAPER_BUILD)/bin/latex-build.sh
	@sh   $(PAPER_BUILD)/bin/latex-build.sh $<
	@perl $(PAPER_BUILD)/bin/check-for-duplicate-words.perl $<
	@sh   $(PAPER_BUILD)/bin/check-for-todo.sh              $<
	cp $(PAPER_BUILD)/papers/paper.pdf $(PAPER_BUILD)/papers/paper_$(shell cat $(PAPER_BUILD)/git-revision).pdf

# Include dependency information for PDF files, if it exists:
-include $(PDF_FILES:%.pdf=%.dep)

# Pattern rules to build plots using gnuplot. These require the data
# to be plotted be in figures/%.dat, while the script to control the
# plot is in figures/%.gnuplot. The script figures/%.gnuplot-pdf (or
# figures/%.gnuplot-svg) is loaded before the main gnuplot script,
# and should call "set terminal ..." and "set output ..." to set the
# appropriate format and output file. This allows the main gnuplot 
# script to be terminal independent.
figures/%.pdf: figures/%.gnuplot-pdf figures/%.gnuplot figures/%.dat
	gnuplot figures/$*.gnuplot-pdf figures/$*.gnuplot

figures/%.svg: figures/%.gnuplot-svg figures/%.gnuplot figures/%.dat
	gnuplot figures/$*.gnuplot-svg figures/$*.gnuplot

# =================================================================================================
# Generic rules to build code:

# Pattern rules to build C programs comprising a single file:
CC     = clang
CFLAGS = -W -Wall -Wextra -O2 -g -std=c99

bin/%: src/%.c
	$(CC) $(CFLAGS) -o $@ $^

# =================================================================================================
# Generic rules to clean-up:

define xargs
$(if $(2),$(1) $(firstword $(2)))
$(if $(word 2,$(2)),$(call xargs,$(1),$(wordlist 2,$(words $(2)),$(2))))
endef

define remove
$(call xargs,rm -f,$(1))
endef

define remove-latex
$(call xargs,sh $(PAPER_BUILD)/bin/latex-build.sh --clean,$(1))
endef

clean:
	$(call remove,$(PAPER_BUILD)/git-revision)
	$(call remove,$(PAPER_BUILD)/$(DOWNLOADS))
ifneq ($(strip $(TOOLS)),)
	$(call remove,$(PAPER_BUILD)/$(TOOLS))
endif
	$(foreach tool,$(TOOLS),rm -rf $(PAPER_BUILD)/$(tool).dSYM)
	@$(call remove-latex,$(PDF_FILES:%.pdf=%.tex))
	rm -f $(PAPER_BUILD)/papers/paper_*.pdf
	rm -f $(PAPER_BUILD)/papers/paper.synctex.gz

full_clean:
	$(call remove,$(PAPER_BUILD)/git-revision)
	$(call remove,$(PAPER_BUILD)/$(DOWNLOADS))
ifneq ($(strip $(TOOLS)),)
	$(call remove,$(PAPER_BUILD)/$(TOOLS))
endif
	$(foreach tool,$(TOOLS),rm -rf $(PAPER_BUILD)/$(tool).dSYM)
	@$(call remove-latex,$(PDF_FILES:%.pdf=%.tex))
	rm -f $(PAPER_BUILD)/papers/paper_*.pdf
	rm -f $(PAPER_BUILD)/papers/paper.synctex.gz
