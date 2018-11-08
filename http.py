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

    # retrieve cookies
    def retrieve_cookies(self, response):
        cookies = ""
        counter = 0
        num_cookies = response.count('Set-Cookie')
        if (num_cookies != 2):
            return None
        current_start = 0
        while counter != 2:
            set_start_index = response.find('Set-Cookie', current_start)
            set_end_index = response.find('\r\n', set_start_index)
            set_cookie = response[set_start_index : set_end_index]
            cookie_start_index = 22
            cookie_end_index = set_cookie.find(';')
            cookie = set_cookie[cookie_start_index : cookie_end_index]
            cookies += cookie + ";"
            current_start = set_end_index
            counter+=1
        return cookies[:-2]

    def send(self, request: HTTPRequest):
        self.s.send(request.encode())
        response = self.s.recv(4096).decode()
        return response


    def __del__(self):
        self.s.close()