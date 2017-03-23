# ping servers

from urlParser import *
from aws import *
from gcp import *
import socket

# runs in geolocate.py, do not change function name
def run_pinger_server(my_dns_name, my_region, central_host, central_port):
    # TODO: add error check for a bogus url
    theSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (central_host, central_port) # these are placeholder values, need to add the actual values for central
    print "pinger server connecting to ", address
    # removed looping as per walsh's recommendation
    # check loop for connections, try connection, if fail sleep and try again
    for i in range(0, 3):
        try:
            theSock.connect(address)
            break
        except Exception as e:
            print "connection failed. Retrying " + str(3 - i) + " times. Error: " + str(e)
            time.sleep(5) # in event of failure, sleep for 5 seconds
    theSock.sendall("PING=" + my_dns_name + "\r\n\r\n")
    print "connected to ", address
    while True:
        incoming = theSock.recv(4096)
        print "received from central: " + incoming
        outbound = connectToTarget(incoming)
        try:
            name = get_my_internal_hostname()
        except Exception as e:
            name = get_my_dns_hostname()
        theSock.sendall("RESULT=" + name + "=" + str(outbound))
