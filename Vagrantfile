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

	git clone git://github.com/mininet/mininet
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
#    v.customize ["modifyvm", :id, "--hwvirtex",                 "on"]
#    v.customize ["modifyvm", :id, "--nestedpaging",             "on"]
#    v.customize ["modifyvm", :id, "--largepages",               "on"]
#    v.customize ["modifyvm", :id, "--acpi",                     "on"]
#    v.customize ["modifyvm", :id, "--apic",                     "on"]
#    v.customize ["modifyvm", :id, "--ioapic",                   "on"]
#    v.customize ["modifyvm", :id, "--x2apic",                   "on"]
#    v.customize ["modifyvm", :id, "--biosapic",             "x2apic"]
#    v.customize ["modifyvm", :id, "--hpet",                     "on"]
#    v.customize ["modifyvm", :id, "--rtcuseutc",                "on"]
#    v.customize ["modifyvm", :id, "--paravirtprovider",        "kvm"]
#    v.customize ["modifyvm", :id, "--nictype1",             "virtio"]
#    v.customize ["modifyvm", :id, "--nictype2",             "virtio"]
#    v.customize ["modifyvm", :id, "--cableconnected1",          "on"]
#    v.customize ["modifyvm", :id, "--audio",                  "none"]
#    v.customize ["modifyvm", :id, "--usb",                     "off"]
#    v.customize ["modifyvm", :id, "--usbehci",                 "off"]
#    v.customize ["modifyvm", :id, "--usbxhci",                 "off"]
#    v.customize ["modifyvm", :id, "--usbcardreader",           "off"]
#    v.customize ["modifyvm", :id, "--accelerate2dvideo",        "on"]
#    v.customize ["modifyvm", :id, "--accelerate3d",             "on"]
    v.customize ["modifyvm", :id, "--vram",                    "256"]
   v.customize ["modifyvm", :id, "--graphicscontroller", "VBoxSVGA"]
  end

  config.vm.provision "shell", privileged: true, inline: $RUN_PROBE 

end
