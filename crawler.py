import time
from parser import *
from http import *
from html.parser import HTMLParser


class Crawler:
    def __init__(self, host='fring.ccs.neu.edu'):
        self.parser = Parser()
        self.host = host

    def login(self, username, password):
        self.http = HTTP(self.host)
        get = HTTPRequest('GET', '/accounts/login/?next=/fakebook')
        response = self.http.send(get)
        print(str(get))
        print('\r\n')
        print(response)
        assert self.retrieve_cookies(response) == True
        body = "username="+username+"&password="+password+"&csrfmiddlewaretoken="+ self.csrf +"&next=%2Ffakebook%2F"
        post = HTTPRequest('POST', '/accounts/login/?next=/fakebook', cookies=self.cookies, body=body)
        response = self.http.send(post)
        print(str(post))
        print('\r\n')
        print(response)

        href = self.retrieve_location(response)
        self.retrieve_cookies(response)
        get = HTTPRequest('GET', href, cookies=self.cookies)
        response = self.http.send(get)
        print(str(get))
        print('\r\n')
        print(response)
        return response


    def send(self, href):
        get = HTTPRequest('GET', href, cookies=self.cookies)
        response = self.http.send(get)
        print(str(get))
        print('\r\n')
        print(response)
        return response


    # retrieve cookies
    def retrieve_cookies(self, response):
        num_cookies = response.count('Set-Cookie')
        if (num_cookies == 0):
            return False
        current_start = 0
        cookies = ""
        counter = 0
        while counter < num_cookies:
            set_start_index = response.find('Set-Cookie', current_start)
            set_end_index = response.find('\r\n', set_start_index)
            set_cookie = response[set_start_index : set_end_index]
            cookie_start_index = 22
            cookie_end_index = set_cookie.find(';')
            cookie = set_cookie[cookie_start_index : cookie_end_index]
            cookies += cookie + ";"
            current_start = set_end_index
            counter+=1
        if (num_cookies == 1):
            self.session = cookies
            self.cookies = "csrftoken="+self.csrf+"; sessionid="+self.session
        elif (num_cookies == 2):
            self.csrf, self.session = cookies[:-2].split(";", 1)
            self.cookies = "csrftoken="+self.csrf+"; sessionid="+self.session
        return True

    def retrieve_location(self, response):
        set_start_index = response.find('Location', 0) + 10
        set_end_index = response.find('\r\n', set_start_index)
        location = response[set_start_index: set_end_index]
        return location

    def retrieve_connection(self, response):
        set_start_index = response.find('Connection', 0) + 12
        set_end_index = response.find('\r\n', set_start_index)
        connection = response[set_start_index: set_end_index]
        return connection

    def crawl(self):
        response = self.login("001688440", "GBLTTC6G")
        self.parser.feed(response)
        while (len(self.parser.links) > 0):
            print(self.parser.links)
            print(self.parser.keys)
            link = self.parser.links.pop()
            while True:
                resp = self.send(link)
                status = resp[9:12]
                print(status)
                connection = self.retrieve_connection(resp)
                print(connection)
                if connection == "close":
                    self.login("001688440", "GBLTTC6G")
                    time.sleep(1)
                elif status == "200":
                    self.parser.feed(resp)
                    break
                elif status == "400" or status == "403" or status == "404":
                    break
                elif status == "500":
                    self.login("001688440", "GBLTTC6G")
                    time.sleep(1)

    def crawl_page(self, href):
        response = self.send(href)
        self.parser.feed(response)
        self.links += self.parser.links
        print("page")
        print(self.links)






    def __del__(self):
        self.http.__del__()


# example from the python documentation. needs refactoring
class Parser(HTMLParser):
    def __init__(self):
        self.links = []
        self.visited = []
        self.flags = []
        super().__init__()


    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if str(attr[0]) == 'href' and has_numbers(str(attr[1])) and attr[1] not in self.visited:
                self.links.append(attr[1])
                self.visited.append(attr[1])
            elif str(attr[0]) == 'h2':
                self.flags.append(attr[1])





def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


crawler = Crawler()
crawler.crawl()



