import json
import logging
from output import SlackOutputter

log = logging.getLogger(__name__)
class Config(object):
    def __init__(self, file):
        if file is None:
            self.load({})
        else:
            try:
                self.load(json.loads(open(file, 'r').read()))
            except Exception:
                log.exception('failed to load config due to exception')
            finally:
                self.load({})
    def load(self, json):
        self.host = getattr(json, 'host', 'localhost')
        self.port = getattr(json, 'port', 8080)
        self.max_bus_lines = getattr(json, 'max_bus_lines', 3)
        self.max_alerts = getattr(json, 'max_alerts', 3)
        self.outputter = SlackOutputter()
        self.webhook_url = getattr(json, 'webhook_url', 'https://hooks.slack.com/services/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')
