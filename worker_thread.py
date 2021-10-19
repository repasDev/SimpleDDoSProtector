import time
import threading
import random
import requests

class WorkerThread(threading.Thread):
    '''
    Creates a thread that can be used to send requests to a server

    Attributes
    ----------
        shutdown : bool
            Stops the thread if true
        url : str
            Server location
        query : str
            Client id parameter sent to the server as query
        client : object 
            Client object associated with the thread
        flood_speed : int
            Speed at which the requests are being sent
        worker : int
            Id of the worker (thread) of the associated client 


    Methods
    -------
    run()
        On thread.start() begins to send requests to server at random intervals
    '''
    
    def __init__(self, url: str, query: str, client: object, flood_speed: int, worker: int):
        threading.Thread.__init__(self)
        self.shutdown = False
        self.url = url
        self.query = query
        self.client = client
        self.flood_speed = flood_speed
        self.worker = worker

    def run(self):
        while not self.shutdown:
            time.sleep(random.random() * self.flood_speed)
            request = requests.get(self.url, params=self.query)
            print(f'Client {self.client} worker {self.worker + 1} got response: {request.status_code}')
