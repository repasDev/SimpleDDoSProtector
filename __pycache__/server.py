from datetime import datetime
import threading

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle get request
        id: int = self.extract_id_from_query()
        limit_reached: bool = limiter.monitor_requests(id)
        # self.print_thread_info()

        if id != None:
            if not limit_reached:
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


class RequestLimiter():
    def __init__(self, request_limit: float, time_limit: float):
        self.clientIds = {}
        self.request_limit: float = request_limit
        self.time_limit: float = time_limit
        self.limited_reached: dict = {}
        self.last_timestamp: dict = {}
        self.rate_amount: dict = {}

    def monitor_requests(self, id: int):
        # Keeps log of requests and their timestamps
        if id not in self.clientIds:
            self.initialize_limiter(id)
            return False
        if self.limited_reached[id]:
            return True
        else:
            return self.check_timestamps(id)

    def initialize_limiter(self, id):
        self.clientIds[id] = [datetime.now().timestamp()]   # TO NE RABI BIT LIST NOT LOL, FIX THIS SHIT
        self.last_timestamp[id] = [datetime.now().timestamp()] 
        self.rate_amount[id] = self.request_limit
        self.limited_reached[id] = False

    def check_timestamps(self, id: int):
        # Checks if 5 requests were made in the time specified by the request_limit
        # If the threshold is reached it returns True to refuse further get requests
        # If the threshold is not reached during a specified time the timestamp list is cleared
        timestamps = self.clientIds[id]   # Fix endless stacking
        timestamps.append(datetime.now().timestamp())
        print(timestamps)
        if len(timestamps) >= self.request_limit:
            self.limited_reached[id] = True
            return True 
        time = (timestamps[-1] - timestamps[0])
        seconds = time
        if seconds > self.time_limit:
            timestamps.clear()
        return False
    
    def check_timestamps2(self, id:int):
        #
        timestamps = self.clientIds[id]
        timestamps.append(datetime.now().timestamp())
        current_timestamp = datetime.now().timestamp()
        for i in range(0, len(timestamps)):
            if current_timestamp - timestamps[i] > 5:
                timestamps.pop(i)
        print(timestamps)
    
    def check_timestamps3(self, id:int):
        #
        current_timestamp = datetime.now().timestamp()
        time_delta = current_timestamp - self.last_timestamp[id]
        self.last_timestamp = current_timestamp
        self.rate_amount[id] += time_delta * (self.request_limit / self.time_limit)
        if self.rate_amount[id] > self.request_limit:
            self.rate_amount = self.request_limit
        if self.rate_amount[id] < 1.0:
            return True
        else:
            self.rate_amount[id] -= 1.0
            return False



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    # daemon_threads = True 


if __name__ == '__main__':
    limiter = RequestLimiter(request_limit=5.0, time_limit=5.0)
    server = ThreadedHTTPServer(('localhost', 8000), ServerHandler)
    server.serve_forever()
