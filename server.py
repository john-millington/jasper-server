#!/usr/local/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs
import time
import json

from Classifier import Classifier

hostName = ""
hostPort = 80

classifier = Classifier()

class MyServer(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def classify(self, text):
        result = classifier.prop_classify(text)

        return {
            'text': text,
            'sentiment': result.max(),
            'scores': result.dict
        }

    def do_GET(self):
        query = urlparse(self.path).query
        query_dict = parse_qs(query)

        response = { 'error': 'No text specified' }
        if ('text' in query_dict):
            response = self.classify(query_dict['text'][0])

        json_dump = json.dumps(response)

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header('Content-Length', len(json_dump))
        self.send_header('Content-Type', 'application/json; charset=UTF-8')
        self.send_header('Cache-Control', 'no-store, no-cache, no-transform, must-revalidate, max-age=0')
        self.end_headers()

        self.wfile.write(bytes(json_dump, 'utf8'))
        

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        json_data = post_data.decode('utf8').replace("'", '"')
        
        post_dict = json.loads(json_data)
        response = { 'error': 'No text specified' }
        if ('texts' in post_dict):
            texts = post_dict['texts']
            
            results = []
            for text in texts:
                results.append(self.classify(text))

            response = {
                'texts': results
            }

        json_dump = json.dumps(response)

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header('Content-Length', len(json_dump))
        self.send_header('Content-Type', 'application/json; charset=UTF-8')
        self.send_header('Cache-Control', 'no-store, no-cache, no-transform, must-revalidate, max-age=0')
        self.end_headers()

        self.wfile.write(bytes(json_dump, 'utf8'))

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))