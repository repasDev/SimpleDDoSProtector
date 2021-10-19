from datetime import datetime

class RequestLimiter():
    '''
    Creates a thread that can be used to send requests to a server

    Attributes
    ----------
        request_limit : float
            Maximum request limit in a certain time amount
        time_limit : float
            Introduces a time constraint to the amount of requests going through
        limit_reached : bool
            When true responds denies the get request with a 503
        last_timestamp : float 
            Timestamp of the last relevant request
        rate_amount : float
            Tracks the rate of request per time
        request_tracker : int
            Tracks the number of requests made in a certain time frame

    '''
    def __init__(self, request_limit: float, time_limit: float):
        self.request_limit: float = request_limit
        self.time_limit: float = time_limit
        self.limit_reached: dict[bool] = {}
        self.last_timestamp: dict[float] = {}

        # For 1st method
        self.request_tracker: dict[int] = {}
        # For 2nd method      
        self.rate_amount: dict[float] = {}

    def monitor_requests(self, id: int):
        if id not in self.limit_reached:
            self.initialize_limiter(id)
        self.check_timestamps(id)

    def initialize_limiter(self, id: int):
        self.last_timestamp[id] = datetime.now().timestamp()
        self.limit_reached[id] = False
        self.request_tracker[id] = self.request_limit
        self.rate_amount[id] = self.request_limit

    def check_timestamps(self, id:int):
        # Allows a certain number of requests in the time frame given by the first request,
        # after the time frame is up it opens up a new time frame which then allows
        # another set of requests. Uses fixed time frames.
        current_time = datetime.now().timestamp() 
        delta_time =  current_time - self.last_timestamp[id]

        if self.request_tracker[id] > 0:
            self.request_tracker[id] -= 1
            self.limit_reached[id] = False
        else:
            self.limit_reached[id] = True
        if delta_time > 5:
            self.request_tracker[id] = self.request_limit - 1 
            self.last_timestamp[id] = current_time
            self.limit_reached[id] = False

 
    def check_timestamps2(self, id:int):
        # Another implementaion. Monitors the average number of requests and only lets requests
        # through when the average threshold isn't reached
        current_timestamp = datetime.now().timestamp()
        time_delta = current_timestamp - self.last_timestamp[id]
        self.last_timestamp[id] = current_timestamp
        self.rate_amount[id] += time_delta * (self.request_limit / self.time_limit)

        if self.rate_amount[id] > self.request_limit:
            self.rate_amount[id] = self.request_limit
        if self.rate_amount[id] < 1.0:
            self.limit_reached[id] = True            
        else:
            self.rate_amount[id] -= 1.0
            self.limit_reached[id] = False
