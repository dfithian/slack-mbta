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
    def adopt(self, dictionary):
        print 'Adopt called'
        self.dictionary = dictionary

class BusReply(Reply):
    def __call__(self):
        return ['BusReply object'] # FIXME format reply object

class AlertReply(Reply):
    def __call__(self):
        return ['AlertReply object'] # FIXME format reply object
