# ping servers

from urlParser import *
from aws import *
from gcp import *
import socket

# runs in geolocate.py, do not change function name
def run_pinger_server(my_dns_name, my_region, central_host, central_port):
    try:
        name = "" #default value for name
        try:  # aws values
            name = get_my_dns_hostname()
        except Exception as e:  # gcp values
            name = get_my_internal_hostname()
        theSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (central_host, central_port)
        print "pinger server connecting to ", address
        for i in range(0, 3):
            try:
                theSock.connect(address)
                break
            except Exception as e:
                print "connection failed. Retrying " + str(3 - i) + " times. Error: " + str(e)
                time.sleep(5)  # in event of failure, sleep for 5 seconds
        theSock.sendall("PING=" + my_dns_name + "\r\n\r\n")
        print "pinger server connected to ", address
        while True:
            incoming = theSock.recv(4096)
            print "received from central: " + incoming
            outbound = connectToTarget(incoming)
            theSock.sendall("RESULT=" + name + "=" + str(outbound) + "=" + my_region)
    except Exception as e:
        print "connection failed.  Error: " + str(e)
        while True:
            theSock.sendall("RESULT=" + name + "=" + str(e) + "=" + my_region)


