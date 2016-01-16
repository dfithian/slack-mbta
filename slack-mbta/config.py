import json
import logging
from output import SlackOutputter

log = logging.getLogger(__name__)
class Config(object):
    def __init__(self, file):
        try:
            log.info('loading config')
            self.load(json.loads(open(file, 'r').read()))
        except Exception:
            log.exception('failed to load config due to exception')
            self.load({})
    def load(self, json):
        self.host = json.get('host')
        self.port = json.get('port')
        self.outputter = SlackOutputter()
        self.webhook_url = json.get('webhook_url')
