import sys
import argparse
import json

class Config(object):
    def __init__(self, dictionary):
        if dictionary is None:
            print 'Configuration dictionary was None.'
            sys.exit(1)
        self.max_bus_lines = getattr(dictionary, "max_bus_lines", 3)
        self.max_alerts = getattr(dictionary, "max_alerts", 3)
    @staticmethod
    def default():
        default_dict = {
            "max_bus_lines" : 3,
            "max_alerts" : 3
        }
        return Config(default_dict)

class ConfigAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        print 'ConfigAction initialized.'
        self.dest = dest
        self.type = str
        self.metavar = None
        self.choices = None
        self.nargs = 1 if nargs is None else nargs
        self.option_strings = option_strings
        self.default = None
        self.help = kwargs["help"]
        self.required = False
        self.const = kwargs["const"]
        self.config = None
    def __call__(self, parser, namespace, values, option_string):
        print 'ConfigAction called.' # construct and return a config object here
        if values and values[0]:
            try:
                f = open(values[0], 'r')
                self.config = json.loads(f.read())
            except IOError:
                print "Oops, IOError!"
        if self.config is None:
            print 'Config is None. Loading default.'
            self.config = Config.default()
        setattr(namespace, self.dest, self.config)

parser = argparse.ArgumentParser(description="Get MBTA info", epilog="(c) 2015 Dan Fithian")

parser.add_argument("alert", action="store_true", help="Get recent MBTA alerts")
parser.add_argument("bus", nargs=1, type=int, help="Get information about a bus line") #FIXME switch to nargs='?' and default is show all
parser.add_argument("-v", action="version", version="1.0", help="Get version information")
parser.add_argument("-c", dest="config", nargs='?', type=str, help="Provide a config file", const=None, action=ConfigAction)

args = parser.parse_args(sys.argv[1:])
config = args.config
bus = args.bus
alert = args.alert

if alert is not None:
    print 'Alert is not None.'
if bus is not None:
    print 'Bus is not None.'
