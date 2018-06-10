import uuid
import json
import datetime
from enum import Enum
from enum import IntEnum

# what type of operation type is being performed
class OpType(IntEnum):
    other = 0
    read = 1
    write = 2
    search = 3
    delete = 4,
    post = 5,
    error = 6

#ref: https://www.experts-exchange.com/questions/22591850/Convert-timedelta-to-milliseconds.html
def timedelta_milliseconds(td):
    return td.days*86400000 + td.seconds*1000 + td.microseconds/1000

# ref https://code.tutsplus.com/tutorials/how-to-work-with-json-data-using-python--cms-25758
def jsonDefault(value):
    try:
        if isinstance(value, datetime.timedelta):
            return timedelta_milliseconds(value)
        elif isinstance(value, datetime.datetime):
            #ref: https://docs.python.org/2/library/datetime.html#datetime-objects
            return str(value.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        elif isinstance(value, uuid.UUID):
            return str(value)
        #elif isinstance(value, OpType):
        #    return str(value)
        else: 
            return value.__dict__
    except Exception as e:
        print('Error creating pstat for {0}: {1}'.format(value, e))
        raise e

#Perfromance stat class
#stores the data related to the operation being monitored
class PerfStat(object):
    def __init__(self,host,user,title,optype,start,stop,description,client=None, id=None):
        self.host = host
        self.user = user
        self.title = title
        self.type = optype
        self.start = start
        self.stop = stop
        self.duration = self.stop - self.start
        self.id = id
        self.client = client
        self.description = description

        if self.id is None:
            self.id = uuid.uuid4()

        if self.client is None:
            self.client = uuid.uuid4()

    def json(self):
        return('{0}'.format(json.dumps(self, default=jsonDefault)))

