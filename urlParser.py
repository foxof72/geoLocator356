# Created by John Williams
# This parses incoming HTTP requests for use

import socket
import urllib
import time

# global startTime


# this function connects to the url that is being targeted
def connectToTarget(host):
    # TODO: put this whole function in a try except loop, loop this several times
    theSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    path, host, port = host.split(':=')
    address = (host, int(port))
    print "connecting to target", address
    theSock.connect(address)
    http = """GET """ + path + """ HTTP/1.0\r\n

    """ # TODO: verify this request is formatted properly, hint its not
    startTime = time.time()
    theSock.sendall(http)
    incoming = theSock.recv(4096)
    endTime = time.time()
    # where incoming is HTTP request from targeted server
    rtt = endTime-startTime
    return str(rtt)

def parser(request):
    lineList = request.splitlines()
    requestList = lineList[0].split(' ')
    decoded = urllib.unquote(requestList[0])
    order, target = decoded.split('?')
    trash, host = target.split('=')
    if '://' in host:
        trash, urlWithPort = host.split('://')
    else:
        urlWithPort = host
    try:
        host, port = urlWithPort.split(':')
    except Exception as e:
        host = urlWithPort
        port = 80
    try:
        host, path = host.split('/', 1)
    except Exception as e:
        host = urlWithPort
        path = "/"
    if path != "":
        path = '/' + path
    return path, host, port


def main():
    testValue = """
GET /geolocate?target=https%3A%2F%2Fwww.mountainproject.com HTTP/1.0'
"""
    result = parser(testValue)
    print "Returns: ", result

if __name__ == '__main__':
    main()