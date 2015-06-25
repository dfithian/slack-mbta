#!/usr/bin/env python

import sys
import argparse
import web
import json
from config import ConfigAction, Config
from transaction import TransactionContext
from output import OutputFactory

def transaction_flow(txn_context, config, outputter):
    mbta_reply = txn_context.do_transaction()
    return json.dumps(outputter(mbta_reply))
    # slack_payload = outputter(mbta_reply)
    # txn_context = TransactionContext.SLACK(config, slack_payload)
    # slack_reply = txn_context.do_transaction()

parser = argparse.ArgumentParser(description="Get MBTA info", epilog="(c) 2015 Dan Fithian")

# parser.add_argument("-a", dest="alert", action="store_true", help="Get recent MBTA alerts")
# parser.add_argument("-b", dest="bus", help="Get information about a bus line") #FIXME switch to nargs='?' and default is show all
parser.add_argument("-v", action="version", version="Version 1.0", help="Get version information")
parser.add_argument("-c", dest="config", type=str, help="Provide a config file", const=None, action=ConfigAction)

# parse the config and set up inputs
args = parser.parse_args(sys.argv[1:])
config = args.config if args.config is not None else Config.default()
# bus = args.bus
# alert = args.alert
outputter = OutputFactory.get_outputter(config)
# if alert:
#     transaction_flow(TransactionContext.MBTA_ALERT(config), config, outputter)
# if bus is not None:
#     transaction_flow(TransactionContext.MBTA_BUS(config, bus), config, outputter)
urls = (
    '/bus/(.*)', 'get_bus',
    '/alerts', 'get_alerts'
)
app = web.application(urls, globals())

class get_bus:
    def GET(self, bus):
        payload = transaction_flow(TransactionContext.MBTA_BUS(config, bus), config, outputter)
        return payload
class get_alerts:
    def GET(self):
        payload = transaction_flow(TransactionContext.MBTA_ALERT(config), config, outputter)
        return payload

if __name__ == "__main__":
    app.run()
