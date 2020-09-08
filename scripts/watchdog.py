import socket
import struct

import SimpleHTTPServer
import SocketServer
# For monitoriong CPU usage
import psutil
import time
import os

import threading

PORT = 8000

# Returns TCP_INFO encoded structure
# for exact unpack format and size, check TCP_INFO struct at /usr/include/linux/tcp.h

# 7 -> is_app_limited
# 14 -> RCV_SSTRESH
# 17 -> SND_SSTRESH
# 18 -> SND_CWND

output = []

def getTCPInfo(s):
    fmt_14_04 = "B"*7+"I"*21
    fmt_18_04 = "B"*8+"I"*21

    desired = fmt_18_04

    struct_size = struct.calcsize(desired)

    info = s.getsockopt(socket.IPPROTO_TCP, socket.TCP_INFO, struct_size)
    x = struct.unpack(desired, info)
    return "app_limited: %s, RCV_SSTRESH: %s, SND_SSTRESH: %s, SND_CWND: %s" % (x[7], x[21], x[24], x[25])


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/end':
            print ("will close server now")
            self.server.server_close()
        

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


def start_server():
    handler = MyHandler
    httpd = SocketServer.TCPServer(("", PORT), handler)

    try:
        httpd.serve_forever() 
    except Exception as e:
        if e.args[0] == 9:
            return
        # Should not really ever get to this point, but if we do log will be interesting
        with open('logs/server.err', 'w') as f:
            f.write(repr(e))
        # Write whatever output we had so far to the outfile
        output_str = ''.join(output)
        f = open('logs/cubic.out', 'w')
        f.write(output_str)
        f.close()


if __name__ == '__main__':
    t = threading.Thread(target=start_server)        
    t.start()


    t.join()
