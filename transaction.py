import json
import urllib, urllib2
from request import MBTAAlertRequest, MBTABusRequest, OutgoingSlackRequest
from reply import MBTAAlertReply, MBTABusReply, OutgoingSlackReply

class TransactionContext(object):
    def __init__(self, request, reply):
        self.request = request
        self.reply = reply
    def do_transaction(self):
        if self.request.payload is None:
            data = None
            req = urllib2.Request(self.request.url)
        else:
            data = json.dumps(self.request.payload)
            req = urllib2.Request(self.request.url, data)
        print ('About to send request with payload %r to url %r' % (data, self.request.url))
        j = urllib2.urlopen(req).read()
        print 'Got raw reply ' + j
        self.reply.adopt(j)
        return self.reply
    @staticmethod
    def MBTA_ALERT(config):
        return TransactionContext(MBTAAlertRequest(), MBTAAlertReply(config))
    @staticmethod
    def MBTA_BUS(config, bus):
        return TransactionContext(MBTABusRequest(bus), MBTABusReply(config))
    @staticmethod
    def SLACK_OUTGOING(config, payload):
        return TransactionContext(OutgoingSlackRequest(payload), OutgoingSlackReply(config))
