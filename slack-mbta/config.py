import enum
import argparse
import sys
import json
import logging

"""Configuration module"""
log = logging.getLogger(__name__)
class OutputType(enum.Enum):
    SLACK = "slack"
    FILE = "file"

MAX_BUS_LINES_DEFAULT = 3
MAX_ALERTS_DEFAULT = 3
OUTPUT_DEFAULT = OutputType.SLACK

class Config(object):
    def __init__(self, dictionary):
        if dictionary is None:
            log.error('Configuration dictionary was None. Exiting.')
            sys.exit(1)
        self.max_bus_lines = dictionary.get('max_bus_lines', MAX_BUS_LINES_DEFAULT)
        self.max_alerts = dictionary.get('max_alerts', MAX_ALERTS_DEFAULT)
        self.output_type = dictionary.get('output', OUTPUT_DEFAULT)
        self.output_filename = dictionary.get('output_filename', '/Users/dan/dev/slack-mbta/output.txt')
    @staticmethod
    def default():
        default_dict = {
            "max_bus_lines" : MAX_BUS_LINES_DEFAULT,
            "max_alerts" : MAX_ALERTS_DEFAULT,
            "output_type" : OUTPUT_DEFAULT,
            "output_filename" : '/Users/dan/dev/slack-mbta/output.txt'
        }
        return Config(default_dict)

class ConfigAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
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
        if values and values[0]:
            try:
                f = open(values[0], 'r')
                self.config = json.loads(f.read())
            except IOError:
                log.exception("Oops, IOError!")
        if self.config is None:
            log.info('Config is None. Loading default.')
            self.config = Config.default()
        setattr(namespace, self.dest, self.config)
