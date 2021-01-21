import threading
import time
import json
import math
import datetime

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


def changeLinkBw(ep1, ep2, in_bw, RTT, logger, out_bw=-1,):
    msg = 'changing BW %s %s ' % (in_bw, datetime.datetime.now().strftime(precise_time_str))
    print(msg)
    logger.append(msg)
    link = ep1.connectionsTo(ep2)
    bdp = _calculate_bdp(in_bw, RTT)
    link[0][0].config(**{'bw': in_bw, 'max_queue_size': bdp})
    link[0][1].config(**{'bw': out_bw if out_bw != -1 else in_bw, 'max_queue_size': bdp if out_bw == -1 else _calculate_bdp(out_bw, RTT)})


def config_bw(conf_file, ep1, ep2, logger):
    delta_time = 0
    current_time = 0
    with open(conf_file) as f:
        conf = json.load(f)
    print(conf)

    if conf.get('repeat'):
        cycles = 1
        while(current_time < conf['duration']):
            for entry in conf['changes']:
                wait_for = entry['time'] - delta_time
                time.sleep(wait_for)
                # Change BW
                changeLinkBw(ep1, ep2, entry['bw'], entry['rtt'], logger)
                delta_time = entry['time']
            
            print(current_time)
            current_time = (entry['time'] + conf['repeat']) * cycles
            cycles += 1
            delta_time = 0
            
    else:
        for entry in conf['changes']:
            wait_for = entry['time'] - delta_time
            time.sleep(wait_for)
            # Change BW
            changeLinkBw(ep1, ep2, entry['bw'], entry['rtt'], logger)
            delta_time = entry['time']
    

def test():
    t = threading.Thread(target=config_bw, args=('/vagrant/scripts/scratch/network_config.json'))
    t.start()

    t.join()


if __name__ == '__main__':
    test()