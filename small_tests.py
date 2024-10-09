import socket
import ssl

"""class URL:
    def __init__(self, schema, host, path, port):
        self.schema = schema
        self.host = host
        self.path = path
        self.port = port

    def file_request(self):

        f = open(self.path, "r")
        print(f.read())

    def request(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as sock:
            sock.connect((self.host, self.port))
            if self.schema == "https":
                ctx = ssl.create_default_context()  # create "context" for encryption
                sock = ctx.wrap_socket(sock, server_hostname=self.host)  # wrap the socket with the context

            request = "GET {} HTTP/1.1\r\nConnection: close\r\n".format(self.path)  # format replaces {} with its argument
            request += "Host: {}\r\n".format(self.host)
            request += "User-Agent: NBE/WIP 0.0 - Custom browser engine.\r\n"
            request += "\r\n"  # newline. Has to be double to specify end of message
            sock.send(request.encode("utf8"))  # converts str into bytes

            response = sock.makefile("r", encoding="utf8", newline="\r\n")
            statusline = response.readline()
            version, status, explanation = statusline.split(" ", 2)
            response_headers = {}  # For the headers, I split each line at the first colon and fill in a map of header names to header values.
            while True:
                line = response.readline()
                if line == "\r\n": break
                header, value = line.split(":", 1)  # split line at : to get headers - names and values
                response_headers[
                    header.casefold()] = value.strip()  # normalization into lowercase because headers are not case-sensitive

            assert "transfer-encoding" not in response_headers
            assert "content-encoding" not in response_headers  # both lines warn us of weird data (??? look it up)
            content = response.read()  # everything after the headers
            sock.close()

            print("request: " + str(request))

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
    show(body)  # both lines show complete page by chaining request and body"""


"""
link = "data:text/html,Hello_world!"
domains = (".com", ".org", ".it")
webp = ("http://", "https://", "www.", ".com", ".org", ".it")
host=""
schema=""
path=""
port=0


if "data:" in link:
    print("data")
elif "file://" in link:
    print("file")
else:
    for x in webp:
        print("tuple: " + x)
        if x in link:
            if "://" in link:
                schema, host = link.split("://", 1)
                if "https" in schema:
                    port = 443
                else:
                    port = 80
            elif "www." in link and "://" not in link:
                schema, host = link.split(".", 1)
            else:
                schema = "https://"
                host = "www." + link
                port = 443
                link = schema + host + ":" + str(port) + path
            if "/" not in host:  # adds the path forward slash
                path = "/"
            else:  # separates path from host
                host, path = host.split("/", 1)
                path = "/" + path
            break


print("link: " + link)
print("schema: " + schema)
print("host: " + host)
print("path: " + path)
print("port: " + str(port))
print("complete: " + schema + host + ":" + str(port) + path)
"""