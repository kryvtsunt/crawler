from html.parser import HTMLParser

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
            elif str(attr[0]) == 'h2':
                self.flags.append(attr[1])

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
