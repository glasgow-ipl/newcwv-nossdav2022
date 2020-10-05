from mn_script import DumbbellTopo
from mn_script import changeLinkBw
from mn_script import _calculate_bdp

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

import unittest
import json

class TestExperiment(unittest.TestCase):

    def test_dumbbelltopo(self):
        n_hosts = 4
        topo = DumbbellTopo(n_hosts)
        self.assertEqual(len(topo.hosts()), n_hosts)

        topo = DumbbellTopo()
        self.assertEqual(len(topo.hosts()), 2)

    def test_calculate_bdp(self):
        bdp = _calculate_bdp(42, 7)
        self.assertEqual(25, bdp)


class TestMininet(unittest.TestCase):

    _net = None

    def setUp(self):
        topo = DumbbellTopo()
        net = Mininet( topo=topo,
                host=CPULimitedHost, link=TCLink)
        self._net = net
        self._topo = topo
        net.start()


    def tearDown(self):
        self._net.stop()


    def test_changeSpeed(self):
        net = self._net
        s1, s2 = net.get('s1', 's2')

        # Check Bandwidth change
        cmd = 'tc class show dev %s'
        intf = 's1-eth2' 

        speed = 42 # Mbps
        expected_speed_str = '42Mbit'
        delay = 7 # ms
        changeLinkBw(s1, s2, speed, delay)
        
        out = s1.cmd(cmd % (intf))
        tc_speed = out.split('rate ')[1].split(' ', 1)[0]
        self.assertEqual(expected_speed_str, tc_speed)

        intf = 's2-eth2'
        out = s2.cmd(cmd % (intf))
        tc_speed = out.split('rate ')[1].split(' ', 1)[0]
        self.assertEqual(expected_speed_str, tc_speed)

        # Check buffer size change 24 -> Calculated buffer for  42Mbps and 7ms delay

        out = s1.cmd('tc qdisc show dev s1-eth2')
        queue = out.split('\n')[1].split('limit ')[1]
        queue = int(queue.strip())
        self.assertEqual(25, queue)

        out = s2.cmd('tc qdisc show dev s2-eth2')
        queue = out.split('\n')[1].split('limit ')[1]
        queue = int(queue.strip())
        self.assertEqual(25, queue)
        

    def test_tcp_retransmissions_nz(self):
        net = self._net
        topo = self._topo

        server, client = net.get('h1', 'h2')

        s1, s2 = net.get('s1', 's2')

        # Set bottleneck link of 50Mbps
        changeLinkBw(s1, s2, 50, topo._RTT)

        server.cmd('iperf3 -s&')

        print("running iperf3 for 30 seconds")
        out = client.cmd('iperf3 -c ' + server.IP() + ' -J -t 30')
        out = json.loads(out)

        # For 30 seconds we should have had at least 15 retransmits, realistically, the number will be way bigger
        self.assertGreater(out['end']['sum_sent']['retransmits'], 15)


if __name__ == '__main__':
    unittest.main()