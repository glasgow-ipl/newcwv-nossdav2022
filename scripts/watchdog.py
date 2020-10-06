import socket
import struct

import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
# For monitoriong CPU usage
import psutil
import time
import os

import json

PORT = 8000

# Returns TCP_INFO encoded structure
# for exact unpack format and size, check TCP_INFO struct at /usr/include/linux/tcp.h

# 7 -> is_app_limited
# 14 -> RCV_SSTRESH
# 17 -> SND_SSTRESH
# 18 -> SND_CWND

# def getTCPInfo(s):
#     fmt_14_04 = "B"*7+"I"*21
#     fmt_18_04 = "B"*8+"I"*21

#     desired = fmt_18_04

#     struct_size = struct.calcsize(desired)

#     info = s.getsockopt(socket.IPPROTO_TCP, socket.TCP_INFO, struct_size)
#     x = struct.unpack(desired, info)
#     return "app_limited: %s, RCV_SSTRESH: %s, SND_SSTRESH: %s, SND_CWND: %s" % (x[7], x[21], x[24], x[25])

class MyHttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With") 

    def do_GET(self):
        if self.path == '/end':
            print("Stopping watchdog (GET)")
            self.server.server_close()


    def do_POST(self):
        if self.path == '/end':
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            with open('dashjs_metrics.json', 'w') as f:
                json.dump(data, f)

            print("Stopping watchdog (POST)")
            self.server.server_close()



def start_server():
    handler = MyHttpHandler
    httpd = SocketServer.TCPServer(("", PORT), handler)

    try:
        httpd.serve_forever() 
    except Exception as e:
        if e.args[0] == 9:
            return
        # Should not really ever get to this point, but if we do log will be interesting
        with open('logs/server.err', 'w') as f:
            f.write(repr(e))


if __name__ == '__main__':
    start_server()
