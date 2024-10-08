import socket
"""import requests
from http.client import HTTPConnection
from urllib3.contrib.emscripten.fetch import is_cross_origin_isolated
HTTPConnection._http_vsn_str = 'HTTP/1.0'"""


class URL:
    def __init__(self, url): #costruttore della classe URL, deve sempre avere self, in aggiunta a qualsiasi parametro richiesto
        self.schema, url = url.split("://", 1) #self.variabile = dichiara variabile nel costruttore a partire da un valore
        assert self.schema == "http" #returns true if schema == http
        if "/" not in url:
            url = url + "/"
        self.host = url.split("/", 1)
        self.path = url + "/"

    def request(self):
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as sock:
        sock = socket.socket(
               family=socket.AF_INET,
               type=socket.SOCK_STREAM,
               proto=socket.IPPROTO_TCP,
               )
        conhost = str(self.host)+"80"
        sock.connect((conhost)) #two parentheses in the connect call: connect takes a single argument, and that argument is a pair of a host and a port. This is because different address families have different numbers of arguments.

        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n" #newline. Has to be double to specify end of message
        sock.send(request.encode("utf8")) #converts str into bytes


        response = sock.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        response_headers = {}
        while True:
            line = response.readline()
            if line =="\r\n" : break
            header, value = line.split(":", 1) #split line at : to get headers - names and values
            response_headers[header.casefold()] = value.strip() #normalization into lowercase because headers are not case-sensitive

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers #both lines warn us of weird data (??? look it up)
        content = response.read()
        sock.close()

        return content

def show(body):
    in_tag = False  # defines if body is within <> or not through bool
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    body = url.request().decode("utf8")
    show(body)  # both lines show complete page by chaining request and body


"""In HTML, there are tags and text. Each tag starts with a < and ends with a >; generally speaking, tags tell you what kind of thing some content is, 
while text is the actual content.That said, some tags, like img, are content, not information about it. 
Most tags come in pairs of a start and an end tag; for example, the title of the page is enclosed in a pair of tags: <title> and </title>. 
Each tag, inside the angle brackets, has a tag name (like title here), and then optionally a space followed by attributes, 
and its pair has a / followed by the tag name (and no attributes)."""
