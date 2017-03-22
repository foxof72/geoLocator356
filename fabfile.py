# This is a basic fabric configuration file for deploying and running code on EC2.
#
# Author: kwalsh@cs.holycross.edu
# Date: January 25, 2015.
#
# To deploy code to all EC2 hosts, run this command on radius:
#   fab -P deploy
# To run the code on all EC2 hosts, run this command on radius:
#    fab -P start
# To do both, run this command on radius:
#    fab -P deploy start
#
# You can edit this file however you like, but update the instructions above if
# you do so that it is clear how to deploy and start your geolocate service.

from fabric.api import hosts, run, env
from fabric.operations import put

# This is the list of EC2 hosts. Add or remove from this list as you like.
env.hosts = [
        '104.199.244.68', # gcp, Mordor
        '35.187.207.40', # gcp, serenity
        '104.199.47.244', # gcp, Tatoonie
        ]
env.user = 'jmwill18'
env.key_filename = '~/.ssh/cloud_sshkey'

# The deploy task copies all python files from local directory to every EC2 host.
def deploy():
    put('*.py', '~/')
    put('form.html', '~/')

# The start task runs the geolocate.py command on every EC2 host.
def start():
    run('python geolocate.py 104.199.47.244 8088')
