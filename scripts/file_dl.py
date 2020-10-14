from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

import os
import datetime
import sys
import time

import re
from subprocess import Popen, PIPE

done = False

def monitor_qlen(iface, interval_sec = 0.01, fname='./qlen.txt'):
    global done
    pat_queued = re.compile(r'backlog\s[^\s]+\s([\d]+)p')
    cmd = "tc -s qdisc show dev %s" % (iface)
    ret = []
    open(fname, 'w').write('')
    while 1 and not done:
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.stdout.read()
        # Not quite right, but will do for now
        matches = pat_queued.findall(output)
        if matches and len(matches) > 1:
            ret.append(matches[1])
            t = "%f" % time.time()
            open(fname, 'a').write(t + ',' + matches[1] + '\n')
        time.sleep(interval_sec)
    #open('qlen.txt', 'w').write('\n'.join(ret))
    return


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

        # 60 Mbps, 70ms delay
        bw = 5
        RTT = 70 # Average delay for netflix <-> host
        delay = RTT / 3 # we have 3 links in our setup
        bdp = bw*RTT # kbps
        bdp = bdp * 1000 #bps
        bdp = bdp / 8 # Bps
        bdp = bdp / 1500 # Buffer expressed in packets where MTU = 1500
        print(bdp)
        self.addLink( hosts[0], s1, bw=bw, delay='%dms' % delay, max_queue_size=bdp)
        self.addLink( hosts[1], s2, bw=bw, delay='%dms' % delay, max_queue_size=bdp)
        self.addLink( s1, s2, bw=bw, delay='%dms' % delay, max_queue_size=bdp)


def main():

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

    data_root = os.path.join('/', 'vagrant', 'logs', 'sanatisation', datetime.datetime.now().strftime('%m-%d-%H%M')) 
    if os.path.isdir(data_root):
        print('Data folder already exists. Exiting...')
        net.stop()
        sys.exit(1)
    else:
        os.mkdir(data_root)

    s_name = os.path.join(data_root, 'server.pcap')
    c_name = os.path.join(data_root, 'client.pcap')

    print ('ethtool -K ' + str(server.intf()) + ' gso off')

    # Disable segment offloading for hosts
    server.cmd('ethtool -K ' + str(server.intf()) + ' gso off')
    server.cmd('ethtool --offload ' + str(server.intf()) + ' tso off')
    client.cmd('ethtool -K ' + str(client.intf()) + ' gso off')
    client.cmd('ethtool --offload ' + str(client.intf()) + ' tso off')

    services = []
    
    server_pcap = server.popen('tcpdump -w %s -z gzip' % s_name)
    services.append(server_pcap)
    
    client_pcap = client.popen('tcpdump -w %s -z gzip' % c_name)
    services.append(client_pcap)



    server_log_name = os.path.join(data_root, "nginx_access.log")

    # optionally add buffer=32k (or some other big value for access_log)
    config_str = "events { } http { log_format tcp_info '$time_local, $msec, \"$request\", $status, $tcpinfo_rtt, $tcpinfo_rttvar, \"$tcpinfo_snd_cwnd\", $tcpinfo_rcv_space, $body_bytes_sent, \"$http_referer\", \"$http_user_agent\"'; server { listen " + server.IP() + "; root /vagrant; access_log " + server_log_name + " tcp_info;} }"
    with open('nginx-conf.conf', 'w') as f:
        f.write(config_str)

    wd = str(server.cmd('pwd'))[:-2]

    # Start HTTP server
    conf_path = os.path.join(wd, 'nginx-conf.conf')
    print(conf_path)

    # Start monitoring the q_len at all routers
    # for intf in ['s1-eth1', 's1-eth2', 's2-eth1', 's2-eth2']:
    #     monitor_path = os.path.join(data_root, intf)
    #     monitor_qlen(intf, fname=monitor_path)

    # Iperf client pushes data onto the server -> server should act as client and vice versa
    iperf_server = client.popen("iperf3 -s")
    services.append(iperf_server)

    print('server started')
    # server_out = server.cmd("sudo nginx -c " + conf_path + " &")

    iperf_out_path = os.path.join(data_root, "iperf_client.json")
    # print()
    iperf_client = server.popen("iperf3 -c " + client.IP() + " -t 240 --logfile " + iperf_out_path + " -J")
    services.append(iperf_client)
    # client_proc = client.popen("wget -q --delete-after http://" + server.IP() + "/form_field_value.ibd")

    # client_proc.wait()
    iperf_client.wait()

    global done
    done = True

    # print('Starting server ' + datetime.datetime.now().strftime(precise_time_str))
    # server_proc = server.popen('iperf3 -s')
    # services.insert(0, server_proc)

    # print('Starting client ' + datetime.datetime.now().strftime(precise_time_str))
    # client_proc = client.popen('iperf3 -c ' + server.IP() + ' -t 120 --logfile ' + os.path.join(data_root, 'client.json') + ' -J')

    # client_proc.wait()

    print('Terminating... ' + datetime.datetime.now().strftime(precise_time_str))
    time.sleep(3)

    for s in services:
        try:
            s.terminate()
        except OSError as e:
            print(repr(e))

    print("Output saved to: " + data_root)

    net.iperf((server, client))

    net.stop()


if __name__ == '__main__':
    main()