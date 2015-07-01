import json
import urllib
import urllib2
import logging
from request import MBTAAlertsRequest, MBTAAlertRouteRequest, MBTABusRequest
from reply import MBTAAlertsReply, MBTABusReply

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
        log.info('About to send request with payload {0} to url {1}'.format(data, self.request.url))
        try:
            j = urllib2.urlopen(req).read()
            log.info('Got raw reply {0}'.format(j))
            self.reply.adopt(j)
        except Exception:
            log.exception('Got exception during do_transaction()')
            self.reply.adopt("{}")
    @staticmethod
    def MBTA_BUS(config, bus):
        return TransactionContext(MBTABusRequest(bus), MBTABusReply(config))
    @staticmethod
    def MBTA_ALERT(config, route):
        return TransactionContext(MBTAAlertRouteRequest(route), MBTAAlertsReply(config))
    @staticmethod
    def MBTA_ALERTS(config):
        return TransactionContext(MBTAAlertsRequest(), MBTAAlertsReply(config))
