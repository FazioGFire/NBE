from small_tests import URL
from small_tests import load
import sys  # so we can run the command line


if __name__ == "__main__":  # run only in main
    link = load(sys.argv[1])

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
