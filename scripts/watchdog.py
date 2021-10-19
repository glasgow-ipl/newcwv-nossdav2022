
import BaseHTTPServer
import SimpleHTTPServer
import SocketServer

import json
import sys

PORT = 8000

class MyHttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With") 

    def do_GET(self):
        if self.path == '/end':
            self.server.clients -= 1
            if self.server.clients == 0:
                self.server.server_close()
            else:
                print("Waiting for %s clients to finish before terminating..." % self.server.clients)


    def do_POST(self):
        cli_addr = self.client_address[0]
        cli_addr.replace('.', '_')
        if self.path == '/end':
            self.server.clients -= 1
            if self.server.clients == 0:
                print("Stopping watchdog (POST)")
                self.server.server_close()
            else:
                print("Waiting for %s clients to finish before terminating..." % self.server.clients)
            
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            with open('dashjs_metrics_client_%s.json' % cli_addr, 'w') as f:
                json.dump(data, f)

        elif self.path == '/estimates':
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            with open('dashjs_estimates_client_%s.json' % cli_addr, 'w') as f:
                json.dump(data, f)

            print("Got estimates", data)
        elif self.path == '/recordLog':
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            print("got data %s" % data)
            with open('event_log_%s.json' % cli_addr, 'w') as f:
                json.dump(data, f)



def start_server():
    clients = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    handler = MyHttpHandler
    httpd = SocketServer.TCPServer(("", PORT), handler)
    httpd.clients = clients

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
