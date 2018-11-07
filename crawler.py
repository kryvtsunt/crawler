#!/usr/bin/env python3
import binascii
import socket
import argparse
import sys
import ssl

MESSAGE = b"""GET /accounts/login/ HTTP/1.0
Connection: Keep-Alive

"""


class Crawler:
    def __init__(self):
        host = "fring.ccs.neu.edu"
        port = 80
        self.cookies = ""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    # retrieve cookies
    def retrieve_cookies(self, response):
        cookies = ""
        counter = 0
        num_cookies = response.count('Set-Cookie')
        current_start = 0
        while counter != num_cookies:
            set_start_index = response.find('Set-Cookie', current_start)
            set_end_index = response.find('\r\n', set_start_index)
            set_cookie = response[set_start_index : set_end_index]

            cookie_start_index = 12
            cookie_end_index = set_cookie.find(';')
            cookie = set_cookie[cookie_start_index : cookie_end_index]
            cookies += cookie + "; "
            current_start = set_end_index
            counter+=1

        return cookies[:-2]

    def GET(self):
        self.s.send(MESSAGE)
        resp = self.s.recv(4096).decode()
        self.cookies = self.retrieve_cookies(resp)
        print(resp)
        print(self.cookies)

    def POST(self):
        headers = """POST /accounts/login/ HTTP/1.0
        Content-Type: application/x-www-form-urlencoded
        Content-Length: 109
        Cookie: {cook}
        Host: fring.ccs.neu.edu
        Connection: keep-alive
        Pragma: no-cache
        Cache-Control: no-cache
        Origin: http://fring.ccs.neu.edu
        Upgrade-Insecure-Requests: 1
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
        Referer: http://fring.ccs.neu.edu/accounts/login/?next=/fakebook/
        Accept-Encoding: gzip, deflate
        Accept-Language: en-US,en;q=0.9
        """

        body = "username=001688440&password=GBLTTC6G&csrfmiddlewaretoken=95164a057814b203c3c8160bccd00122&next=%2Ffakebook%2F\r\n\r\n"
        headers = headers.format(
            cook= self.cookies,
        )
        request = headers + body
        self.s.sendall(request.encode('ascii'))
        print(self.s.recv(4096).decode())

    def __del__(self):
        self.s.close()


crawler = Crawler()
print("start")
crawler.GET()
crawler.POST()
print("end")
