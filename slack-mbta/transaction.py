import urllib
import urllib2
import logging
from const import ROUTE_ENDPOINT, ALERTS_ENDPOINT, ALERT_ENDPOINT
from request import MBTAAlertsRequest, MBTAAlertRouteRequest, MBTARouteRequest, SlackRequest
from reply import MBTAAlertsReply, MBTARouteReply, SlackReply

log = logging.getLogger(__name__)
def make_mbta_context(endpoint, params):
    if endpoint == ROUTE_ENDPOINT:
        return TransactionContext(MBTARouteRequest(params), MBTARouteReply())
    elif endpoint == ALERTS_ENDPOINT:
        return TransactionContext(MBTAAlertsRequest(params), MBTAAlertsReply())
    elif endpoint == ALERT_ENDPOINT:
        return TransactionContext(MBTAAlertRouteRequest(params), MBTAAlertsReply())
    else:
        return None

def make_slack_context(mbta_context, params):
    return TransactionContext(SlackRequest(mbta_context), SlackReply())

class TransactionContext(object):
    def __init__(self, request, reply):
        self.request = request
        self.reply = reply
    def do_transaction(self):
        if self.request.payload is None:
            data = None
            req = urllib2.Request(self.request.url)
        else:
            data = urllib.urlencode(self.request.payload)
            req = urllib2.Request(self.request.url, data)
        log.info('about to send request with payload {0} to url {1}'.format(data, self.request.url))
        try:
            j = urllib2.urlopen(req).read()
            log.info('got raw reply {0}'.format(j))
            self.reply.adopt(j)
        except Exception:
            log.exception('got exception during transaction')
            self.reply.adopt("{}")
