# Created by John Williams
# This parses incoming HTTP requests for use
import urllib
import time

def parser(request):
    print "request:", request
    lineList = []
    requestList = []
    timeList = []
    lineList = request.splitlines()
    print "line: ", lineList[1]
    requestList = lineList[1].split(' ')
    decoded = urllib.unquote(requestList[1])
    trash, url = decoded.split('=')
    timeList = lineList[2].split(' ') # the second line contains the sent at value, these must line up
    return url, timeList[1]


def main():
    testValue = """
GET /geolocate?target=https%3A%2F%2Fwww.mountainproject.com/fourms/southerncalifornia HTTP2.0 OK'
sentAt: """ + str(time.time()) + """
Server: test
isRealRequest = false
Content-Length: 8 bytes
Date: now

"""
    result = parser(testValue)
    print "Returns: ", result[1]

if __name__ == '__main__':
    main()