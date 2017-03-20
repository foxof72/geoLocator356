# Uses Prof. Walsh's code, modified by John Williams
# Author: K. Walsh <kwalsh@cs.holycross.edu>
# Date: 15 January 2015
#
# A simple web server from scratch in Python. Run it like this:

import os  # for os.path.isfile()
import socket  # for socket stuff
import sys  # for sys.argv
import urllib  # for urllib.unquote()()
import time  # for time.time()

# Global "configuration" variables, with default values
server_host = ""  # emptystring means "use any available network inerface"
server_port = 8888
server_root = "./web_files"

# Global "status/performance" counter variables
num_connections = 0
num_requests = 0
num_errors = 0
tot_time = 0  # total time spent handling requests
avg_time = 0  # average time spent handling requests
max_time = 0  # max time spent handling a request


# handle_status_request returns a status code, mime-type, and message
# appropriate for the special "/status" url.
def handle_status_request():
    print "Handling status request"
    return ("200 OK",
            "text/plain",
            "Web server by kwalsh, modified by John Williams\n" +
            "\n" +
            str(num_connections) + " connections handled (including this one)\n" +
            str(num_requests) + " requests handled (including this one)\n" +
            str(num_errors) + " errors encountered\n" +
            str(avg_time) + "s average request handling time (not including this one)\n" +
            str(max_time) + "s slowest request handling time (not including this one)\n")


# handle_hello_request returns a status code, mime-type, and message
# appropriate for the special "/hello" url.
def handle_hello_request():
    print "Handling hello request"
    return ("200 OK",
            "text/plain",
            "Why, hello yourself!\n")


def handle_hello_name_request(name):
    print "Handling hello-name request"
    return ("200 OK",
            "text/plain",
            "Why, hello %s! How are you doing today?\n" % (name))

def handle_goelocate(name): #return the url and port number for the request
    print "Handling geolocation"
    #parse url, send to pinger
    #add pingers to list
    #error check to make sure pingers live
    return ()


# handle_file_request returns a status code, mime-type, and the body of a file
# for the given path, or an appropriate message if an error was encountered.
def handle_file_request(path):
    global num_errors
    print "Handling file request for", str(path)
    try:
        if not os.path.isfile(path):
            print "File was not found: " + str(path)
            num_errors = num_errors + 1
            return ("404 NOT FOUND", "text/plain", "No such file: " + path)
        data = open(path).read()
    except:
        print "Error encountered reading from file"
        num_errors = num_errors + 1
        return ("403 FORBIDDEN", "text/plain", "Permission denied: " + path)
    mime_type = get_mime_type(path)
    return ("200 OK", mime_type, data)


# handle_request() returns a status code, mime-type, and body for the given url.
def handle_request(url):
    global num_errors
    url = urllib.unquote(url)
    if url == "/status":
        return handle_status_request()
    elif url == "/hello":
        return handle_hello_request()
    elif url.startswith("/hello?"):
        name = url[7:]
        return handle_hello_name_request(name)
    elif url == "/geolocate":
        return handle_geolocate(url)
    elif url.startswith("/"):
        path = server_root + '/' + url[1:]
        return handle_file_request(path)
    else:
        print "Unrecognized url prefix"
        num_errors = num_errors + 1
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


# handle_http_connection reads an HTTP request from socket c, parses and handles
# the request, then sends the response back to socket c.
def handle_http_connection(c):
    global num_errors, num_requests
    data = c.recv(4096)
    if not data:
        print "Empty request"
        num_errors = num_errors + 1
        return
    num_requests = num_requests + 1
    headers, body = data.split("\r\n\r\n", 1)
    first_line, headers = headers.split("\r\n", 1)
    print "Request is:", first_line
    method, url, version = first_line.split()
    print "Method is", method, "url is", url, "version is", version
    code, mime_type, body = handle_request(url)
    c.sendall("HTTP/1.0 " + code + "\r\n")
    c.sendall("Server: central\r\n")
    c.sendall("Content-type: " + mime_type + "\r\n")
    c.sendall("Content-Length: " + str(len(body)) + "\r\n")
    c.sendall("\r\n")
    c.sendall(body)


def run_central_coordinator():

    # Print a welcome message
    server_addr = (server_host, server_port)
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
            c, client_addr = s.accept()
            print "Handling connection ", num_requests, "from", client_addr
            start = time.time()
            num_connections = num_connections + 1;
            handle_http_connection(c)
            end = time.time()
            c.close()
            print "Done with connection ", num_requests, "from", client_addr
            # Update status/performance counters
            duration = end - start
            tot_time = tot_time + (end - start)
            avg_time = tot_time / num_requests
            if duration > max_time:
                max_time = duration
    finally:
        print 'Server is shutting down'
        # Clean up
        s.close()