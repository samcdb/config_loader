'''
import http.server
import socketserver
import socket

PORT = 8000

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("192.168.88.254", PORT), handler) as httpd:
    print("Server started at: 192.168.88.254:" + str(PORT))
    httpd.serve_forever()



import http.server
import socketserver

PORT = 8000
DIRECTORY = 'D:/OneSpace/config_loader/server'


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


with socketserver.TCPServer(("192.168.88.254", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
    '''
import http.server
import socketserver

# launch webserver to transfer files to router
def createServer(path, ip, port):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=path, **kwargs)

    with socketserver.TCPServer((ip, port), Handler) as httpd:
        print("serving at: {}:{}".format(ip, port))
        httpd.serve_forever()

if __name__ == '__main__':
    createServer()


