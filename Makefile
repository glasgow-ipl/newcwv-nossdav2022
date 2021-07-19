ROOT:=/vagrant

DASH_ALG=abrThroughput
MPD_LOCATION=data/ietf/bbb.mpd
OUT_DIR=${ROOT}/data
IGNORE_LINK_LOSS=0

REPEAT = 7
RUNS = $(shell seq 1 ${REPEAT})
ALGS = reno vreno newcwv
LINKS = FTTP FTTC DSL

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

# Tools to build before the PDF files. This is a list of executable files in
# the bin/ directory:
TOOLS = 


# Master build rule:
paper: check-make git-revision $(TOOLS) $(PDF_FILES) 

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