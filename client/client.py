import datetime
import os
import stat
import sys
import uuid
import json

import PerfClient
import PerfStat

from PerfClient import *
from PerfStat import *

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

#load the web driver
dir_path = os.path.dirname(os.path.realpath(__file__))
driverPath = os.path.abspath("{0}/{1}".format(dir_path, 'chromedriver.exe'))


def runCommand(client, command):
    start = datetime.datetime.now()

    try:
        #print('id: {0}, command: {1}, target: {2}, value: {3}'.format(command['id'], command['command'], command['target'], command['value']))
        pstat = client.runCommand( command['command'],  command['target'],  command['value'])
        print('{0}'.format(pstat.json()))
    except Exception as e:
        pstat = PerfStat(client.root_url,client.username, 'app.error', OpType.error, start, datetime.datetime.now(), 'id: {0}, command: {1}, target: {2}, value: {3}, Error: {4}, Source: {5}'.format(command['id'], command['command'], command['target'], command['value'], e, client.viewSource()), client.client)
        print('{0}'.format(pstat.json()))
        raise Exception(pstat.json())

#get a list of the commands in the config file
def getCommands():
    filepath =  os.path.abspath("{0}/{1}".format(dir_path, 'perftest.side'))
    with open(filepath) as data:
        script = json.load(data)

    #this could be expanded to handle multiple tests
    commands = script['tests'][0]['commands']

    return commands

#gets the event hubs connection string
def getEventHubConnectionString(trackevents):
    connection_string = ''

    settings_file = os.path.abspath("{0}/{1}".format(dir_path, 'queue.config.json'))
    with open(settings_file) as settings_data:
        settings = json.load(settings_data)
        if trackevents:
            connection_string = settings['connectionstring']

    return connection_string

#run the script file for a PerfTest client
def runClientScript(client):
    commands = getCommands()
    
    cmdlength = len(commands)
    #run for the specified number of iterations        
    for i in range (0, cmdlength):
        command = commands[i]
        
        runCommand(client, command)
    
#Run the perf test for a specified duration
def runClientScriptForDuration(client, duration):
    tsec = 0
    count = 0
    tstart = datetime.now()
    commands = getCommands()    
    cmdlength = len(commands)

    while tsec < duration:
        try:
            #get the command
            current = count % cmdlength 
            command = commands[current]

            runCommand(client, command)

            # update the stats
            td = datetime.now() - tstart 
            tsec = td.days*86400000 + td.seconds*1000 + td.microseconds/1000     
            count = count + 1
            print('Test runtime: {0}'.format(tsec))
        except Exception as e:
            print(e)
            count = 0

#ex: "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\python.exe" \dev\git\kabs\OdooDev\client.py "http://localhost" "fake@user.com" "" 10 1 1 10000
if __name__ == "__main__":
    #runClient()
    #test()
    runs = 1
    headless = False
    trackevents = False
    host = ''
    username = ''
    password = ''
    duration = 0
    connection_string = ''

    # host, username, password, runs, headless, trackevents, duration
    

    if len(sys.argv) > 1:
        host = str(sys.argv[1])

    if len(sys.argv) > 2:
        username = str(sys.argv[2])

    if len(sys.argv) > 3:
        password = str(sys.argv[3])
    

    if len(sys.argv) > 4:
        runs = int(sys.argv[4])

    if len(sys.argv) > 5:
        headless = bool(int(sys.argv[5]))

    if len(sys.argv) > 6:
        trackevents = bool(int(sys.argv[6]))
    
    if len(sys.argv) > 7:
        duration = int(sys.argv[7])

    clientid = uuid.uuid4()

    print('Host: {3}, Running {0} time(s), ClientId: {1}, Headless: {2}, Tracking: {4}'.format(runs, clientid, headless, host, trackevents))
    connection_string = getEventHubConnectionString(trackevents)
    if len(host) == 0:
        host = 'http://localhost'
    client = PerfClient(driverPath, host, username, password, 30, clientid, headless, connection_string)

    try:
        for i in range(0,runs):
            try:
                runClientScript(client)
                print('Complete: {0}'.format(i+1))
            except Exception as e:
                print('Error: {0} {1} {2}'.format(i+1,  sys.exc_info()[0], e))


        runClientScriptForDuration(client, duration)
    finally: 
        client.close()
    print('finished...')
