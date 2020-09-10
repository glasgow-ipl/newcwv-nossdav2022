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

import subprocess

class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=2 ):
        switch = self.addSwitch( 's1' )
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost( 'h%s' % (h + 1),
                            cpu=.5/n )
            # 10 Mbps, 5ms delay, 2% loss
            bw = 1000
            delay = 5
            bdp = bw*delay
            self.addLink( host, switch, bw=bw, delay='%dms' % delay, max_queue_size=bdp)

class DumbbellTopo( Topo ):
    "Dumbbell topology with n hosts."
    def build( self, n=2 ):
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        hosts = []
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost( 'h%s' % (h + 1), cpu=.5/n )
            hosts += [host]

        # 10 Mbps, 5ms delay, 2% loss, 1000 packet queue
        bw = 1000
        delay = 5
        bdp = bw*delay
        self.addLink( hosts[0], s1, bw=bw, delay='%dms' % delay, max_queue_size=bdp)
        self.addLink( hosts[1], s2, bw=bw, delay='%dms' % delay, max_queue_size=bdp)
        self.addLink( s1, s2, bw=bw, delay='%dms' % delay, max_queue_size=bdp)


def changeLinkBw(ep1, ep2, in_bw, delay, out_bw=-1):
    link = ep1.connectionsTo(ep2)
    bdp = in_bw * delay
    link[0][0].config(**{'bw': in_bw, 'max_queue_size': bdp})
    link[0][1].config(**{'bw': out_bw if out_bw != -1 else in_bw, 'max_queue_size': bdp})


def run_on_host(host, cmd):
    host.cmdPrint(cmd)


def test_change_bw():
    topo = SingleSwitchTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    h1, h2 = net.get('h1', 'h2')

    s1 = net.get('s1')
    net.iperf((h1, h2))
    
    changeLinkBw(h1, s1, 10, 5)
    net.iperf((h1, h2))
    net.iperf((h1, h2))
    net.iperf((h1, h2))

    setLogLevel('info')
    #print(h1.connectionsTo(s1)[0][0].tc())
    # CLI(net)

def doSimulation():
    "Create network and run simple performance test"

    # Create a list to keep logging events
    logger = []

    # Create Topology
    topo = DumbbellTopo()
    net = Mininet( topo=topo,
               host=CPULimitedHost, link=TCLink)
    net.start()
    precise_time_str = "%m-%d-%H:%M:%S:%f"
    time_stamp = datetime.datetime.now().strftime('%m-%d-%H%M')

    # Test connectivity
    print("Dumping host connections")
    dumpNodeConnections( net.hosts )
    print("Testing network connectivity")
    net.pingAll()

    server, client = net.get( 'h1', 'h2' )
#CHANGE PYTHON2


    pcap_path = os.path.join('/', 'vagrant', 'logs', time_stamp)

    print('tcpdump -w %s' % os.path.join(pcap_path, 'server.pcap'))
    # server.cmdPrint('ls /vagrant/logs')


    s_name = os.path.join(pcap_path, 'server.pcap')
    c_name = os.path.join(pcap_path, 'client.pcap')

    print ('ethtool -K ' + str(server.intf()) + ' gso off')

    # Disable segment offloading for hosts
    server.cmd('ethtool -K ' + str(server.intf()) + ' gso off')
    server.cmd('ethtool --offload ' + str(server.intf()) + ' tso off')
    client.cmd('ethtool -K ' + str(client.intf()) + ' gso off')
    client.cmd('ethtool --offload ' + str(client.intf()) + ' tso off')

    # Create root folder for experiment data
    if os.path.exists(pcap_path):
        print("Os path exists... exiting")
        net.stop()
        sys.exit(1)
    else:
        os.mkdir(pcap_path)

    # Start pcaps on the client and the server
    server_pcap = server.popen('tcpdump -w %s -z gzip' % s_name)
    print(type(server_pcap))
    client_pcap = client.popen('tcpdump -w %s -z gzip' % c_name)
    # Get server/client config settings
    wd = str(server.cmd('pwd'))[:-2]
    user = os.getlogin()
    server_ip = server.IP()

    # Create server config
    server_log_name = os.path.join(time_stamp, "nginx_access.log")

    

    # optionally add buffer=32k (or some other big value for access_log)
    config_str = "events { } http { log_format tcp_info '$time_local, \"$request\", $status, $tcpinfo_rtt, $tcpinfo_rttvar, \"$tcpinfo_snd_cwnd\", $tcpinfo_rcv_space, $body_bytes_sent, \"$http_referer\", \"$http_user_agent\"'; server { listen " + server_ip + "; root /vagrant; access_log /vagrant/logs/" + server_log_name + " tcp_info;} }"
    with open('nginx-conf.conf', 'w') as f:
        f.write(config_str)

    # Start watchdog service

    server.cmd("python watchdog.py &")
    watchdog_pid = server.cmd("echo $!")
    print("watchdog pid: %s" % watchdog_pid)

    # Start HTTP server
    server_out = server.cmd("sudo nginx -c " + wd + "/nginx-conf.conf &")

    time.sleep(3)

    net.iperf((client, server))

    msg = "starting client at: %s" % datetime.datetime.now().strftime(precise_time_str)
    print(msg)
    logger.append(msg)

    client_cmd = 'su - %s -c "nohup firefox --headless --private http://%s/scripts/player.html&"' % (user, server_ip)
    print ("Client cmd: %s " % client_cmd)

    # client_thread = Thread(target=run_on_host, args=(client, client_cmd))
    # client_thread.setDaemon(True) 
    # client_thread.start()

    # CLI(net)

    client.cmd(client_cmd)

    # CLI(net)

    #appClient.cmd("curl http://" + appServer.IP() + "/available-fruits.html")

    #client_thread = Thread(target=run_on_host, args=(h2,
    #         'su - %s -c "nohup firefox --headless --private http://%s:8000/scripts/player.html"' % (user, server_ip) ))
    #client_thread.setDaemon(True) 
    #client_thread.start()

    s1, s2 = net.get('s1', 's2')
    print 'Waiting for 80 seconds'
    time.sleep(80)


    #month-day-hour:minute:second:microsecond
    msg = 'changing BW %s ' % datetime.datetime.now().strftime(precise_time_str)
    print msg
    logger.append(msg)
    changeLinkBw(s1, s2, .5, 5)
    net.iperf((client, server))
    time.sleep(60)

    msg = 'changing BW %s ' % datetime.datetime.now().strftime(precise_time_str)
    print msg
    logger.append(msg)    
    changeLinkBw(s1, s2, 15, 5)
    net.iperf((client, server))
    time.sleep(80)
    
    msg = "Waiting for server to finish %s" % datetime.datetime.now().strftime(precise_time_str)
    print(msg)
    logger.append(msg)

    server.cmd("wait %s " % watchdog_pid)

    logger.append("terminating")

    server_pcap.terminate()
    client_pcap.terminate()

    time.sleep(2)

    print("Stopping server")
    server.cmd("sudo nginx -s stop")
    print("Closing...")
    net.stop()


    logger_path = os.path.join(pcap_path, 'events.log')
    logger = '\n'.join(logger)
    with open(logger_path, 'w') as f:
        f.write(logger)

    os.system('su - %s -c "/vagrant/scripts/quitff.sh"' % user)


if __name__ == '__main__':
    setLogLevel( 'info' )
    doSimulation()
    # test_change_bw()
