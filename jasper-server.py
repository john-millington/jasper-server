#!/usr/local/bin/python3

from http.server import HTTPServer
import time

from server.JasperServer import JasperServer

hostName = ''
hostPort = 80

myServer = HTTPServer((hostName, hostPort), JasperServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))