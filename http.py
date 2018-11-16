import socket

from request import *


# HHTP request implementation that uses socket
class HTTP:
    def __init__(self, host='fring.ccs.neu.edu'):
        self.connect(host)

    # send a request and return a respond
    def send(self, request: HTTPRequest):
        self.s.send(request.encode())
        response = self.s.recv(4096).decode()
        return response

    # connect until connection is not established
    def connect(self, host, counter = 1):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, 80))
        except TimeoutError:
            # print("Server does not respond. Reconnection attempt " + str(counter))
            counter+=1
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect(host, counter)



