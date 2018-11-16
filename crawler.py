from parser import *
from http import *
from html.parser import HTMLParser


class Crawler:
    def __init__(self, host='fring.ccs.neu.edu'):
        self.parser = Parser()
        self.host = host
        self.cookies = ""
        self.http = HTTP(self.host)

    def login(self, username, password):
        self.send('/accounts/login/?next=/fakebook')
        body = "username=" + username + "&password=" + password + "&csrfmiddlewaretoken=" + self.csrf + "&next=%2Ffakebook%2F"
        self.send('/accounts/login/?next=/fakebook', type='POST', body=body)

    def send(self, href, type='GET', body=''):
        get = HTTPRequest(type, href, cookies=self.cookies, body=body)
        while True:
            # open new socket for every request
            if get.version == '1.1':
                self.http.s.close()
                self.http = HTTP(self.host)
            resp = self.http.send(get)
            status = resp[9:12]
            connection = self.retrieve_connection(resp)
            print(str(get))
            print('\r\n')
            print(resp)
            print('\r\n')
            print("STATUS")
            print(status)
            print(connection)
            print('\r\n')
            print('\r\n')
            # open new socket only when server tells to do so
            if (get.version == '1.0') and (connection == "close" or connection == None):
                self.http.s.close()
                self.http = HTTP(self.host)
            if status == "200":
                self.retrieve_cookies(resp)
                self.parser.feed(resp)
                break
            elif status == "302" or status == "301" or status == "300":
                href = self.retrieve_location(resp)
                self.retrieve_cookies(resp)
                return self.send(href)
            elif status == "500":
                continue
            else:
                break

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
            set_cookie = response[set_start_index: set_end_index]
            cookie_start_index = 22
            cookie_end_index = set_cookie.find(';')
            cookie = set_cookie[cookie_start_index: cookie_end_index]
            cookies += cookie + ";"
            current_start = set_end_index
            counter += 1
        if (num_cookies == 1):
            self.session = cookies
        elif (num_cookies == 2):
            self.csrf, self.session = cookies[:-2].split(";", 1)
        self.cookies = "csrftoken=" + self.csrf + "; sessionid=" + self.session
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

    def crawl(self, username, password):
        while len(self.parser.links) > 0:
            if (len(self.parser.flags) == 5):
                break
            print(self.parser.links)
            print(self.parser.flags)
            print(len(self.parser.links))
            print('\r\n')
            print('\r\n')
            link = self.parser.links.pop()
            self.send(link)
        if (len(self.parser.flags) != 5):
            self.parser.visited = []
            self.crawl(username,password)

    def run(self, username, password):
        crawler.login(username, password)
        crawler.crawl(username, password)
        for flag in crawler.parser.flags:
            print(flag)



class Parser(HTMLParser):
    def __init__(self):
        self.links = []
        self.visited = []
        self.flags = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if str(attr[0]) == 'href' and has_numbers(str(attr[1])) and str(attr[1]) not in self.visited:
                self.links.append(str(attr[1]))
                self.visited.append(str(attr[1]))

    def handle_data(self, data):
        if 'FLAG: ' == data[: 6]:
            self.flags.append(data[6:])


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


crawler = Crawler()
crawler.run('001688440', 'GBLTTC6G')

