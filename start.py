import tkinter

from MyBrowser import URL
from MyBrowser import UI


if __name__ == "__main__":  # run only in main
    import sys  # so we can run the command line
    UI().load(URL(sys.argv[1]))
    tkinter.mainloop()