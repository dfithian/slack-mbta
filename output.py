import enum
import abc

"""Formats output depending on environment (console or slack)"""

class OutputType(enum.Enum):
    CONSOLE = "console"
    SLACK = "slack"
    FILE = "file"

class OutputFactory(object):
    @staticmethod
    def get_outputter(config):
        if config.output_type is OutputType.CONSOLE:
            return ConsoleOutputter(config)
        elif config.output_type is OutputType.SLACK:
            return SlackOutputter(config)
        elif config.output_type is OutputType.FILE:
            return FileOutputter(config)
        else:
            print('output_type was type %r but was expecting one of OutputType' % (type(config.output_type)))

class Output(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, config):
        self.config = config
    @abc.abstractmethod
    def __call__(reply):
        """Output some reply from the server to an appropriate format"""
        return

class ConsoleOutputter(Output):
    def __call__(self, reply):
        print '\n'.join(str(line) for line in reply())

class SlackOutputter(Output):
    def __call__(self, reply):
        print '```' + '\n'.join(str(line) for line in reply()) + '```'

class FileOutputter(Output):
    def __call__(self, reply):
        f = open(self.config.output_filename, 'w')
        f.write('\n'.join(str(line) for line in reply()))
        f.close()
