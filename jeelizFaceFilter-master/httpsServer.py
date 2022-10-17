#!/usr/bin/python2

import http.server
import ssl

print('Basic HTTPS server. It should be run with Python2 (not 3)')

httpd = http.server.HTTPServer(('localhost', 4443), http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)

print('OK buddy now open https://127.0.0.1:4443 in your web browser, and accept the camera (icon at the right of the URL bar)')
httpd.serve_forever()