# Simple DDoS Protection System

Contains a server that can detect DDoS attacks and deny them and a client that provides these atttacks.

There are 2 ways to limit the requests. One is through a limited time frame, while the other let's through requests based on an average req/time threshold.
You can switch between these 2 in the request_limiter.py

## Dependencies

Requests - an elegant and simple HTTP library for Python

## Installation

Start the server first with:
```sh
python server.py
```
Then run the client:
```sh
python client.py
```

Input the parameters for the client to begin the DDoS attack. To stop the attack simply use the Ctrl+C command to gracefully exit.
