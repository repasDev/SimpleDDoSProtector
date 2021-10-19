from worker_thread import WorkerThread


class Client():
    def __init__(self):
        self._number_of_clients: int = None
        self._number_of_concurrent_workers: int = None
        self.clients: list = []
        self.threads: list = []

    def set_number_of_concurrent_workers(self, number_of_concurrent_workers: int):
        self._number_of_concurrent_workers = number_of_concurrent_workers

    def set_number_of_clients(self, number_of_clients: int):
        self._number_of_clients = number_of_clients

    def create_clients(self):
        for clientId in range(1, (self._number_of_clients + 1)):
            self.clients.append(clientId)

    def flood_server(self, url: str, client: object, flood_speed: int):
        # For each client create multiple workers (threads) that continiously
        # send requests to the server
        for clientId in self.clients:
            query = f'clientId={clientId}'
            for worker in range(self._number_of_concurrent_workers):
                thread = WorkerThread(url, query, clientId, flood_speed, worker)
                self.threads.append(thread)
                thread.start()

        while client.check_if_threads_alive(self.threads):
            self.monitor_threads()

        print("Program shutdown")

    def monitor_threads(self):
        try:
            # Synchronization timeout of threads stop
            [thread.join(1) for thread in self.threads
                if thread is not None and thread.is_alive()]
        except KeyboardInterrupt:
            # Ctrl-C handling and send stop signal to threads
            self.stop_threads()

    def stop_threads(self):
        print(""" \nStop signal sent to working threads \nWaiting for rest of requests to finish... \n """)

        for thread in self.threads:
            thread.shutdown = True

    def check_if_threads_alive(self, threads):
        return True in [thread.is_alive() for thread in threads]



if __name__ == '__main__':

    url = 'http://127.0.0.1:8000/'
    client = Client()
    flood_speed = 5

    print('Simple DDoS Protection Program \n')

    # Limit input values?
    client.set_number_of_clients(
        int(input('Please input number of clients: ')))
    client.set_number_of_concurrent_workers(int(input(
        'Please input number of concurrent workers per client: ')))
    
    client.create_clients()
    client.flood_server(url, client, flood_speed)
