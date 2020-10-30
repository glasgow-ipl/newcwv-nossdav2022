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


${root}/logs/1/nginx_access.log: ${root}/scripts/mn_script.py
	cd ${root}/scripts && sudo python mn_script.py --log_dir "$(shell dirname $@)"

${root}/logs/2/nginx_access.log: ${root}/scripts/mn_script.py
	cd ${root}/scripts && sudo python mn_script.py --log_dir "$(shell dirname $@)"

${root}/logs/3/nginx_access.log: ${root}/scripts/mn_script.py
	cd ${root}/scripts && sudo python mn_script.py --log_dir "$(shell dirname $@)"

${root}/logs/4/nginx_access.log: ${root}/scripts/mn_script.py
	cd ${root}/scripts && sudo python mn_script.py --log_dir "$(shell dirname $@)"

${root}/logs/5/nginx_access.log: ${root}/scripts/mn_script.py
	cd ${root}/scripts && sudo python mn_script.py --log_dir "$(shell dirname $@)"

${root}/logs/6/nginx_access.log: ${root}/scripts/mn_script.py
	cd ${root}/scripts && sudo python mn_script.py --log_dir "$(shell dirname $@)"

${root}/logs/7/nginx_access.log: ${root}/scripts/mn_script.py
	cd ${root}/scripts && sudo python mn_script.py --log_dir "$(shell dirname $@)"

${root}/logs/8/nginx_access.log: ${root}/scripts/mn_script.py
	cd ${root}/scripts && sudo python mn_script.py --log_dir "$(shell dirname $@)"

${root}/logs/9/nginx_access.log: ${root}/scripts/mn_script.py
	cd ${root}/scripts && sudo python mn_script.py --log_dir "$(shell dirname $@)"

${root}/logs/10/nginx_access.log: ${root}/scripts/mn_script.py
	cd ${root}/scripts && sudo python mn_script.py --log_dir "$(shell dirname $@)"

${root}/doc/1/fig.pdf: ${root}/scripts/mn_script.py ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6 ${root}/logs/1/nginx_access.log
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --source ${root}/logs/1

${root}/doc/2/fig.pdf: ${root}/scripts/mn_script.py ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6 ${root}/logs/2/nginx_access.log
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --source ${root}/logs/2

${root}/doc/3/fig.pdf: ${root}/scripts/mn_script.py ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6 ${root}/logs/4/nginx_access.log
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --source ${root}/logs/3

${root}/doc/5/fig.pdf: ${root}/scripts/mn_script.py ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6 ${root}/logs/5/nginx_access.log
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --source ${root}/logs/5

${root}/doc/6/fig.pdf: ${root}/scripts/mn_script.py ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6 ${root}/logs/6/nginx_access.log
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --source ${root}/logs/6

${root}/doc/7/fig.pdf: ${root}/scripts/mn_script.py ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6 ${root}/logs/7/nginx_access.log
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --source ${root}/logs/7

${root}/doc/8/fig.pdf: ${root}/scripts/mn_script.py ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6 ${root}/logs/8/nginx_access.log
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --source ${root}/logs/8

${root}/doc/9/fig.pdf: ${root}/scripts/mn_script.py ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6 ${root}/logs/9/nginx_access.log
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --source ${root}/logs/9

${root}/doc/10/fig.pdf: ${root}/scripts/mn_script.py ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6 ${root}/logs/10/nginx_access.log
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --source ${root}/logs/10

logs:
	@echo 'creating logs'
	mkdir $@

data:
	@echo 'Creating Data directory'
	mkdir $@

stage3-plot: ${root}/doc/1/fig.pdf ${root}/doc/2/fig.pdf ${root}/doc/4/fig.pdf ${root}/doc/5/fig.pdf ${root}/doc/6/fig.pdf ${root}/doc/7/fig.pdf ${root}/doc/8/fig.pdf ${root}/doc/9/fig.pdf ${root}/doc/10/fig.pdf
	@echo 'Generating plots'

stage3-plot-all: ${root}/scripts/net_utils.py ${root}/plotter/bin/python3.6
	@echo 'plotting data'
	/vagrant/plotter/bin/python3.6 /vagrant/scripts/net_utils.py --all

doc:
	@echo 'Creating doc directory'
	mkdir $@
	
