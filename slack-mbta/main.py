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
from web.wsgiserver import CherryPyWSGIServer

VERSION='1.0'
base_dir = os.path.dirname(os.path.realpath(__file__))
def start_logging(is_debug, log_file=None):
    base_options = dict(
        level=(logging.DEBUG if is_debug else logging.INFO),
        format='%(asctime)s %(levelname)s - %(message)s'
    )
    options = base_options if log_file is None else dict(dict(filename=log_file), **base_options)
    logging.basicConfig(**options)
    log = logging.getLogger(__name__)
    log.info("Logger started with options is_debug=%r, log_file=%r" % (str(is_debug), log_file))
    log.info("Slack-MBTA version %r" % (VERSION))
    return log

def transaction_flow(txn_context, config, outputter):
    txn_context.do_transaction()
    return outputter(txn_context.request, txn_context.reply)

parser = argparse.ArgumentParser(description="Get MBTA info", epilog="(c) 2015 Dan Fithian")

parser.add_argument("-l", dest="log_file", help="Specify a log file", default=None)
parser.add_argument("-p", dest="port", type=int, help="Specify a port to listen on", default="8080")
parser.add_argument("-ip", dest="ip", type=str, help="Specify an IP to bind", default="0.0.0.0")
parser.add_argument("-c", dest="config", type=str, help="Provide a config file", const=None, action=ConfigAction)
parser.add_argument("-d", dest="debug", action="store_true", help="Enable debug logging")

# parse the config and set up inputs
args = parser.parse_args(sys.argv[1:])

# start logging
log = start_logging(args.debug, args.log_file)

config = args.config if args.config is not None else Config.default()
outputter = OutputFactory.get_outputter(config)
urls = (
    '/bus', 'get_bus',
    '/alert', 'get_alert',
    '/alerts', 'get_alerts'
)

class SlackApp(web.application):
    def run(self, *middleware):
        log.info("Starting web application with address {0}:{1}".format(args.ip, args.port))
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, server_address=(args.ip, args.port))

class get_bus:
    def GET(self):
        route = web.input().text
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
    def GET(self):
        route = web.input().text
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

CherryPyWSGIServer.ssl_certificate = base_dir + '/../cert/server.crt'
CherryPyWSGIServer.ssl_private_key = base_dir + '/../cert/server.key'
if __name__ == "__main__":
    app = SlackApp(urls, globals())
    app.run()
