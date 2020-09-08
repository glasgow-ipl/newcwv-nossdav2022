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


class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=2 ):
        switch = self.addSwitch( 's1' )
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost( 'h%s' % (h + 1),
                            cpu=.5/n )
            # 10 Mbps, 5ms delay, 2% loss, 1000 packet queue
            self.addLink( host, switch, bw=1000, delay='5ms',
                             )

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
        self.addLink( hosts[0], s1, bw=10000, delay='5ms'  )
        self.addLink( hosts[1], s2, bw=10000, delay='5ms' )
        self.addLink( s1, s2, bw=10000, delay='5ms')


def changeLinkBw(ep1, ep2, in_bw, out_bw=-1):
    link = ep1.connectionsTo(ep2)
    link[0][0].config(**{'bw': in_bw})
    link[0][1].config(**{'bw': out_bw if out_bw != -1 else in_bw})


def run_on_host(host, cmd):
    host.cmdPrint(cmd)


def test_change_bw():
    topo = SingleSwitchTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    h1, h2 = net.get('h1', 'h2')

    s1 = net.get('s1')
    net.iperf((h1, h2))
    
    changeLinkBw(h1, s1, 10)
    net.iperf((h1, h2))

def doSimulation():
    "Create network and run simple performance test"
    # Create Topology
    topo = DumbbellTopo()
    net = Mininet( topo=topo,
               host=CPULimitedHost, link=TCLink)
    net.start()
    precise_time_str = "%m-%d-%H:%M:%S:%f"

    # Test connectivity
    print("Dumping host connections")
    dumpNodeConnections( net.hosts )
    print("Testing network connectivity")
    net.pingAll()

    

    server, client = net.get( 'h1', 'h2' )
#CHANGE PYTHON2

    # Get server/client config settings
    wd = str(server.cmd('pwd'))[:-2]
    user = os.getlogin()
    server_ip = server.IP()

    # Create server config
    time_str = datetime.datetime.now().strftime('%m-%d-%H%M')
    server_log_name = "%s_nginx_access.log" % time_str

    

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

    print("starting client at: %s" % datetime.datetime.now().strftime(precise_time_str))
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
    print 'changing BW %s ' % datetime.datetime.now().strftime(precise_time_str)
    changeLinkBw(server, s1, .5)
    net.iperf((client, server))
    time.sleep(60)

    print 'changing BW %s ' % datetime.datetime.now().strftime(precise_time_str)    
    changeLinkBw(server, s1, 10)
    net.iperf((client, server))
    time.sleep(80)
    
    print("Waiting for server to finish %s" % datetime.datetime.now().strftime(precise_time_str))
    server.cmd("wait %s " % watchdog_pid)

    time.sleep(2)

    print("Stopping server")
    server.cmd("sudo nginx -s stop")
    print("Closing...")
    net.stop()

    os.system('su - %s -c "/vagrant/scripts/quitff.sh"' % user)


if __name__ == '__main__':
    setLogLevel( 'info' )
    doSimulation()
    # test_change_bw()
