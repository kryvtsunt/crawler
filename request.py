class HTTPRequest:

    # creates a HTTPRequest
    # all params are strings except for cookies
    # method is 'GET' or 'POST'
    # resource is the URI
    # version is the HTTP version
    # host is the host
    # connection specifies whether to keep the connection alive
    # cookies is a dict of any cookies to include in the request
    # body is the body message
    def __init__(self, method, resource, host='fring.ccs.neu.edu', cookies='', body='', version='1.0'):
        self.method = method.upper()
        self.resource = resource
        self.version = version
        self.host = host
        self.content_length = len(body)
        self.cookies = cookies
        self.body = body

    # this request as a String
    def __str__(self):
        request = (
            f'{self.method} {self.resource} HTTP/{self.version}\r\n'
            f'Host: {self.host}\r\n'
            f'Connection: keep-alive\r\n'
            f'Content-Length: {self.content_length}\r\n'
            f'Cookie: {self.cookies}\r\n'
            f'{self.body}\r\n\r\n'
            )
        return request


    def encode(self):
        return str(self).encode()

# class FakebookHTTPRequest(HTTPRequest):
#     def __init__(self, method, resource, cookies, body='', version='1.0'):
#         super().__init__(method, resource, 'fring.ccs.neu.edu', cookies, body, version)

# login_get = HTTPRequest('GET', '/accounts/login/?next=/fakebook', 'fring.ccs.neu.edu')
# fakebook_login = FakebookHTTPRequest('GET', '/accounts/login/?next=/fakebook')