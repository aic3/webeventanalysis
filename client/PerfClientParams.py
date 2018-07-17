class PerfClientParams():
    def __init__(self, host, runs, duration, username, password, event_hub, hub_name, keyname, key):
        #assign the local variables
        self.host = host
        self.runs = int(runs)
        self.duration = int(duration) 
        self.username = username
        self.password = password
        self.event_hub = event_hub
        self.hub_name = hub_name
        self.keyname = keyname
        self.key = key

        #build the connection string
        self.connection_string = "Endpoint=sb://{0}/;SharedAccessKeyName={1};SharedAccessKey={2};EntityPath={3}".format(self.event_hub, self.keyname, self.key, self.hub_name)


