import http.server
import socketserver
import threading
import time

# launch webserver to transfer files to router  

class Server:
    def __init__(self, path, ip, port):
        self.path = path
        self.ip = ip
        self.port = port
        self.server = self.start(path, ip, port)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def start(self, path, ip, port):
        print("path {}    ip {}    port {}".format(path, ip, port))
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=path, **kwargs)

        server = socketserver.TCPServer((ip, port), Handler)
        print("serving at: {}:{}".format(ip, port))
        return server

    def thread_start(self):
        self.thread.start() 

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()

