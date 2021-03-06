#!/usr/bin/python
#
# Author: K. Walsh <kwalsh@cs.holycross.edu>
# Project by John Williams and Anthony Green
# Date: 9 February 2017 (geolocate)
# Date: 23 March 2017
#
# Everything is working to our knowledge, though sometimes strange, nearly impossible to replicate bugs occur.  These
# can do everything from cause a massive crash to cause a small delay.  Rerunning the program with no changes resolves
# them.  We took about 18 hours on this project.
#
# Geolocation service top level program. Run it like this:
#   ./geolocation.py <CentralIP> <Port>
# or like this:
#   python geolocation.py <CentralIP> <Port>
# where <CentralIP> is the IP address (or the DNS host name) of the host that
# will be the central coordinator, and <Port> is the port on which the central
# coordinator will serve HTTP requests from users.
# Recent as of 7:16PM, on 3/23/17

import sys            # for sys.argv
import aws            # for aws.region_for_zone
import gcp            # for gcp.region_for_zone
import cloud          # for cloud.region_cities, etc.

# Get the central_host name and port number from the command line
central_host = sys.argv[1]
central_port = int(sys.argv[2])

# Figure out our own host name.
try:
    # First try AWS meta-data service to figure out our own ec2 availability zone and region.
    my_dns_name = aws.get_my_dns_hostname()
    my_ipaddr = aws.get_my_external_ip()
    my_zone = aws.get_my_zone()
    my_region = aws.region_for_zone(my_zone)
except:
    # Next try GCP meta-data service.
    my_dns_name = gcp.get_my_internal_hostname()
    my_ipaddr = gcp.get_my_external_ip()
    my_zone = gcp.get_my_zone()
    my_region = gcp.region_for_zone(my_zone)

if my_dns_name == central_host or my_ipaddr == central_host:
    # If we are the central coordinator host...
    # then call some function that implements the front end and central coordinator.
    # This code assumes there is a file named central.py containing a function
    # named run_central_coordinator(). Alternatively, you can delete these two lines and
    # put your central coordinator code right here.
    print "Starting central coordinator at http://%s:%s/" % (central_host, central_port)
    from central import *
    run_central_coordinator(my_ipaddr, my_zone, my_region, central_host, central_port)
else:
    # Otherwise, we are one of the pinger server hosts...
    # then call some function that implements the pinger server.
    # This code assumes there is a file named pinger.py containing a function
    # named run_pinger_server(). Alternatively, you can delete these two lines and
    # put your pinger server code right here.
    print "Starting pinger within region %s (city: %s, coordinates: %s)" % (
            my_region, cloud.region_cities[my_region], cloud.region_coords[my_region])
    from pinger import *
    run_pinger_server(my_dns_name, my_region, central_host, central_port)
