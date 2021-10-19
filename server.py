import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import Counter
from urllib.parse import urlparse, parse_qs
from request_limiter import RequestLimiter


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        id: int = self.extract_id_from_query()
        limiter.monitor_requests(id)

        if id != None:
            if not limiter.limit_reached[id]:
                self.simple_response(code=200, message='Hello')
            else:
                self.simple_response(code=503, message='503 Service Unavailable')

    def extract_id_from_query(self):
        parsed_url = urlparse(self.path)
        query = parse_qs(parsed_url.query)

        if 'clientId' not in query.keys():
            self.simple_response(code=400, message='400 Bad Request')
            return None
            
        id = int(query['clientId'][0])
        return id

    def simple_response(self, code: int, message: str):
        self.send_response(code)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f'{message}'.encode())

    def print_thread_info(self):
        # For informational use
        message = threading.currentThread().getName()
        print('')
        print(message)
        print(threading.active_count())


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    # daemon_threads = True 


if __name__ == '__main__':
    limiter = RequestLimiter(request_limit=5.0, time_limit=5.0)
    server = ThreadedHTTPServer(('localhost', 8000), ServerHandler)
    server.serve_forever()
