import json
import socket
import sys
import getopt
import logging
from enum import Enum
from datetime import datetime
import base64
import hmac
import hashlib
import time
import urllib.request
import urllib.parse
import configparser


config_key_endpoint = 'Endpoint'
config_key_shared_access_key_name = 'SharedAccessKeyName'
config_key_shared_access_key = 'SharedAccessKey'
config_key_entity_path = 'EntityPath'
encoding = 'utf-8'

#ref: https://azure.microsoft.com/en-us/resources/samples/virtual-machines-python-scheduled-events-central-logging/
class EventQueue(object):
    API_VERSION = '2016-07'
    TOKEN_VALID_SECS = 10
    TOKEN_FORMAT = 'SharedAccessSignature sig=%s&se=%s&skn=%s&sr=%s'

    def __init__(self, connection_string):
        self.connection_string = connection_string

        # get the key value pairs from the connection string
        keyValues = dict((item.split('=', 1)) for item in self.connection_string.split(';'))
        
        self.endPoint = keyValues[config_key_endpoint].replace('sb://', '')
        self.keyName = keyValues[config_key_shared_access_key_name]
        self.keyValue = keyValues[config_key_shared_access_key]
        self.entityPath = keyValues[config_key_entity_path]

    #creates the session token
    def build_token(self):
        expiry = int(time.time() + 10000)

        string_to_sign = '{}\n{}'.format(urllib.parse.quote_plus(self.endPoint), expiry)
        key = self.keyValue.encode(encoding)
        string_to_sign = string_to_sign.encode(encoding)
        signed_hmac_sha256 = hmac.HMAC(key, string_to_sign, hashlib.sha256)
        signature = signed_hmac_sha256.digest()
        signature = base64.b64encode(signature)
        token = 'SharedAccessSignature sr={}&sig={}&se={}&skn={}'.format(urllib.parse.quote_plus(self.endPoint), urllib.parse.quote(signature), expiry, self.keyName)
        return token

    def send(self, msg):
        token = self.build_token()
        url = 'https://{}{}/messages?api-version={}'.format(self.endPoint, self.entityPath, self.API_VERSION)
        data = msg.encode('ASCII')

        req = urllib.request.Request(url, headers={'Authorization': token}, data=data, method='POST')
        with urllib.request.urlopen(req) as f:
            pass

        return f.read().decode(encoding)
