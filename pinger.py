# ping servers

from urlParser import *
import socket
import sys
import time

theSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# this function sends a greeting to central
def greeting():
    global theSock
    greet = """
HEAD /specialHello HTTP2.0 OK

    """
    theSock.send(greet)

# this function determines the RTT of the target
def clocker(incoming):
    urlTime = parser(incoming)
    currentTime = time.time()
    elaspedTime = currentTime-urlTime[1]
    timeResponse = "Passed time="+elaspedTime
    return timeResponse

def run_pinger_server():
    global theSock
    address = ('serverAddress', 8072) # these are placeholder values, need to add the actual values for central
    print "pinger server connecting to ", address
    theSock.bind(address)
    theSock.listen(1)
    while True:
        try:
            server , clientAddress = theSock.accept()
            while True:
                try:
                    incomingURL = server.recv(4096)
                    greeting()
                    rtt = clocker(incomingURL)
                    server.sendall(rtt) # this might need to get moved
                except Exception as inner:
                    print "Error occurred, escaping inner while.  Error: " + inner
                    server.close()
                    break
        except Exception as outer:
            print "Error occurred, escaping while.  Error: " + outer
            if server is not None:
                server.close()
            break
    print "connection exited"
