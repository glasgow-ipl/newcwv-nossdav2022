import socket
import struct
from binascii import * 

import SimpleHTTPServer
import SocketServer
# For monitoriong CPU usage
import psutil
import time
import os

PORT = 8000

MAX_SEGMENTS = 30 # Assuming bbb_sunflower and 1 second segments TODO: Get value from MPD or data directory

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


def getServerInfo():
    return getTCPInfo(httpd.socket)


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print ('-'*10+'custom GET'+'-'*10)
 
        print ('PATH %s' % self.path)
        if 'm4s' in self.path: # this is a segment
            cpu_load = psutil.cpu_percent()
            if self.request != self.wfile._sock:
                print ('%s %d %d' % ('>'*15, self.request.fileno(), self.wfile._sock.fileno()))
            info = getTCPInfo(self.wfile._sock)
            info += ", CPU_LOAD: %f" % cpu_load

            t = time.time() - now
            root_stripped = self.path.split('/data/')[1].split('/') 
            quality = root_stripped[0]
            no = root_stripped[-1][2:-4] # TODO: remove magic numbers
            if no == 'init':
                no = '0'

            output.append('%.5f,%s,%s\n%s %s\n' % (t, quality, no,info, self.request.fileno()))

            if int(no) == MAX_SEGMENTS:
                print("sending shutdown signal")
                self.server._BaseServer__shutdown_request = True
                output_str = ''.join(output)
                f = open('logs/cubic.out', 'w')
                f.write(output_str)
                f.close()
                
        print ('-'*10+'END custom GET'+'-'*10)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

# Change directory to project root and serve that
os.chdir('..')
print("CWD: %s" % os.getcwd())

handler = MyHandler
httpd = SocketServer.TCPServer(("", PORT), handler)

now = time.time()

#print psutil.cpu_percent()
print(getServerInfo())

#f = open('logs/cubic.out', 'w')

print("serving at port", PORT)
try:
    httpd.serve_forever() 
except Exception as e:
    # Should not really ever get to this point, but if we do log will be interesting
    with open('logs/server.err', 'w') as f:
        f.write(repr(e))
    # Write whatever output we had so far to the outfile
    output_str = ''.join(output)
    f = open('logs/cubic.out', 'w')
    f.write(output_str)
    f.close()
    
