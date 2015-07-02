import threading
import web
import json
import logging
from config import Config
from output import OutputFactory
from transaction import TransactionContext
from route_resolver import resolve_route
from slack_messaging_thread import SlackMessagingThread

log = logging.getLogger(__name__)
def config():
    return Config.instance()
def outputter():
    return OutputFactory.get_outputter(config())

def transaction_flow(txn_context, config, outputter):
    txn_context.do_transaction()
    return outputter.format(txn_context.request, txn_context.reply)

class get_bus:
    def GET(self):
        input_params = dict(
            route=web.input().text,
            user=web.input().user_name
        )
        log.info("Received request for bus: {0}".format(json.dumps(input_params)))
        payload = transaction_flow(
            TransactionContext.MBTA_BUS_TXN_CONTEXT(
                config(),
                input_params
            ),
            config(),
            outputter()
        )
        SlackMessagingThread.queue.put(payload)
        log.info("Enqueued payload {0}".format(payload))
        return ''

class get_alert:
    def GET(self):
        input_params = dict(
            route=web.input().text,
            user=web.input().user_name
        )
        log.info("Received request for alert: {0}".format(json.dumps(input_params)))
        payload = transaction_flow(
            TransactionContext.MBTA_ALERT_TXN_CONTEXT(
                config(),
                input_params
            ),
            config(),
            outputter()
        )
        SlackMessagingThread.queue.put(payload)
        log.info("Enqueued payload {0}".format(payload))
        return ''

class get_alerts:
    def GET(self):
        input_params = dict(
            user=web.input().user_name
        )
        log.info("Received request for alerts: {0}".format(json.dumps(input_params)))
        payload = transaction_flow(
            TransactionContext.MBTA_ALERTS_TXN_CONTEXT(
                config(),
                input_params
            ),
            config(),
            outputter()
        )
        SlackMessagingThread.queue.put(payload)
        log.info("Enqueued payload {0}".format(payload))
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
