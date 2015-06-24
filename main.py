import sys
import argparse
from config import ConfigAction, Config
from transaction import TransactionContext
from output import OutputFactory

parser = argparse.ArgumentParser(description="Get MBTA info", epilog="(c) 2015 Dan Fithian")

parser.add_argument("-a", dest="alert", action="store_true", help="Get recent MBTA alerts")
parser.add_argument("-b", dest="bus", help="Get information about a bus line") #FIXME switch to nargs='?' and default is show all
parser.add_argument("-v", action="version", version="1.0", help="Get version information")
parser.add_argument("-c", dest="config", type=str, help="Provide a config file", const=None, action=ConfigAction)

# parse the config and set up inputs
args = parser.parse_args(sys.argv[1:])
config = args.config if args.config is not None else Config.default()
bus = args.bus
alert = args.alert
outputter = OutputFactory.get_outputter(config)

transaction_context = TransactionContext.BUS(config, bus) if bus is not None else TransactionContext.ALERT(config)
reply = transaction_context.do_transaction() # do the transaction and adopt the output
outputter(reply) # output the reply all nice like
