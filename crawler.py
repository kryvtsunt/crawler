from request import *
from http import *


class Crawler:
    def __init__(self, host='fring.ccs.neu.edu'):
        self.http = HTTP(host)

    def login(self, username, password):
        get = HTTPRequest('GET', '/accounts/login/?next=/fakebook')
        response = self.http.send(get)
        print(str(get))
        print(response)
        assert self.retrieve_cookies(response) == True
        body = "username="+username+"&password="+password+"&csrfmiddlewaretoken="+ self.csrf +"&next=%2Ffakebook%2F"
        post = HTTPRequest('POST', '/accounts/login/?next=/fakebook', cookies=self.cookies, body=body)
        response = self.http.send(post)
        print(str(post))
        print(response)

    # retrieve cookies
    def retrieve_cookies(self, response):
        num_cookies = response.count('Set-Cookie')
        if (num_cookies != 2):
            return False
        current_start = 0
        cookies = ""
        counter = 0
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
        self.csrf, self.session = cookies[:-2].split(";", 1)
        self.cookies = "csrftoken="+self.csrf+"; sessionid="+self.session
        return True

    def __del__(self):
        self.http.__del__()




crawler = Crawler()
crawler.login("001688440", "GBLTTC6G")