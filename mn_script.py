from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
#from mininet.node import OVSController
import time

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
        self.addLink( hosts[0], s1, bw=1, delay='5ms', loss=0 )
        self.addLink( hosts[1], s2, bw=1, delay='5ms', loss=0 )
        self.addLink( s1, s2, bw=1, delay='5ms', loss=0)


def changeLinkBw(ep1, ep2, in_bw, out_bw=-1):
    link = ep1.connectionsTo(ep2)
    link[0][0].config(**{'bw': in_bw})
    link[0][1].config(**{'bw': out_bw if out_bw != -1 else in_bw})


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

    import threading
#    t = threading.Thread(target=h1.cmdPrint, args=('python2 server.py',))
#    t.start()
    h1.cmdPrint('python server.py&')
    time.sleep(2)
#CHANGE USER
    #h2.cmd('xterm')
    #h2.cmd('echo "a" > server-output.txt')
    #h2.cmd("runuser -l tech -c 'firefox --private --headless http://"+h1.IP()+":8000/player.html&'")
    #h1.cmdPrint('ls -la')

#    t = threading.Thread(target=h2.cmd, args=('xterm -hold "./last.sh"',))    
    #t = threading.Thread(target=h2.cmd, args=('xterm -hold "/run_chrome.sh"',))
    #t.start()
    h2.cmdPrint('su - vagrant -c "/usr/bin/google-chrome --incognito --disable-application-cahce http://10.0.0.1:8000/player.html&"')
    s1, s2 = net.get('s1', 's2')
    print 'sleepin`'
    time.sleep(80)
    print 'changing BW'
    changeLinkBw(s1, s2, .5)
    time.sleep(60)
    print 'changing BW'    
    changeLinkBw(s1, s2, 1)
    time.sleep(60)
    
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest()
