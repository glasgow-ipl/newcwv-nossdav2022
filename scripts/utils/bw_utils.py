import threading
import time
import json
import math
import datetime

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

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
        bdp = _calculate_bdp(bw, RTT)
        print(bdp) 

        # Leaving non-bottleneck links to run at maximum capacity with default parameters
        self.addLink( hosts[0], s1)#, bw=bw, delay='%dms' % delay, max_queue_size=bdp)
        self.addLink( hosts[1], s2)#, bw=bw, delay='%dms' % delay, max_queue_size=bdp)
        self.addLink( s1, s2, bw=bw, delay='%dms' % (RTT/2), max_queue_size=bdp)


precise_time_str = "%y-%m-%d-%H:%M:%S:%f"

def _calculate_bdp(bw, RTT):
    '''
        Returns BDP in MTU sized packets, default MTU=1500
        @bw -> badwidth in Mbps
        @RTT -> round trip time in ms
    '''
    bdp = bw * 1000 # kbps
    bdp /= 8 #kBps
    bdp *= RTT # Bytes
    bdp = math.ceil(bdp / 1500.0) # MTU sized packets
    return int(bdp)


def changeLinkBw(ep1, ep2, in_bw, RTT, logger, out_bw=-1, loss=None):
    msg = 'changing BW %s RTT %s loss %s %s ' % (in_bw, RTT, loss, datetime.datetime.now().strftime(precise_time_str))
    print(msg)
    logger.append(msg)
    link = ep1.connectionsTo(ep2)
    bdp = _calculate_bdp(in_bw, RTT)
    link[0][0].config(**{'bw': in_bw, 'max_queue_size': bdp, 'delay': '%sms' % (RTT / 2), 'loss': loss})
    link[0][1].config(**{'bw': out_bw if out_bw != -1 else in_bw, 'max_queue_size': bdp if out_bw == -1 else _calculate_bdp(out_bw, RTT), 'delay': '%sms' % (RTT / 2)})


def config_bw(conf_file, ep1, ep2, logger):
    delta_time = 0
    with open(conf_file) as f:
        conf = json.load(f)

    if conf.get('repeat'):
        total_time = 0
        pause = conf['pause']
        while(total_time < conf['duration']):
            for entry in conf['changes']:
                wait_for = entry['time'] - delta_time
                time.sleep(wait_for)
                total_time += wait_for

                if total_time > conf['duration']: # Check if we should exit
                    return

                loss = entry['loss'] if entry['loss'] else None
                # Change BW
                changeLinkBw(ep1, ep2, entry['bw'], entry['rtt'], logger, loss=loss)
                delta_time = entry['time']
                
            time.sleep(pause) # wait for PAUSE seconds before looping again
            total_time += pause
            # current_time = (entry['time'] + conf['repeat']) * cycles
            
            delta_time = 0
            
    else:
        for entry in conf['changes']:
            wait_for = entry['time'] - delta_time
            time.sleep(wait_for)
            # Change BW
            changeLinkBw(ep1, ep2, entry['bw'], entry['rtt'], logger)
            delta_time = entry['time']
    

def test():
    topo = DumbbellTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    s1, s2 = net.get('s1', 's2')
    logger = []

    t = threading.Thread(target=config_bw, args=('/vagrant/network_models/dash_if/network_config_1.json', s1, s2, logger))
    t.start()

    t.join()
    net.stop()

if __name__ == '__main__':
    test()
