from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
#from mininet.node import OVSController

import random
import time
from threading import Thread
import os
import datetime
import sys
import server
import math
import argparse
import generate_player
import glob
import threading

import subprocess

from utils import bw_utils
from check_playtime import check_playtime

bw_init = None
class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=2 ):
        switch = self.addSwitch( 's1' )
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost( 'h%s' % (h + 1),
                            cpu=.5/n )
            # 10 Mbps, 5ms delay, 2% loss
            delay = 5
            bdp = bw_init*delay
            self.addLink( host, switch, bw=bw_init, delay='%dms' % delay, max_queue_size=bdp)

class DumbbellTopo( Topo ):
    "Dumbbell topology with n hosts."

    _bw = None
    _RTT = None

    _hosts = 0

    def build( self, n=2 ):
        if n != 2:
            print("Building topo with %s nodes" % n)
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        hosts = []
        for h in range(n):
            host = self.addHost( 'h%s' % (h + 1))
            hosts += [host]

        # 10 Mbps, 5ms delay, 2% loss, 1000 packet queue
        bw = 50 #Mbps
        global bw_init
        bw_init = self._bw = bw
        RTT = self._RTT = 70 #ms
        bdp = bw_utils._calculate_bdp(bw, RTT)
        print(bdp) 

        # Leaving non-bottleneck links to run at maximum capacity with default parameters
        for i in range(len(hosts)):
            self.addLink(hosts[i], s1 if i % 2 == 0 else s2)#, bw=bw, delay='%dms' % delay, max_queue_size=bdp)

        self.addLink( s1, s2, bw=bw, delay='%dms' % (RTT/2), max_queue_size=bdp)


def run_on_host(host, cmd):
    host.cmdPrint(cmd)


def test_change_bw():
    topo = SingleSwitchTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    h1, h2 = net.get('h1', 'h2')

    s1 = net.get('s1')
    net.iperf((h1, h2))
    
    bw_utils.changeLinkBw(h1, s1, 10, 5)
    net.iperf((h1, h2))
    net.iperf((h1, h2))
    net.iperf((h1, h2))

    setLogLevel('info')

def doSimulation(log_root=None, cong_alg=None, network_model_file=None, mpd_location=None, dash_alg=None, ignore_link_loss=None, clients=1):
    "Create network and run simple performance test"

    # Create a list to keep logging events
    logger = []

    # Check if there are enough profiles to run firefox
    print("Checking if firefox can initiate %s clients" % clients)

    for i in range(clients):
        if not glob.glob('/home/vagrant/.mozilla/firefox/*client%s' % (i + 1)):
            print("Creating Firefox Client Profile %s" % (i + 1))
            os.system('su - vagrant -c "xvfb-run -e /vagrant/scripts/xvfb_error.log firefox -CreateProfile client%s"' % (i + 1))

    print("Ok")

    # Create Topology
    topo = DumbbellTopo(n=clients * 2)
    net = Mininet( topo=topo,
               host=CPULimitedHost, link=TCLink)
    logger.append('initial link speed: %sMbps' % bw_init)

    net.start()
    precise_time_str = "%y-%m-%d-%H:%M:%S:%f"
    time_stamp = datetime.datetime.now().strftime('%y-%m-%d-%H%M')

    # Test connectivity
    print("Dumping host connections")
    dumpNodeConnections( net.hosts )
    print("Testing network connectivity")
    net.pingAll()

    server = net.get( 'h1' ) # server
    client_hosts = []
    for i in range(clients):
        client_hosts.append(net.get('h%s' % ((i+1) * 2))) # clients

    s1, s2 = net.get('s1', 's2') # Switches

    # If congestion control algorithm was specified, enable that algortithm on the server
    if cong_alg:
        print("Enabling " + cong_alg + " at the server...")
        server.cmd('sudo bash /vagrant/scripts/enable_' + cong_alg + '.sh')
    else:
        print("No congestion control algorithm specified")


    server.cmdPrint("sudo sysctl net.ipv4.tcp_congestion_control")

