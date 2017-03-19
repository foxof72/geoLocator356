# ping servers

from urlParser import *
import socket
import time

# this function determines the RTT of the target
# def clocker(incoming):
#     urlTime = parser(incoming)
#     currentTime = time.time()
#     elaspedTime = currentTime-urlTime[1]
#     timeResponse = "Passed time="+elaspedTime
#     return timeResponse

# runs in geolocate.py, do not change function name
def run_pinger_server():
    theSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('serverAddress', 8072) # these are placeholder values, need to add the actual values for central
    print "pinger server connecting to ", address
    theSock.bind(address) # TODO: i believe i need this?
    # theSock.listen(1) # TODO: i believe i dont need to listen
    # removed looping as per walsh's recommendation
    connection = theSock.connect(address)
    connection.sendall("PING")
    while connection is not None: # TODO: check this condition
        incoming = connection.recv(4096)
        targetValues = parser(incoming)
        sendTime = time.time()
        outbound = connectToTarget(targetValues[1], targetValues[2], targetValues[3])
        lineList = outbound.splitlines()
        print "line: ", lineList[2]
        requestList = lineList[2].split(' ')
        rtt = sendTime - requestList[2]
        connection.sendall(rtt)
