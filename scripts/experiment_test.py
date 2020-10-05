from mn_script import DumbbellTopo
from mn_script import changeLinkBw

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

import unittest

class TestExperiment(unittest.TestCase):

    def test_dumbbelltopo(self):
        n_hosts = 4
        topo = DumbbellTopo(n_hosts)
        self.assertEqual(len(topo.hosts()), n_hosts)

        topo = DumbbellTopo()
        self.assertEqual(len(topo.hosts()), 2)



class TestMininet(unittest.TestCase):

    _net = None

    def setUp(self):
        topo = DumbbellTopo()
        net = Mininet( topo=topo,
                host=CPULimitedHost, link=TCLink)
        self._net = net
        net.start()


    def tearDown(self):
        print('teardown')
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

        # Check buffer size change

        out = s1.cmd('tc qdisc show dev s1-eth2')
        queue = out.split('\n')[1].split('limit ')[1]
        self.assertEqual(336, queue)

        out = s2.cmd('tc qdisc show dev s2-eth2')
        queue = out.split('\n')[1].split('limit ')[1]
        self.assertEqual(336, queue)

    def test_calculate_bdp(self):
        pass


    def test_tcp_retransmissions_nz(self):
        pass

if __name__ == '__main__':
    unittest.main()