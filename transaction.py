import json
import urllib2
from request import AlertRequest, BusRequest
from reply import AlertReply, BusReply

class TransactionContext(object):
    def __init__(self, request, reply):
        self.request = request
        self.reply = reply
    def do_transaction(self):
        req = self.request()
        print 'About to send request ' + req
        raw = urllib2.urlopen(req).read()
        print 'Got raw reply ' + raw
        self.reply.adopt(json.loads(raw))
        return self.reply
    @staticmethod
    def ALERT(config):
        return TransactionContext(AlertRequest(), AlertReply(config))
    @staticmethod
    def BUS(config, bus):
        return TransactionContext(BusRequest(bus), BusReply(config))
