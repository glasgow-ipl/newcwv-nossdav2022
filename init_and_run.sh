vagrant up
vagrant ssh -c "mkdir results && mkdir logs && cd scripts && make gen_mpd && sudo python2 mn_script.py"
