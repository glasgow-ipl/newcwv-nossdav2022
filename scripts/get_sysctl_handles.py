import os
import sys

def generate_conf():
    
    with open('/proc/sys/net/ipv4/tcp_congestion_control') as f:
        alg_name = f.read().strip()

    configs = []
    base = [ '/proc/sys/net/ipv4/', '/proc/sys/net/core']
    for b in base:
        for x in os.listdir(b):
            handle_path = os.path.join(b, x)
            if not os.path.isdir(handle_path) and os.access(handle_path, os.R_OK) and (x.startswith('tcp') or 'core' in b):
                with open(handle_path) as f:
                    configs.append(f'{x}, {f.read()}')

    with open(f'{alg_name}_handles.conf', 'w') as f:
        f.write(''.join(configs))



if __name__ == '__main__':
    generate_conf()