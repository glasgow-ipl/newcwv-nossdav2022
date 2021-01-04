#!/bin/bash

# BBR requires pacing. Linux's default qdisc(fq_codel) does NOT support pacing, therefore BBR requires fq in order to operate
sudo sysctl net.core.default_qdisc=fq
sudo sysctl net.ipv4.tcp_congestion_control=bbr
