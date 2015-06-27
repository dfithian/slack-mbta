import os
import sys
import argparse
import web
import json
import logging
from route_resolver import resolve_route
from config import ConfigAction, Config
from transaction import TransactionContext
from output import OutputFactory

VERSION='1.0'
def start_logging(is_debug, log_file=None):
    logging.basicConfig(
        filename=log_file if log_file is not None else os.path.dirname(os.path.realpath(__file__))  + '/slack-mbta.log',
        level=(logging.DEBUG if is_debug else logging.INFO),
        format='%(asctime)s %(levelname)s - %(message)s'
    )
    log = logging.getLogger(__name__)
    log.info("Logger started with options is_debug=%r, log_file=%r" % (str(is_debug), log_file))
    log.info("Slack-MBTA version %r" % (VERSION))
    return log

def transaction_flow(txn_context, config, outputter):
    mbta_reply = txn_context.do_transaction()
    return json.dumps(outputter(mbta_reply))

parser = argparse.ArgumentParser(description="Get MBTA info", epilog="(c) 2015 Dan Fithian")

parser.add_argument("-c", dest="config", type=str, help="Provide a config file", const=None, action=ConfigAction)
parser.add_argument("-d", dest="debug", action="store_true", help="Enable debug logging")
parser.add_argument("-l", dest="log_file", type=str, help="Provide a log file", const=None)

# parse the config and set up inputs
args = parser.parse_args(sys.argv[1:])

# start logging
log = start_logging(args.debug, args.log_file)

config = args.config if args.config is not None else Config.default()
outputter = OutputFactory.get_outputter(config)
urls = (
    '/bus/(.*)', 'get_bus',
    '/alert/(.*)', 'get_alert',
    '/alerts', 'get_alerts'
)

class SlackApp(web.application):
    def run(self, port=8080, ip='0.0.0.0', *middleware):
        log.info("Starting web application with address http://%r:%r/" % (ip, port))
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (ip, port))

class get_bus:
    def GET(self, route):
        log.info("Received request for bus route %r" % (route))
        payload = transaction_flow(
            TransactionContext.MBTA_BUS(
                config,
                resolve_route(route)
            ),
            config,
            outputter
        )
        log.info("Replying with %r" % (payload))
        return payload
class get_alert:
    def GET(self, route):
        log.info("Received alert request for route %r" % (route))
        payload = transaction_flow(
            TransactionContext.MBTA_ALERT(
                config,
                resolve_route(route)
            ),
            config,
            outputter
        )
        log.info("Replying with %r" % (payload))
        return payload
class get_alerts:
    def GET(self):
        log.info("Received request for alerts")
        payload = transaction_flow(
            TransactionContext.MBTA_ALERTS(
                config
            ),
            config,
            outputter
        )
        log.info("Replying with %r" % (payload))
        return payload

if __name__ == "__main__":
    app = SlackApp(urls, globals())
    app.run()
