import datetime
import os
import parse_pcap


def get_cwnds(kern_log_path, unique=True, video_only=True):
    cwnds = {}
    fmt = '%Y-%m-%dT%H:%M:%S.%f'

    with open(kern_log_path) as f:
        for line in f:
            if "ACK Received" in line:
                #Get client port
                c_port = int(line.split('dstp: ')[1].split(' ')[0])
                cwnds_con = cwnds.get(c_port, [])
                #Get cwnd size
                cwnd = int(line.split('send window: ')[1].split(' ')[0])
                #Get kernel timestamp
                ts = line.split(' ')[0].split('+')[0]
                ts = datetime.datetime.strptime(ts, fmt)

                if unique and cwnds_con:
                    if cwnds_con[-1][1] != cwnd:
                        cwnds_con.append((ts, cwnd))
                else:
                    cwnds_con.append((ts, cwnd))
                
                cwnds[c_port] = cwnds_con
                
    # By now we have captured multiple connections being made to the server. The DASH connection requesting video is the one with most ACKs

    if video_only:
        # cross-check what the video cwnds were with the pcap file.
        base = os.path.dirname(kern_log_path)
        pcap_path = os.path.join(base, 'server.pcap')
        ports = parse_pcap.get_client_connection_ports(pcap_path)

        cwnds = [(k, v) for k, v in cwnds.items() if k in ports]

    return cwnds            

def get_packet_loss(kern_log_path):
    lost_packets = []
    fmt = '%Y-%m-%dT%H:%M:%S.%f'
    with open(kern_log_path) as f:
        for line in f:
            if 'Trace event:' in line and 'Loss' in line:
                #Get kernel timestamp
                time = line.split(' ')[0].split('+')[0]
                time = datetime.datetime.strptime(time, fmt)

                reason = line.split("Loss. ")[1]
                lost_packets.append((time, reason))

    return lost_packets

if __name__ == '__main__':
    # print(get_cwnds('/vagrant/logs/tmp/newcwv/newcwvtest_reno/kern.log'))
    get_cwnds('/vagrant/logs/tmp/newcwv/newcwv_newcwvh/kern.log')
