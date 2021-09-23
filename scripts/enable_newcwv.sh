#!/usr/bin/bash

newcwv_loaded=`sudo sysctl net.ipv4.tcp_available_congestion_control | grep newcwv`
echo ${newcwv_loaded}

if [ -z "${newcwv_loaded}" ]; then
    cd /home/vagrant/newcwv
    sudo make
    sudo make install_newcwv
fi

sudo sysctl net.ipv4.tcp_congestion_control=newcwv
