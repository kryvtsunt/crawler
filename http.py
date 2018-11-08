#!/usr/bin/env python3
import binascii
import socket
import argparse
import sys
import ssl

from request import *



class HTTP:
    def __init__(self, host='fring.ccs.neu.edu'):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, 80))

    def send(self, request: HTTPRequest):
        self.s.send(request.encode())
        response = self.s.recv(4096).decode()
        return response


    def __del__(self):
        self.s.close()