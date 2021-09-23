#!/usr/bin/bash

vreno_loaded=`sudo sysctl net.ipv4.tcp_available_congestion_control | grep reno_verbose`
echo ${vreno_loaded}

if [ -z "${vreno_loaded}" ]; then
    cd /home/vagrant/verbose_reno
    make
    sudo make install_vreno
fi

sudo sysctl net.ipv4.tcp_congestion_control=reno_verbose