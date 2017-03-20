# ping servers

import thread
from urlParser import *
from aws import *
from gcp import *
import socket

# runs in geolocate.py, do not change function name
def run_pinger_server():
    # TODO: add error check for a bogus url
    theSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('serverAddress', 8072) # these are placeholder values, need to add the actual values for central
    print "pinger server connecting to ", address
    # removed looping as per walsh's recommendation
    # check loop for connections, try connection, if fail sleep and try again
    for i in range(0, 3):
        try:
            connection = None
            connection = theSock.connect(address)
            if connection is not None: # this means connection has been established
                break
        except Exception as e:
            print "connection failed. Retrying " + 3 - i + " times. Error: " + str(e)
            thread.sleep(5000) # in event of failure, sleep for 5 seconds
    connection.sendall("PING=" + get_my_external_ip())
    while True:
        incoming = connection.recv(4096)
        print "received from central: " + incoming
        outbound = connectToTarget(incoming)
        connection.sendall("RESULT=" + outbound)
