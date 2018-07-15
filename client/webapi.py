from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
#from flask.ext.jsonpify import jsonify
#import jsonify

import client 

app = Flask(__name__)
api = Api(app)


@app.route('/client', methods=['GET', 'POST'])
def get():
    
    runs = request.args.get('runs', default = 1, type = int)
    duration = request.args.get('duration', default = 0, type = int)
    endpoint = request.args.get('endpoint', default = '', type = str)
    keyname = request.args.get('keyname', default = '', type = str)
    key = request.args.get('key', default = '', type = str)
    path = request.args.get('path', default = '', type = str)
    host = request.args.get('host', default = '', type = str)

    connection_string = 'Endpoint=sb://{0}/;SharedAccessKeyName={1};SharedAccessKey={2};EntityPath={3}'.format(endpoint, keyname, key, path)
    print("runs {0}, headless: {1}, trackevents: {2}, host: {3}, username: {4}, duration: {5}, connection_string: {6}".format(runs, True, True, host, '', duration, connection_string))
    print("starting client...")

    #start the cient
    client.runClient(int(runs), True,  True, host, '', '', int(duration), connection_string)
    return '{0}'.format(True)

if __name__ == '__main__':
     app.run(port='9999')