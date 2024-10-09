import tkinter

#tkinter.mainloop() #while true, for each event, draw screen
WIDTH, HEIGHT = 800, 600

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Cavas(
            self.window,
            width=WIDTH,
            height=HEIGHT,
        )
        self.canvas.pack()

    def load(link):
        body = link.request()
        show(body)  # both lines show complete page by chaining request and body

