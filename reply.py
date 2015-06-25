import abc
import json

"""Represents a reply object from the server"""

class Reply(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, config):
        self.config = config
    @abc.abstractmethod
    def __call__(self):
        """Return information from server in a human-readable format"""

class MBTAReply(Reply):
    def adopt(self, j):
        self.dictionary = json.loads(j)

class MBTABusReply(MBTAReply):
    def __call__(self):
        return ['MBTABusReply object'] # FIXME format reply object

class MBTAAlertReply(MBTAReply):
    def __call__(self):
        return ['MBTAAlertReply object'] # FIXME format reply object

class OutgoingSlackReply(Reply):
    def adopt(self, msg):
        self.dictionary = { 'response_message' : msg }
    def __call__(self):
        return ['OutgoingSlackReply object'] # FIXME format reply object
