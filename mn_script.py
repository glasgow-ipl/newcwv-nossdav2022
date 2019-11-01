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

def perfTest():
    "Create network and run simple performance test"
    topo = SingleSwitchTopo()
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
    h1.cmdPrint('python2 server.py&')
    time.sleep(2)
#CHANGE USER
    #h2.cmd('xterm')
    #h2.cmd('echo "a" > server-output.txt')
    #h2.cmd("runuser -l tech -c 'firefox --private --headless http://"+h1.IP()+":8000/player.html&'")
    #h1.cmdPrint('ls -la')

    t = threading.Thread(target=h2.cmd, args=('xterm',))    
    t.start()
    print 'sleepin`'
    time.sleep(80)
    s1 = net.get('s1')
    print 'changing BW'
    s1.intf().config(bw=5)
    time.sleep(60)
    print 'changing BW'    
    s1.intf().config(bw=10)
    time.sleep(60)
    
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest()
