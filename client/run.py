import os
import json
import client 

runs = 1
headless = False
trackevents = False
host = ''
username = ''
password = ''
duration = 0
connection_string = ''

#get the response
postreqdata = json.loads(open(os.environ['req']).read())
response = open(os.environ['res'], 'w')

#red the required paramsd
runs = postreqdata['runs']
headless = postreqdata['headless']
trackevents = postreqdata['trackevents']
host = postreqdata['host']
username = postreqdata['username']
password = postreqdata['password']
duration = postreqdata['duration']
connection_string = postreqdata['connection_string']

#acknowledge the params
response.write("runs {0}, headless: {1}, trackevents: {2}, host: {3}, username: {4}, duration: {5}, connection_string: {6}".format(runs, headless, trackevents, host, username, duration, connection_string))
response.write("starting client...")

response.close()