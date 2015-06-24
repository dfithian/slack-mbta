import argparse
import sys
import json
from output import OutputType

"""Configuration module"""
MAX_BUS_LINES_DEFAULT = 3
MAX_ALERTS_DEFAULT = 3
OUTPUT_DEFAULT = OutputType.CONSOLE

class Config(object):
    def __init__(self, dictionary):
        if dictionary is None:
            print 'Configuration dictionary was None.'
            sys.exit(1)
        self.max_bus_lines = getattr(dictionary, "max_bus_lines", MAX_BUS_LINES_DEFAULT)
        self.max_alerts = getattr(dictionary, "max_alerts", MAX_ALERTS_DEFAULT)
        self.output_type = getattr(dictionary, "output", OUTPUT_DEFAULT)
        self.output_filename = getattr(dictionary, "output_filename", None)
    @staticmethod
    def default():
        default_dict = {
            "max_bus_lines" : MAX_BUS_LINES_DEFAULT,
            "max_alerts" : MAX_ALERTS_DEFAULT,
            "output_type" : OUTPUT_DEFAULT,
            "output_filename" : None
        }
        return Config(default_dict)

class ConfigAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        print 'ConfigAction __init__() called'
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
        print 'ConfigAction __call__() called'
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
