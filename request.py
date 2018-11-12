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
    def __init__(self, method, resource, host='fring.ccs.neu.edu', cookies='', body='', version='1.1'):
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
            self.method+' '+ self.resource+' HTTP/' + self.version +'\r\n'
            'Host: ' + self.host + '\r\n'
            'Connection: keep-alive\r\n'
            'Content-Type: application/x-www-form-urlencoded\r\n'
            'Content-Length: '+ str(self.content_length) +'\r\n'
            'Cookie: '+self.cookies+'\r\n\r\n' + self.body
            )
        return request


    def encode(self):
        return str(self).encode()
