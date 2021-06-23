ROOT:=/vagrant

DASH_ALG='abrThroughput'
MPD_LOCATION='data/3s/bbb.mpd'
OUT_DIR=${ROOT}/data
IGNORE_LINK_LOSS=0

logs: ${ROOT}/logs/newcwv/1_reno/nginx_access.log


${ROOT}/logs/newcwv/1_reno/nginx_access.log: ${ROOT}/scripts/mn_script.py ${OUT_DIR}/3s/bbb.mpd | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/dash_if/network_config_1.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs/1/%_newcwv/nginx_access.log: ${ROOT}/scripts/mn_script.py ${out_dir}/3s/bbb.mpd | ${ROOT}/logs
	@echo $@
	cd ${ROOT}/scripts && sudo python mn_script.py --log_dir $(@D) --cong_alg cubic --network_model /vagrant/network_models/links/DSL.json --mpd_location $(MPD_LOCATION) --dash_alg $(DASH_ALG) --ignore_link_loss $(IGNORE_LINK_LOSS)

${ROOT}/logs:
	mkdir ${ROOT}/logs