#    server.cmdPrint("sudo sysctl net.core.default_qdisc")


    if not log_root:
        pcap_path = os.path.join('/', 'vagrant', 'logs', time_stamp)
    else:
        pcap_path = os.path.normpath(log_root)

    print('tcpdump -s 200 -w %s' % os.path.join(pcap_path, 'server.pcap'))

    print ('ethtool -K ' + str(server.intf()) + ' gso off')

    # Disable segment offloading for hosts
    hosts = [server]
    hosts.extend(client_hosts)
    for host in hosts:
        host.cmd('ethtool -K ' + str(host.intf()) + ' gso off')
        host.cmd('ethtool --offload ' + str(host.intf()) + ' tso off')

    # Create root folder for experiment data
    if os.path.exists(pcap_path):
        print("Os path exists... exiting")
        net.stop()
        sys.exit(1)
    else:
        os.makedirs(pcap_path)


    # Start pcaps on the client and the server
    s_name = os.path.join(pcap_path, 'server.pcap')
    server_pcap = server.popen('tcpdump -s 200 -w %s -z gzip' % s_name)

    client_pcaps = []    
    for client in client_hosts:
        c_addr = client.IP()
        c_addr.replace('.', '_')
        c_name = os.path.join(pcap_path, 'client_%s.pcap' % c_addr)
        client_pcap = client.popen('tcpdump -s 200 -w %s -z gzip' % c_name)
        client_pcaps.append(client_pcap)

    # Get server/client config settings
    wd = str(server.cmd('pwd'))[:-2]
    user = os.getlogin()
    server_ip = server.IP()


    # Clear previous kernel logs
    server.cmd('echo "" > /var/log/kern.log')
    print("Kernel logs cleared")

    # Create server config
    #server_log_name = os.path.join(time_stamp, "nginx_access.log")
    server_log_name = os.path.join(pcap_path, "nginx_access.log")

    # optionally add buffer=32k (or some other big value for access_log)
    config_str = "events { } http { log_format tcp_info '$time_local, $msec, \"$request\", $status, $tcpinfo_rtt, $tcpinfo_rttvar, \"$tcpinfo_snd_cwnd\", $tcpinfo_rcv_space, $body_bytes_sent, \"$http_referer\", \"$http_user_agent\", $remote_addr'; keepalive_requests 10000; server { listen " + server_ip + "; root /vagrant; access_log " + server_log_name + " tcp_info;} }"
    print(config_str)
    with open('nginx-conf.conf', 'w') as f:
        f.write(config_str)

    # Start watchdog service
    server.cmd("python watchdog.py %s &" % clients)
    watchdog_pid = server.cmd("echo $!")
    print("watchdog pid: %s" % watchdog_pid)

    # Start HTTP server
    server.cmd("sudo nginx -c " + wd + "/nginx-conf.conf &")

    # Create player.html for clients to use
    generate_player.generate_player(mpd_location=mpd_location, dash_alg=dash_alg)

    time.sleep(3)

    bw_manager = Thread(target=bw_utils.config_bw, args=(network_model_file, s1, s2, logger, ignore_link_loss))
    bw_manager.start()
    time.sleep(1)

    firefox_output = os.path.join(pcap_path, "browser_out.txt")
    firefox_log_format = "timestamp,rotate:200,nsHttp:5,cache2:5,nsSocketTransport:5,nsHostResolver:5,cookie:5"

    start_times = []
    for _ in range(len(client_hosts) - 1):
        # generate start times for the clients randomly within the first 5 minutes
        start_times.append(random.randint(0, 60*5))

    start_times = sorted(start_times)
    if len(start_times) > 1:
        start_times = [start_times[i+1] - start_times[i] for i in range(len(start_times) - 1)]
    
    start_times = [0] + start_times
    msg = "Client start times " + str(start_times)
    print(msg)
    logger.append(msg)

    for idx, client in enumerate(client_hosts):
        client_cmd = 'su - %s -c "xvfb-run -a -e /vagrant/xvfb_error.log firefox -P client%s --private http://%s/scripts/player.html http://%s/scripts/player.html&"' % (user, (idx + 1), server_ip, server_ip)

        print ("Client cmd: %s " % client_cmd)
        if idx != 0:
            time.sleep(start_times[idx])
        
        client.cmd(client_cmd)
 
    msg = "Waiting for server to finish %s" % datetime.datetime.now().strftime(precise_time_str)
    print(msg)
    logger.append(msg)

    server.cmd("wait %s " % watchdog_pid)

    logger.append("terminating")

    server_pcap.terminate()
    for client_pcap in client_pcaps:
        client_pcap.terminate()

    time.sleep(2)

    bw_manager.join()

    print("Stopping firefox instances")
    for client in client_hosts:
        client.cmd("sudo killall firefox")


    print("Stopping server")
    server.cmd("sudo nginx -s stop")
    print("Closing...")
    net.stop()


    # Xvfb sometimes does not quit after its process has ended.
    # For sanity and to preserve system memory, make sure all heavy processes are killed after each simulation
    os.system("killall nginx")
    os.system("killall firefox")
    os.system("killall Xvfb")


    # Move dashjs_metrics file to relevant directory
    if glob.glob('dashjs_metrics_*.json'):
        print("Saving dash metrics to %s" % pcap_path)
        os.system('mv dashjs_metrics_*.json %s' % pcap_path)
    else:
        print("Dash metrics not found")

    # Move dashjs_metrics file to relevant directory
    if os.path.exists('dashjs_estimates.json'):
        print("Saving dash estimates to %s" % pcap_path)
        os.system('mv dashjs_estimates.json %s' % pcap_path)
    else:
        print("Dash estimates not found")


    # copy kernel logs
    os.system('sudo cp /var/log/kern.log %s' % pcap_path)

    logger_path = os.path.join(pcap_path, 'events.log')
    logger = '\n'.join(logger)
    with open(logger_path, 'w') as f:
        f.write(logger)

    os.system('su - %s -c "bash /vagrant/scripts/quitff.sh"' % user)

    # if we got to here everything is good, remove the event_log.json we do not need it anymore
    for entry in glob.glob("event_log_*.json"):
        print("Removing event log %s" % entry)
        os.remove(entry)

    for entry in glob.glob(os.path.join(pcap_path, 'dashjs_metrics_client_*')):
        check_playtime(os.path.join('/vagrant', mpd_location), entry)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--log_dir', help="Root directory for the generated logs")

    parser.add_argument('--cong_alg', help="Congestion control algorithm to use for the simulation")

    parser.add_argument('--network_model', help="A JSON file, that contains data for BW and RTT changes required during the experiment")

    parser.add_argument('--dash_alg', help="DASH algorithm to be used by the player {abrThroughput, abrDynamic, abrBola}", default='abrThroughput')

    parser.add_argument('--mpd_location', help="MPD location relative to the web server's root (/vagrant)", default='data/bbb.mpd')

    parser.add_argument('--ignore_link_loss', help="1 if link loss characteristics should be ignored 0 to apply them. Default 0", default=0, type=int)

    parser.add_argument('--clients', help="Number of concurrent video streams to run", default=1, type=int)

    args = parser.parse_args()
    log_dir = args.log_dir

    cong_alg = args.cong_alg

    network_model_file = args.network_model

    dash_alg = args.dash_alg

    mpd_location = args.mpd_location

    ignore_link_loss = args.ignore_link_loss

    clients = args.clients

    fails = 0
    while True:
        t = threading.Thread(target=doSimulation, args=(log_dir, cong_alg, network_model_file, mpd_location, dash_alg, ignore_link_loss, clients))
        t.setDaemon(True)
        t.start()

        WAIT_TIME = 40*60 # 40 minutes
        # Wait for the simulation thread to complete for 40 minutes
        # then cleanup and record unsuccessful event
        t.join(WAIT_TIME)

        if not t.is_alive():
            # If the thread completed successfully in the time interval, terminate the execution
            break

        fails += 1
        os.system("killall nginx")
        os.system("killall firefox")
        os.system("killall Xvfb")
        os.system("rm -rf " + log_dir)
        os.system("sudo mn -c")
        os.system('su - %s -c "bash /vagrant/scripts/quitff.sh"' % os.getlogin())
        os.system("touch /vagrant/rerun/" + log_dir.replace("/", "_") + str(fails))

