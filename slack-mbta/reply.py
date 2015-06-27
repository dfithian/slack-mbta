import abc
import json
import logging

"""Represents a reply object from the server"""
log = logging.getLogger(__name__)
class Reply(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, config):
        self.config = config
    @abc.abstractmethod
    def __call__(self):
        """Return information from server in a human-readable format"""

class MBTAReply(Reply):
    def adopt(self, j):
        try:
            self.dictionary = json.loads(j)
        except Exception:
            log.exception('Got exception loading invalid json %r' % (j))
            self.dictionary = dict()

class MBTABusReply(MBTAReply):
    def __call__(self):
        def parse_direction(direction):
            trips = direction["trip"]
            if trips is not None and len(trips) > 0:
                return (text["trip_name"] for text in trips)
            else:
                return ['No trips']
        directions = self.dictionary["direction"]
        if directions is not None and len(directions) > 0:
            parsed_directions = (parse_direction(direction) for direction in directions)
            return (pd for pds in parsed_directions for pd in pds)
        else:
            return ['No predictions']

class MBTAAlertsReply(MBTAReply):
    def __call__(self):
        headers = self.dictionary["alert_headers"]
        if headers is not None and len(headers) > 0:
            return (text["header_text"] for text in headers)
        else:
            return ['No alerts']

class OutgoingSlackReply(Reply):
    def adopt(self, msg):
        self.dictionary = { 'response_message' : msg }
    def __call__(self):
        return ['OutgoingSlackReply object'] # FIXME format reply object
