import threading
import web
import json
import logging
from transaction import TransactionContext
from route_resolver import resolve_route
from slack_messaging_thread import SlackMessagingThread

log = logging.getLogger(__name__)
class get_bus:
    def GET(self):
        input_params = dict(
            route=web.input().text,
            user=web.input().user_name
        )
        log.info("Received request for bus: {0}".format(json.dumps(input_params)))
        SlackMessagingThread.queue.put((TransactionContext.MBTA_BUS_TXN_CONTEXT, input_params))
        return ''

class get_alert:
    def GET(self):
        input_params = dict(
            route=web.input().text,
            user=web.input().user_name
        )
        log.info("Received request for alert: {0}".format(json.dumps(input_params)))
        SlackMessagingThread.queue.put((TransactionContext.MBTA_ALERT_TXN_CONTEXT, input_params))
        return ''

class get_alerts:
    def GET(self):
        input_params = dict(
            user=web.input().user_name
        )
        log.info("Received request for alerts: {0}".format(json.dumps(input_params)))
        SlackMessagingThread.queue.put((TransactionContext.MBTA_ALERTS_TXN_CONTEXT, input_params))
        return ''

class RestAPIThread(threading.Thread):
    class SlackApp(web.application):
        def run(self, *middleware):
            log.info("Starting web application with address {0}:{1}".format(self.opts.ip, self.opts.port))
            func = self.wsgifunc(*middleware)
            return web.httpserver.runsimple(func, server_address=(self.opts.ip, self.opts.port))
    def __init__(self, opts, *args, **kwargs):
        super(RestAPIThread, self).__init__(*args, **kwargs)
        self.opts = opts
    def run(self):
        urls = (
            '/bus', 'get_bus',
            '/alert', 'get_alert',
            '/alerts', 'get_alerts'
        )
        app = self.SlackApp(urls, globals())
        app.opts = self.opts
        app.run()
