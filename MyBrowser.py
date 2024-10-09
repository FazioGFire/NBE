import socket
import ssl
import tkinter

flag_file=0
flag_web=0
flag_data=0
class URL:

    def __init__(self, link):
        link.strip()
        if "://" in link:
            self.schema, self.host = link.split("://", 1)  # https://en.wikipedia.org/wiki/List_of_URI_schemes - all of them are ://
            #BIG TODO: implement files, separate them from web category and run different functions based on user input
            if "file:" in link:
                flag_file = 1
                self.path = self.host
                self.path.replace("/", "", 1)
            elif self.schema == "http": #need to define different scenarios
                self.port = 80
                flag_web=1
            elif self.schema == "https":
                self.port = 443
                flag_web=1
            else:
                print("unrecognized")
        elif "www" in link and "://" not in link and "data:" not in link: #if link doesn't include protocol but only subdomain - www.example.org
            print("www and not ://")
            self.host = link
            self.schema = "http"
            link = self.schema + "://" + self.host
        elif "www" not in link and "://" not in link and "data:" not in link: #if link doesn't include protocol and subdomain - example.org
            print("not www and not ://")
            self.schema = "http"
            self.host = link
            link = self.schema + "://" + self.host
        elif "data:" in link:
            print("data") #data:text/html,Hello world!

        if "/" not in self.host: #adds the path forward slash
            self.path = "/"
        else: #separates path from host
            self.host, self.path = self.host.split("/", 1)
            self.path = "/" + self.path
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)


        print("link after checks: " + link)
        print("protocol: " + str(self.schema))
        print("host: " + str(self.host))
        print("path: " + str(self.path))
        print("port: " + str(self.port))
        print("complete: " + self.schema + "://" + self.host + self.path)


    def request(self):

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as sock:
                sock.connect((self.host, self.port))
                if self.schema == "https":
                    ctx = ssl.create_default_context() # create "context" for encryption
                    sock = ctx.wrap_socket(sock, server_hostname=self.host) #wrap the socket with the context

                request = "GET {} HTTP/1.1\r\nConnection: close\r\n".format(self.path) #format replaces {} with its argument
                request += "Host: {}\r\n".format(self.host)
                request += "User-Agent: NBE/WIP 0.0 - Custom browser engine.\r\n"
                request += "\r\n"  # newline. Has to be double to specify end of message
                sock.send(request.encode("utf8"))  # converts str into bytes

                response = sock.makefile("r", encoding="utf8", newline="\r\n")
                statusline = response.readline()
                version, status, explanation = statusline.split(" ", 2)
                response_headers = {} #For the headers, I split each line at the first colon and fill in a map of header names to header values.
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

                print("request: " + str(request))

                return content


#coordinates are x pos, y pos, x size, y size
WIDTH, HEIGHT = 1440, 660
HSTEP, VSTEP = 9, 12 #characters spacing
SCROLL_STEP = 100

class UI:
    def __init__(self):
        self.scroll = 100
        self.window = tkinter.Tk()
        self.window.bind("<Down>", "test")
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT,
        )
        self.canvas.pack()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            self.canvas.create_text(x, y - self.scroll, text=c)


    def load(self, link):
        body = link.request() #take the text from the request
        text = lex(body) #excludes tags.
        self.display_list = layout(text)
        self.draw()

        cursor_x, cursor_y = HSTEP, VSTEP
        for c in text:
            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP
            self.canvas.create_text(cursor_x, cursor_y, text=c) #draws text based on cursor
            cursor_x += HSTEP

    def scroll(self, e):
        self.scroll += SCROLL_STEP
        self.draw()



def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        display_list.append((cursor_x, cursor_y, c))
    return display_list


def lex(body):
    text = ""
    in_tag = False  # defines if body is within <> or not through bool
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c
    return text