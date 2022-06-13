# -*- mode: ruby -*-
# vi: set ft=ruby :


$RUN_PROBE = <<SCRIPT
	service vboxguest enable
	service vboxservice enable

#	pwd
	apt-get update
	apt-get install -y firefox
	apt-get install -y ffmpeg

	apt-get install -y python2
	apt-get install -y net-tools

  apt-get install -y xterm
  apt-get install -y xvfb

	sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 2
	sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1

  # Get pip 2, so that mininet installation later is happy
  curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
  sudo python2 get-pip.py

  apt-get install -y make
  apt-get install -y gcc

	git clone https://github.com/mininet/mininet
	echo `pwd`
	export LC_ALL=C
	# Cannot use -a flag on install.sh as pox requires python-scapy package which is no longer supported in 20.04
	sudo mininet/util/install.sh -fnv
	apt-get install -y nginx
	apt-get install -y iperf3
  cd /vagrant/deps && python3 enable_high_precision.py
  cd /home/vagrant
  git clone https://github.com/janev94/verbose_reno && cd verbose_reno && git checkout dash_verbose
  cd /home/vagrant
  git clone https://github.com/janev94/newcwv 

  # Required to build the figures
  apt-get install -y python3-pip
  pip3 install -r /vagrant/deps/requirements.txt

  # Required to build the paper
  apt-get install -y texlive-latex-extra
  apt-get install -y texlive-fonts-extra

  # Required to verify the paper build
  apt-get install -y poppler-utils
SCRIPT


Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.box_version = "20201103.0.0"
  
  # enable X11 forwarding
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true

  config.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--memory",                 "16384"]
    v.customize ["modifyvm", :id, "--cpus",                      "8"]
    v.customize ["modifyvm", :id, "--vram",                    "256"]
   v.customize ["modifyvm", :id, "--graphicscontroller", "VBoxSVGA"]
  end

  config.vm.provision "shell", privileged: true, inline: $RUN_PROBE
  
  #config.vm.network :forwarded_port, guest: 22, host: 2299, id: 'ssh'
  config.vm.synced_folder ".", "/vagrant", mount_options: ["dmode=755", "fmode=664"]

end
