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
    # theSock.bind(address) # TODO: i believe i need this?
    # theSock.listen(1) # TODO: i believe i dont need to listen
    # removed looping as per walsh's recommendation
    #check loop for connections, try connection, if fail sleep and try again
    connection = theSock.connect(address)
    # TODO: add a loop to try several times to connect in event of failure
    connection.sendall("PING")
<<<<<<< HEAD
    while True: # TODO: check this condition
=======
    while True:
>>>>>>> 0f107723f332619a9ce83b7d77ae4581d451796e
        incoming = connection.recv(4096)
        targetValues = parser(incoming)
        sendTime = time.time()
        outbound = connectToTarget(targetValues[1], targetValues[2], targetValues[3])
        # TODO: fix this, rtt not found here
        lineList = outbound.splitlines()
        print "line: ", lineList[2]
        requestList = lineList[2].split(' ')
        rtt = sendTime - requestList[2]
        connection.sendall(rtt)
