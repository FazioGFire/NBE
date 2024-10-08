from MyBrowser import URL
from MyBrowser import load


if __name__ == "__main__":  # run only in main
    import sys  # so we can run the command line
    load(URL(sys.argv[1]))