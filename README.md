# NOSSDAV 2022: Does TCP New Congestion Window Validation improve HTTP adaptive video stability

# Hardware Requirements

Before attempting to reproduce the results, we suggest that you use a machine with the following minimal setup:

1. RAM 16 GB
2. Cores 8

# Reproducing the results

The easiest way to reproduce the dataset used in this paper is to use the provided Vagrantfile. This builds a virtual machine and
installs all required dependencies. To obtain a copy of the data using the recommended method do the following:

0. Make sure you have vagrant and some virtualization software (Oracule Virtual Box recommended) installed
1. Clone this repository
2. From within the repository run vagrant up
3. Log into the virtual machine using `vagrant ssh`
4. Navigate to the shared directory `cd /vagrant/`

From there you can use `make` -> To build all dependencies and reproduce the paper, or you can run any of the following commands to carry out individual build steps:

1. `make stage1-mpd-ietf` -> To build the different video encodings required to carry out the simulations
2. `make stage2-logs` -> To produce the data used in this paper _Note: This will execute all previous stages_
3. `make stage3-plots` -> To produce the figures in http://dx.doi.org/10.5525/gla.researchdata.1278 _Note: This will execute all previous stages_
4. `make stage4-paper` -> To produce the a copy of http://dx.doi.org/10.5525/gla.researchdata.1278 _Note: This will execute all previous stages_

## Notes

The Vagrantfile in this repository is tied to VirtualBox.
The dataset was obtained with the following versions of its dependencies:

VirtualBox 6.1.32r149290
Vagrant 2.2.19

Additionally, internal dependency packahges were as follows:

Mozilla Firefox 100.0.2
ffmpeg version 4.2.4-1ubuntu0.1
Python 2.7.18
xorg-server 1.20.13
Python 3.8.10
GNU Make 4.2.1
gcc 9.4.0
nginx 1.18.0
iperf 3.7

Host machine used to produce the original dataset used:
Intel(R) Xeon(R) CPU E5-2609 0 @ 2.40GHz

