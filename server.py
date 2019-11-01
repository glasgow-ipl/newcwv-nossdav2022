import socket
import struct
from binascii import *
 
# 7 -> is_app_limited
# 14 -> RCV_SSTRESH
# 17 -> SND_SSTRESH
# 18 -> SND_CWND


import SimpleHTTPServer
import SocketServer
# For monitoriong CPU usage
import psutil
import time

PORT = 8000

# Returns TCP_INFO encoded structure
# for exact unpack format and size, check TCP_INFO struct at /usr/include/linux/tcp.h

def getTCPInfo(s):
    fmt = "B"*7+"I"*21
    fmt2 = "B"*8+"I"*21
    info = s.getsockopt(socket.IPPROTO_TCP, socket.TCP_INFO, 92)
    #print hexlify(info)
    x = struct.unpack(fmt, info)
    #print x
    proper = struct.unpack(fmt2, info)
    #print proper
    return "app_limited: %s, RCV_SSTRESH: %s, SND_SSTRESH: %s, SND_CWND: %s" % (proper[7], proper[14 + 8], proper[17+8], proper[18+8])


def getServerInfo():
    return getTCPInfo(httpd.socket)


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print '-'*10+'custom GET'+'-'*10
 
        cpu_load = psutil.cpu_percent()
        info = getServerInfo()
        info += ", CPU_LOAD: %f" % cpu_load
        print 'PATH %s' % self.path
        if 'video' in self.path:
            t = time.time() - now
            quality_no = self.path.split('video=')[1]
            if '-' in quality_no:
                quality, no = quality_no.split('-')
                no = no[:-4]
                with open('cubic.out', 'a') as f:
                    f.write('%.5f,%s,%s\n%s\n' % (t, quality, no,info))
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
