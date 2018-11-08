from request import *
from http import *


class Crawler:
    def __init__(self, host='fring.ccs.neu.edu'):
        self.http = HTTP()

    def login(self):
        get = HTTPRequest('GET', '/accounts/login/?next=/fakebook')
        response = self.http.send(get)
        print(str(get))
        print(response)
        cookies = self.http.retrieve_cookies(response)
        assert cookies is not None
        self.csrf, self.session = cookies.split(";", 1)

        print(self.csrf, self.session)
        cookies= self.csrf +"; " + self.session
        body = "username=001688440&password=GBLTTC6G&csrfmiddlewaretoken="+ self.csrf +"&next=%2Ffakebook%2F"

        post = HTTPRequest('POST', '/accounts/login/?next=/fakebook', cookies=cookies, body=body)
        response = self.http.send(post)
        print(str(post))
        print(response)




crawler = Crawler()
crawler.login()