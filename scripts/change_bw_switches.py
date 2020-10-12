from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

import os
import time

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
        bw = 200
        delay = 5
        bdp = bw*delay
        self.addLink( hosts[0], s1, delay='%dms' % delay, max_queue_size=bdp)
        self.addLink( hosts[1], s2, delay='%dms' % delay, max_queue_size=bdp)
        self.addLink( s1, s2, bw=bw, delay='%dms' % delay, max_queue_size=bdp)

def changeLinkBw(ep1, ep2, in_bw, delay, out_bw=-1):
    link = ep1.connectionsTo(ep2)
    bdp = in_bw * delay
    link[0][0].config(**{'bw': in_bw, 'max_queue_size': bdp})
    link[0][1].config(**{'bw': out_bw if out_bw != -1 else in_bw, 'max_queue_size': bdp})

def simulate_change_bw():
    topo = DumbbellTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)

    net.start()

    h1, h2 = net.get('h1', 'h2')
    s1, s2 = net.get('s1', 's2')

    tcpdump = h1.popen('tcpdump -w test.pcap')

    h1.cmd('ping 10.0.0.1 -c 3')

    tcpdump.terminate()

    # print("Before changing the link")
    # net.iperf((h1, h2))
    # net.iperf((h1, h2))
    # net.iperf((h1, h2))
    # net.iperf((h1, h2))


    # changeLinkBw(s1, s2, 10, 5)

    # print("Changing the link")
    # time.sleep(3)

    # print("After changing the link")
    # net.iperf((h1, h2))
    # net.iperf((h1, h2))
    # net.iperf((h1, h2))
    # net.iperf((h1, h2))

    # CLI(net)

    net.stop()

if __name__ == '__main__':
    simulate_change_bw()