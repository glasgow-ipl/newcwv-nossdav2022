from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
#from mininet.node import OVSController

import time
from threading import Thread
import os
import datetime
import sys
import server
import math
import argparse
import generate_player

import subprocess

from utils import bw_utils

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
        self.addLink( hosts[0], s1)#, bw=bw, delay='%dms' % delay, max_queue_size=bdp)
        self.addLink( hosts[1], s2)#, bw=bw, delay='%dms' % delay, max_queue_size=bdp)
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

def doSimulation(log_root=None, cong_alg=None, network_model_file=None, mpd_location=None, dash_alg=None, ignore_link_loss=None):
    "Create network and run simple performance test"

    # Create a list to keep logging events
    logger = []
    # Create Topology
    topo = DumbbellTopo()
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

    server, client = net.get( 'h1', 'h2' ) # Hosts
    s1, s2 = net.get('s1', 's2') # Switches

    # If congestion control algorithm was specified, enable that algortithm on the server
    if cong_alg:
        print("Enabling " + cong_alg + " at the server...")
        server.cmd('sudo /vagrant/scripts/enable_' + cong_alg + '.sh')
    else:
        print("No congestion control algorithm specified")


    server.cmdPrint("sudo sysctl net.ipv4.tcp_congestion_control")
#    server.cmdPrint("sudo sysctl net.core.default_qdisc")


    if not log_root:
        pcap_path = os.path.join('/', 'vagrant', 'logs', time_stamp)
    else:
        pcap_path = os.path.normpath(log_root)

    print('tcpdump -w %s' % os.path.join(pcap_path, 'server.pcap'))

    s_name = os.path.join(pcap_path, 'server.pcap')
    c_name = os.path.join(pcap_path, 'client.pcap')

    print ('ethtool -K ' + str(server.intf()) + ' gso off')

    # Disable segment offloading for hosts
    for host in [server, client]:
        host.cmd('ethtool -K ' + str(server.intf()) + ' gso off')
        host.cmd('ethtool --offload ' + str(server.intf()) + ' tso off')

    # Create root folder for experiment data
    if os.path.exists(pcap_path):
        print("Os path exists... exiting")
        net.stop()
        sys.exit(1)
    else:
        os.makedirs(pcap_path)


    # Start pcaps on the client and the server
    server_pcap = server.popen('tcpdump -w %s -z gzip' % s_name)
    print(type(server_pcap))
    client_pcap = client.popen('tcpdump -w %s -z gzip' % c_name)
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
    config_str = "events { } http { log_format tcp_info '$time_local, $msec, \"$request\", $status, $tcpinfo_rtt, $tcpinfo_rttvar, \"$tcpinfo_snd_cwnd\", $tcpinfo_rcv_space, $body_bytes_sent, \"$http_referer\", \"$http_user_agent\"'; keepalive_requests 10000; server { listen " + server_ip + "; root /vagrant; access_log " + server_log_name + " tcp_info;} }"
    print(config_str)
    with open('nginx-conf.conf', 'w') as f:
        f.write(config_str)

    # Start watchdog service
    server.cmd("python watchdog.py &")
    watchdog_pid = server.cmd("echo $!")
    print("watchdog pid: %s" % watchdog_pid)

    # Start HTTP server
    server_out = server.cmd("sudo nginx -c " + wd + "/nginx-conf.conf &")

    # Create player.html
    generate_player.generate_player(mpd_location=mpd_location, dash_alg=dash_alg)

    time.sleep(3)

    bw_manager = Thread(target=bw_utils.config_bw, args=(network_model_file, s1, s2, logger, ignore_link_loss))
    bw_manager.start()
    time.sleep(1)

    # bw_utils.changeLinkBw(s1, s2, bw_speed, topo._RTT)

    net.iperf((client, server))

    firefox_output = os.path.join(pcap_path, "browser_out.txt")
    firefox_log_format = "timestamp,rotate:200,nsHttp:5,cache2:5,nsSocketTransport:5,nsHostResolver:5,cookie:5"
    client_cmd = 'su - %s -c "firefox --headless --private http://%s/scripts/player.html --MOZ_LOG=%s --MOZ_LOG_FILE=%s &"' % (user, server_ip, firefox_log_format, firefox_output)

    client_cmd = 'su - %s -c "firefox --headless --private http://%s/scripts/player.html&"' % (user, server_ip)

    print ("Client cmd: %s " % client_cmd)

    print('1. Open xterm at the client. Run: xterm h2.\n2. In the newly opened terminal, open Firefox as a non-root user by running: su - %s -c "firefox"\n2. In firefox navigate to http://%s/scripts/player.html and wait for the video to playout' % (user, server_ip) )
    CLI(net)

    # msg = "starting client at: %s" % datetime.datetime.now().strftime(precise_time_str)
    # print(msg)
    # logger.append(msg)

    # client.cmd(client_cmd)
    #client.cmdPrint('python /vagrant/scripts/scratch/start_chrome.py')

    # print('Waiting for 80 seconds')
    # time.sleep(80)


    #month-day-hour:minute:second:microsecond
    # bw_speed = .5
    # msg = 'changing BW %s %s ' % (bw_speed, datetime.datetime.now().strftime(precise_time_str))
    # print(msg)
    # logger.append(msg)

    # changeLinkBw(s1, s2, bw_speed, topo._RTT)
    # net.iperf((client, server))
    # time.sleep(60)

    # bw_speed = 15
    # msg = 'changing BW to %s %s ' % (bw_speed, datetime.datetime.now().strftime(precise_time_str) )
    # print(msg)

    # logger.append(msg)    
    # changeLinkBw(s1, s2, bw_speed, topo._RTT)
    # net.iperf((client, server))
    # time.sleep(80)
    
    # msg = "Waiting for server to finish %s" % datetime.datetime.now().strftime(precise_time_str)
    # print(msg)
    # logger.append(msg)

    # server.cmd("wait %s " % watchdog_pid)

    logger.append("terminating")

    server_pcap.terminate()
    client_pcap.terminate()

    time.sleep(2)

    bw_manager.join()

    print("Stopping firefox instances")
    client.cmd("sudo killall firefox")


    print("Stopping server")
    server.cmd("sudo nginx -s stop")
    print("Closing...")
    net.stop()

    # Move dashjs_metrics file to relevant directory
    if os.path.exists('dashjs_metrics.json'):
        print("Saving dash metrics to %s" % pcap_path)
        os.system('mv dashjs_metrics.json %s' % pcap_path)
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

    # remove player.html
    # os.remove('player.html')

    logger_path = os.path.join(pcap_path, 'events.log')
    logger = '\n'.join(logger)
    with open(logger_path, 'w') as f:
        f.write(logger)

    os.system('su - %s -c "/vagrant/scripts/quitff.sh"' % user)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--log_dir', help="Root directory for the generated logs")

    parser.add_argument('--cong_alg', help="Congestion control algorithm to use for the simulation")

    parser.add_argument('--network_model', help="A JSON file, that contains data for BW and RTT changes required during the experiment")

    parser.add_argument('--dash_alg', help="DASH algorithm to be used by the player {abrThroughput, abrDynamic, abrBola}", default='abrThroughput')

    parser.add_argument('--mpd_location', help="MPD location relative to the web server's root (/vagrant)", default='data/bbb.mpd')

    parser.add_argument('--ignore_link_loss', help="1 if link loss characteristics should be ignored 0 to apply them. Default 0", default=0, type=int)

    args = parser.parse_args()
    log_dir = args.log_dir

    cong_alg = args.cong_alg

    network_model_file = args.network_model

    dash_alg = args.dash_alg

    mpd_location = args.mpd_location

    ignore_link_loss = args.ignore_link_loss

    setLogLevel( 'info' )
    doSimulation(log_root=log_dir, cong_alg=cong_alg, network_model_file=network_model_file, dash_alg=dash_alg, mpd_location=mpd_location, ignore_link_loss=ignore_link_loss)
