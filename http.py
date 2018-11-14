import socket
import time


from request import *



class HTTP:
    def __init__(self, host='fring.ccs.neu.edu'):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.connect(1)


    def send(self, request: HTTPRequest):
        try:
            self.s.send(request.encode())
            response = self.s.recv(4096).decode()
            return response
        except ConnectionResetError:
            self.connect(1)
            self.send(request)


    def connect(self, counter):
        try:
            self.s.connect((self.host, 80))
        except TimeoutError:
            print(counter)
            time.sleep(counter)
            counter+=1
            self.connect(counter)

