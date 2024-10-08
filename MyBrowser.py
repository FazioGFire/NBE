import socket
import ssl

class URL:

    def __init__(self, link):
        link.strip()
        if "://" in link:
            self.schema, self.host = link.split("://", 1)  # https://en.wikipedia.org/wiki/List_of_URI_schemes - all of them are ://
            if "http" in self.schema: #need to define different scenarios
                print("http")
                self.port = 80
            elif "https" in self.schema:
                print("https")
                self.port = 443
            elif "file" in self.schema:
                print("file")
            elif "ftp" in self.schema:
                print("ftp")
            elif "admin" in self.schema:
                print("admin")
            else:
                print("unrecognized")
        elif "www" in link and "://" not in link: #if link doesn't include protocol but only subdomain - www.example.org
            print("www and not ://")
            self.host = link
            self.schema = "http"
            link = self.schema + "://" + self.host
        elif "www" not in link and "://" not in link: #if link doesn't include protocol and subdomain - example.org
            print("not www and not ://")
            self.schema = "http"
            self.host = link
            link = self.schema + "://" + self.host

        if "/" not in self.host: #adds the path forward slash
            path = self.host + "/"
        else: #separates path from host
            self.host, self.path = self.host.split("/", 1)
            self.path = "/" + self.path


        print("link after checks: " + link)
        print("host: " + str(self.host))
        print("path: " + str(self.path))
        print("host + path: " + self.host + self.path)


    def request(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as sock:
            sock.connect((self.host, self.port))
            ctx = ssl.create_default_context() # create "context" for encryption
            sock = ctx.wrap_socket(sock, server_hostname=self.host) #wrap the socket with the context

            request = "GET {} HTTP/1.0\r\n".format(self.path)
            request += "Host: {}\r\n".format(self.host)
            request += "\r\n"  # newline. Has to be double to specify end of message
            sock.send(request.encode("utf8"))  # converts str into bytes

            response = sock.makefile("r", encoding="utf8", newline="\r\n")
            statusline = response.readline()
            version, status, explanation = statusline.split(" ", 2)
            response_headers = {}
            while True:
                line = response.readline()
                if line == "\r\n": break
                header, value = line.split(":", 1)  # split line at : to get headers - names and values
                response_headers[
                    header.casefold()] = value.strip()  # normalization into lowercase because headers are not case-sensitive

            assert "transfer-encoding" not in response_headers
            assert "content-encoding" not in response_headers  # both lines warn us of weird data (??? look it up)
            content = response.read() #everything after the headers
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

def load(link):
    body = link.request()
    show(body)  # both lines show complete page by chaining request and body
