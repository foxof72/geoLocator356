# Uses Prof. Walsh's code, modified by Anthony Green and John Williams
# Author: K. Walsh <kwalsh@cs.holycross.edu>
# Date: 15 January 2015

import os  # for os.path.isfile()
import socket  # for socket stuff
import urllib  # for urllib.unquote()()

import urlParser

# Global "configuration" variables, with default values
server_host = ""  # emptystring means "use any available network interface"
server_port = 8888
server_root = "form.html"  # file for landing page

# Global variable for list and a flag for pingers
ping_list = []
pinger_bool = False

def handle_geolocate(name): #return the url and port number for the request
    global ping_list
    print "Handling geolocation"
    path, host, port = urlParser.parser(name)

    mime_type = get_mime_type(name)

    count = 0
    while count < len(ping_list):
        try:
            p = ping_list[count]
            p.sendall(path+':='+host+':='+str(port))
            count += 1
        except:
            ping_list.pop(count)

    count = 0
    result = []
    while count < len(ping_list):
        p = ping_list[count]
        result.append(p.recv(4096))
        count += 1
    return "200 Ok", mime_type, result


# handle_file_request returns a status code, mime-type, and the body of a file
# for the given path, or an appropriate message if an error was encountered.
def handle_file_request(path):
    print "Handling file request for", str(path)
    try:
        if not os.path.isfile(path):
            print "File was not found: " + str(path)
            return ("404 NOT FOUND", "text/plain", "No such file: " + path)
        data = open(path).read()
    except:
        print "Error encountered reading from file"
        return ("403 FORBIDDEN", "text/plain", "Permission denied: " + path)
    mime_type = get_mime_type(path)
    return ("200 OK", mime_type, data)


# handle_request() returns a status code, mime-type, and body for the given url.
def handle_request(url):
    url = urllib.unquote(url)
    if url.startswith("/geolocate"):
        return handle_geolocate(url)
    elif url.startswith("/"):
        path = server_root
        return handle_file_request(path)
    else:
        print "Unrecognized url prefix"
        return ("404 NOT FOUND", "text/plain", "No such resource: " + url)


# get_mime_type() tries to guess the mime-type for a given path.
def get_mime_type(path):
    path = path.lower()
    if path.endswith('.jpg') or path.endswith('.jpeg'):
        return 'image/jpeg'
    elif path.endswith('.png'):
        return 'image/png'
    elif path.endswith('.txt'):
        return 'text/plain'
    elif path.endswith('.css'):
        return 'text/css'
    elif path.endswith('.js'):
        return 'application/javascript'
    else:
        return 'text/html'

# this finds the fastest rtt time
def fastest(rttList):
    fast = 100000000000000000000000.0  # impossibly large number as default value
    i = 0
    while i < len(rttList):
        if rttList[i] != '':
            valueList = rttList[i].split('=')
            if float(fast) >= float(valueList[2]):
                fast = valueList[2]
        i += 1
    return str(fast)

# handle_http_connection reads an HTTP request from socket c, parses and handles
# the request, then sends the response back to socket c.
def handle_http_connection(c):
    global ping_list, pinger_bool
    data = c.recv(4096)
    if not data:
        print "Empty request"
        return

    headers, body = data.split("\r\n\r\n", 1)
    if 'PING' in headers:  # if this is a ping request, store the socket in the list and set the bool to true
        ping_list.append(c)
        pinger_bool = True
        return
    first_line, headers = headers.split("\r\n", 1)
    method, url, version = first_line.split()
    code, mime_type, rttList = handle_request(url)
    if (rttList[1].startswith("RESULT") or rttList[1].startswith('')) and "</html>" not in rttList:
        #This block of code organizes the results of the geolocation
        i = 0
        fancyList = []  # max number of pings is 50
        fastestValue = fastest(rttList)
        while i < len(rttList):  # for every received result
            if rttList[i] != '':
                cosList = rttList[i].split('=')  # list of value to be used for cosmetic purposes
                if "Errno" not in cosList[2]:
                    # this makes a nice sentence of results
                    fancy = "Name: " + cosList[1] + ".  Result: " + cosList[2] + "ms.  " + "Region: " + cosList[3]
                elif "Errno" in cosList[2]:
                    fancy = "Warning: Error-Name: " + cosList[1] + ".  Error: " + cosList[2] + "  " + "Region: " + cosList[3]
                fancyList.append(str(fancy))  # adds string containing fancy result into list of result to be displayed
            i += 1
        fancyList.append("Fastest RTT: " + str(fastestValue))
        strRttList = '<br>'.join(fancyList)
    else:
        strRttList = rttList
    c.sendall("HTTP/1.0 " + code + "\r\n")
    c.sendall("Server: central\r\n")
    c.sendall("Content-type: " + mime_type + "\r\n")
    c.sendall("Content-Length: " + str(len(strRttList)) + "\r\n")
    c.sendall("\r\n")
    c.sendall(strRttList)


def run_central_coordinator(my_ipaddr, my_zone, my_region, central_host, central_port):

    global pinger_bool


    # Print a welcome message
    server_addr = ('', int(central_port)) # due to an odd error, port must be left as ''
    print "Starting web server"
    print "Listening on address", server_addr
    print "Serving files from", server_root

    # Create the server socket, and set it up to listen for connections
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(server_addr)
    s.listen(5)

    try:
        # Repeatedly accept and handle connections
        while True:
            pinger_bool = False
            c, client_addr = s.accept()
            print "Handling connection from", client_addr
            handle_http_connection(c)
            if not pinger_bool:
                c.close()
                print "Done with connection from", client_addr
            # Update status/performance counters
    finally:
        # Clean up
        s.close()
