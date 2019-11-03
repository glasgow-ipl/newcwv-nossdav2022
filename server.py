import socket
import struct
from binascii import * 

import SimpleHTTPServer
import SocketServer
# For monitoriong CPU usage
import psutil
import time

PORT = 8000

# Returns TCP_INFO encoded structure
# for exact unpack format and size, check TCP_INFO struct at /usr/include/linux/tcp.h

# 7 -> is_app_limited
# 14 -> RCV_SSTRESH
# 17 -> SND_SSTRESH
# 18 -> SND_CWND

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
        print '-'*10+'custom GET'+'-'*10
 
        print 'PATH %s' % self.path
        if 'video' in self.path:
            cpu_load = psutil.cpu_percent()
            info = getTCPInfo(self.wfile._sock)
            info += ", CPU_LOAD: %f" % cpu_load

            t = time.time() - now
            quality_no = self.path.split('video=')[1]
            if '-' in quality_no:
                quality, no = quality_no.split('-')
                no = no[:-4]
                with open('cubic.out', 'a') as f:
                    f.write('%.5f,%s,%s\n%s %s\n' % (t, quality, no,info, self.request.fileno()))
                #print 'written to FILE %s' % str(f)
                if int(no) == 100:
                    print 'EXITING now'
                    sys.exit(1)

        print '-'*10+'END custom GET'+'-'*10
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

handler = MyHandler

httpd = SocketServer.TCPServer(("", PORT), handler)
now = time.time()

#print psutil.cpu_percent()
print getServerInfo()

#f = open('cubic.out', 'w')

print "serving at port", PORT
httpd.serve_forever() 
