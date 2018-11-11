from request import *
from http import *
from html.parser import HTMLParser


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

class Crawler:
    def __init__(self, host='fring.ccs.neu.edu'):
        self.http = HTTP(host)
        self.links = []

    def login(self, username, password):
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


    def __del__(self):
        self.http.__del__()

# example from the python focumentation. needs refactoring
class MyHTMLParser(HTMLParser):

    def __init__(self):
        self.links = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            if hasNumbers(str(attr)):
                #set_start_index = attr.find('/fakebook/', 0)
                #print(set_start_index)
                #set_end_index = attr.find(")", set_start_index)
                #href = attr[set_start_index: set_end_index]
                self.links.append(attr[1])
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)



crawler = Crawler()
response = crawler.login("001688440", "GBLTTC6G")
parser = MyHTMLParser()
parser.feed(response)
crawler.links += parser.links
print(crawler.links)
crawler.send(crawler.links[0])



