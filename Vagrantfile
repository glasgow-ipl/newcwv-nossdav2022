# -*- mode: ruby -*-
# vi: set ft=ruby :

# install mininet + firefox
# install xterm (DEBUG ONLY)
# install ffmpeg (required to play video)


$RUN_PROBE = <<SCRIPT
	service vboxguest enable
	service vboxservice enable

#	pwd
	apt-get update
	apt-get install -y firefox
	apt-get install -y ffmpeg

	git clone git://github.com/mininet/mininet
	cd mininet && git tag && git checkout 2.3.0d6 && cd util && rm install.sh && wget https://gist.githubusercontent.com/janev94/c443075986ec344359904c9ceba93f2b/raw/99c9146940450beb155a31cb5b30c38643466b46/install.sh && chmod u+x install.sh && cd ../..
	echo `pwd`
	export LC_ALL=C
	sudo mininet/util/install.sh -a
  apt-get install -y nginx
  apt-get install -y iperf3

  # Create virtual envrionment for plotting results
  apt-get install -y python3-venv
  apt-get install -y virtualenv
  cd /vagrant && virtualenv plotter -p python3 --always-copy && plotter/bin/pip install -r deps/requirements.txt 
  
  #DNS does not work on some machines, unless some traffic has gone out already
  ping -c 3 google.com 
SCRIPT


Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.box_version = "1.0.282"

  # enable X11 forwarding
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true

  config.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--memory",                 "8192"]
    v.customize ["modifyvm", :id, "--cpus",                      "4"]
    v.customize ["modifyvm", :id, "--hwvirtex",                 "on"]
    v.customize ["modifyvm", :id, "--nestedpaging",             "on"]
    v.customize ["modifyvm", :id, "--largepages",               "on"]
    v.customize ["modifyvm", :id, "--acpi",                     "on"]
    v.customize ["modifyvm", :id, "--apic",                     "on"]
    v.customize ["modifyvm", :id, "--ioapic",                   "on"]
    v.customize ["modifyvm", :id, "--x2apic",                   "on"]
    v.customize ["modifyvm", :id, "--biosapic",             "x2apic"]
    v.customize ["modifyvm", :id, "--hpet",                     "on"]
    v.customize ["modifyvm", :id, "--rtcuseutc",                "on"]
    v.customize ["modifyvm", :id, "--paravirtprovider",        "kvm"]
    v.customize ["modifyvm", :id, "--nictype1",             "virtio"]
    v.customize ["modifyvm", :id, "--nictype2",             "virtio"]
    v.customize ["modifyvm", :id, "--cableconnected1",          "on"]
    v.customize ["modifyvm", :id, "--audio",                  "none"]
    v.customize ["modifyvm", :id, "--usb",                     "off"]
    v.customize ["modifyvm", :id, "--usbehci",                 "off"]
    v.customize ["modifyvm", :id, "--usbxhci",                 "off"]
    v.customize ["modifyvm", :id, "--usbcardreader",           "off"]
#    v.customize ["modifyvm", :id, "--accelerate2dvideo",        "on"]
#    v.customize ["modifyvm", :id, "--accelerate3d",             "on"]
    v.customize ["modifyvm", :id, "--vram",                    "256"]
#    v.customize ["modifyvm", :id, "--graphicscontroller", "VBoxSVGA"]
  end

  config.vm.provision "shell", privileged: true, inline: $RUN_PROBE 

end
