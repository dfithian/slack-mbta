import json
import urllib
import urllib2
import logging
from request import MBTAAlertsRequest, MBTAAlertRouteRequest, MBTABusRequest, OutgoingSlackRequest
from reply import MBTAAlertsReply, MBTABusReply, OutgoingSlackReply

log = logging.getLogger(__name__)
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
        log.info('About to send request with payload %r to url %r' % (data, self.request.url))
        try:
            j = urllib2.urlopen(req).read()
            log.info('Got raw reply ' + j)
            self.reply.adopt(j)
        except Exception:
            log.exception('Got exception during do_transaction()')
        return self.reply
    @staticmethod
    def MBTA_BUS(config, bus):
        return TransactionContext(MBTABusRequest(bus), MBTABusReply(config))
    @staticmethod
    def MBTA_ALERT(config, route):
        return TransactionContext(MBTAAlertRouteRequest(route), MBTAAlertsReply(config))
    @staticmethod
    def MBTA_ALERTS(config):
        return TransactionContext(MBTAAlertsRequest(), MBTAAlertsReply(config))
    @staticmethod
    def SLACK_OUTGOING(config, payload):
        return TransactionContext(OutgoingSlackRequest(payload), OutgoingSlackReply(config))
