import json

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs

from server.services.ClassifyService import ClassifyService
from server.services.SearchService import SearchService
from server.services.AnalysisService import AnalysisService

class JasperServer(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    SERVICES = {
        '/api/analyse': AnalysisService(),
        '/api/classify': ClassifyService(),
        '/api/search': SearchService()
    }

    def do_GET(self):
        parsed_params = urlparse(self.path)
        request_body = parse_qs(parsed_params.query)

        self.handle_service_request(request_body)

    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        json_data = post_data.decode('utf8').replace("'", '"')
        post_dict = json.loads(json_data)

        self.handle_service_request(post_dict)


    def handle_service_request(self, request_body):
        parsed_params = urlparse(self.path)
        
        service = parsed_params.path
        if (service in JasperServer.SERVICES):
            response = JasperServer.SERVICES[service].handle(request_body)
        else:
            response = {
                'error': {
                    'message': 'unknown service',
                    'code': 'JS_ERR_4000'
                }
            }

        self.send(response)


    def send(self, response):
        dump = json.dumps(response)

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header('Content-Length', len(dump))
        self.send_header('Content-Type', 'application/json; charset=UTF-8')
        self.send_header('Cache-Control', 'no-store, no-cache, no-transform, must-revalidate, max-age=0')
        self.end_headers()

        self.wfile.write(bytes(dump, 'utf8'))
