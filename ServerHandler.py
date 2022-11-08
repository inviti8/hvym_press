
# -*- coding: UTF-8 -*-
import http.server
import socketserver
import threading
import time
import os

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )


class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SCRIPT_DIR, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        if self.path == '/kill_server/':
            print("Shutdown server")
            threading.Thread(target = self.server.shutdown, daemon=True).start()


        return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
    def do_POST(self):
        self._set_headers()
        if self.path.startswith('/shutdown'):
            print("server shutting down.")
            threading.Thread(target = self.server.shutdown, daemon=True).start()

class TCPServer(socketserver.TCPServer):
    def server_bind(self):
        import socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        
        
class Server():
    def __init__(self, server=TCPServer,  handler=ServerHandler, server_address=('', 8000)):
        self.ServerHandler = handler
        self.httpd = TCPServer(server_address, handler)
        
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        print("Server started on localhost:{server_address}\n Ctrl+C to Stop")
        
        while True:
            
            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                break
                print('interrupted!')
                