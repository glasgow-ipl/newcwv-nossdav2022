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
    server.cmd("echo 'events { } http { server { listen " + server_ip + "; root /vagrant; access_log /vagrant/logs/"
         + server_log_name + ";} }' > nginx-conf.conf")

    # Start HTTP server
    server_out = server.cmd("sudo nginx -c " + wd + "/nginx-conf.conf &")

    time.sleep(3)

    net.iperf((client, server))

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
    precise_time_str = "%m-%d-%H:%M:%S:%f"

    print 'changing BW %s ' % datetime.datetime.now().strftime(precise_time_str)
    changeLinkBw(server, s1, .5)
    net.iperf((client, server))
    time.sleep(60)

    print 'changing BW %s ' % datetime.datetime.now().strftime(precise_time_str)    
    changeLinkBw(server, s1, 10)
    net.iperf((client, server))
    time.sleep(80)
    
    # Wait for the last sement to be requested at the server
    #server_thread.join()

    print("Stopping server")
    server.cmd("sudo nginx -s stop")
    print("Closing...")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    doSimulation()
    # test_change_bw()
