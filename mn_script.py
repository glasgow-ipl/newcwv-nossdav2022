from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
#from mininet.node import OVSController

import time
from threading import Thread


class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=2 ):
	switch = self.addSwitch( 's1' )
	for h in range(n):
	    # Each host gets 50%/n of system CPU
	    host = self.addHost( 'h%s' % (h + 1),
		                 cpu=.5/n )
	    # 10 Mbps, 5ms delay, 2% loss, 1000 packet queue
	    self.addLink( host, switch, bw=10, delay='5ms', loss=2,
                          max_queue_size=1000, use_htb=True )

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
        self.addLink( hosts[0], s1, bw=1, delay='5ms'  )
        self.addLink( hosts[1], s2, bw=1, delay='5ms' )
        self.addLink( s1, s2, bw=1, delay='5ms')


def changeLinkBw(ep1, ep2, in_bw, out_bw=-1):
    link = ep1.connectionsTo(ep2)
    link[0][0].config(**{'bw': in_bw})
    link[0][1].config(**{'bw': out_bw if out_bw != -1 else in_bw})


def run_on_host(host, cmd):
    host.cmdPrint(cmd)


def perfTest():
    "Create network and run simple performance test"
    topo = DumbbellTopo()
    net = Mininet( topo=topo,
	           host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections( net.hosts )
    print "Testing network connectivity"
    net.pingAll()

    h1, h2 = net.get( 'h1', 'h2' )
#CHANGE PYTHON2
    h1.cmdPrint('pwd')

    t = Thread(target=run_on_host, args=(h1, 'python2 server.py'))
    t.start()

    t = Thread(target=run_on_host, args=(h2, 'su - tech -c "nohup firefox --headless --private http://'+ h1.IP() +':8000/player.html"')) 
    t.start()

    s1, s2 = net.get('s1', 's2')
    print 'Waiting for 80 seconds'
    time.sleep(80)
    print 'changing BW'
    changeLinkBw(s1, s2, .5)
    time.sleep(60)
    print 'changing BW'    
    changeLinkBw(s1, s2, 1)
    time.sleep(60)


    print('alive: %s' % t.is_alive()) 
    t.join()
    print('alive: %s' % t.is_alive())
    
    time.sleep(20)

    print('alive: %s' % t.is_alive())

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest()
