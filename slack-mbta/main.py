import os
import sys
import argparse
import logging
import time
import threading
import web
from output import OutputFactory, Output
from config import ConfigAction, Config
from route_resolver import resolve_route
from rest_api_thread import RestAPIThread
from slack_messaging_thread import SlackMessagingThread

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
    log.info("Logger started with options is_debug={0}, log_file={1}".format(str(is_debug), log_file))
    log.info("Slack-MBTA version {0}".format(VERSION))
    return log

parser = argparse.ArgumentParser(description="Get MBTA info", epilog="(c) 2015 Dan Fithian")

parser.add_argument("-l", dest="log_file", help="Specify a log file", default=None)
parser.add_argument("-p", dest="port", type=int, help="Specify a port to listen on", default="8080")
parser.add_argument("-ip", dest="ip", type=str, help="Specify an IP to bind", default="0.0.0.0")
parser.add_argument("-c", dest="config", type=str, help="Provide a config file", const=None, action=ConfigAction)
parser.add_argument("-d", dest="debug", action="store_true", help="Enable debug logging")

# parse the config and set up inputs
opts = parser.parse_args(sys.argv[1:])

# start logging
log = start_logging(opts.debug, opts.log_file)

Config.this = opts.config if opts.config is not None else Config.default()

class Main(object):
    def __init__(self, opts):
        self.slack_messaging_thread = SlackMessagingThread()
        self.rest_api_thread = RestAPIThread(opts)
    def __call__(self):
        self.slack_messaging_thread.start()
        self.rest_api_thread.start()

main = Main(opts)
main()
