ROOT:=/vagrant

DASH_ALG=abrThroughput
MPD_LOCATION=data/3s/bbb.mpd
OUT_DIR=${ROOT}/data
IGNORE_LINK_LOSS=0

REPEAT = 5
RUNS = $(shell seq 1 ${REPEAT})
ALGS = vreno newcwv
LINKS = DSL FTTC FTTP

LOGS = $(foreach link, ${LINKS}, $(foreach alg, ${ALGS}, $(foreach run_instance, ${RUNS}, ${ROOT}/logs/newcwv/${link}/${run_instance}_${alg}/nginx_access.log)))

logs: ${LOGS}

${ROOT}/logs/newcwv/DSL/%_vreno/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg vreno --network_model /vagrant/network_models/links/DSL.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/DSL/%_newcwv/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/links/DSL.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/FTTC/%_vreno/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg vreno --network_model /vagrant/network_models/links/FTTC.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/FTTC/%_newcwv/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/links/FTTC.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/FTTP/%_vreno/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg vreno --network_model /vagrant/network_models/links/FTTP.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/newcwv/FTTP/%_newcwv/nginx_access.log: ${ROOT}/scripts/mn_script.py ${ROOT}/${MPD_LOCATION} | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg newcwv --network_model /vagrant/network_models/links/FTTP.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)


${ROOT}/logs:
	mkdir ${ROOT}/logs
