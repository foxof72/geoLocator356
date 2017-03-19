# Created by John Williams
# This parses incoming HTTP requests for use

import socket
import urllib
import time
global startTime


# this function connects to the url that is being targeted
def connectToTarget(path, url, port):
    theSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (url, port)
    print "connecting to target", address
    theSock.bind(address) # TODO: believe i need to bind
    # TODO: theSock.listen(1) don't believe i need to listen
    connection = theSock.connect(address)
    http = """GET """ + path + url + path + """ HTTP1.0 OK\n\r
    Date: """ + time.time() + """
    """ # TODO: verify this request is formatted properly
    connection.sendall(http)
    incoming = connection.recv(4096)
    # where incoming is HTTP request from targeted server
    return incoming

def parser(request):
    print "request:", request
    # lineList = []
    # requestList = []
    # timeList = []
    # hostList = []
    lineList = request.splitlines()
    print "line: ", lineList[1]
    requestList = lineList[1].split(' ')
    decoded = urllib.unquote(requestList[1])
    print "decoded", decoded
    path, target = decoded.split('?')
    trash, host = target.split('=')
    trash, urlWithPort = host.split('://')
    print "host with port: ", urlWithPort
    url, port = urlWithPort.split(':')
    return path, url, port


def main():
    testValue = """
GET /geolocate?target=https%3A%2F%2Fwww.mountainproject.com/fourms/southerncalifornia:8072 HTTP2.0 OK'
sentAt: """ + str(time.time()) + """
Server: test
isRealRequest = false
Content-Length: 8 bytes
Date: now

"""
    result = parser(testValue)
    print "Returns: ", result

if __name__ == '__main__':
    main()