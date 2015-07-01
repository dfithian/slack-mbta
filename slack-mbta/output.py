import abc
import datetime
import logging
from config import OutputType

"""Formats output depending on environment (console or slack)"""
log = logging.getLogger(__name__)
class OutputFactory(object):
    @staticmethod
    def get_outputter(config):
        if config.output_type is OutputType.SLACK:
            return SlackOutputter(config)
        elif config.output_type is OutputType.FILE:
            return FileOutputter(config)
        else:
            log.error('output_type was type %r but was expecting one of OutputType' % (type(config.output_type)))

class Output(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, config):
        self.config = config
    @abc.abstractmethod
    def __call__(reply):
        """Output some reply from the server to an appropriate format"""
        return

class SlackOutputter(Output):
    def __call__(self, request, reply):
        request_info = ("Request %r response:\r\n" % str(request))
        reply_info = '```{0}```'.format('\r\n'.join(str(line) for line in reply()))
        return (request_info + reply_info)

class FileOutputter(Output):
    def format_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    def __call__(self, reply):
        if self.config.output_filename is not None:
            t = self.format_datetime()
            f = open(self.config.output_filename, 'a')
            f.write('\n'.join(t + str(line) for line in reply()))
            f.write('\n') # end with newline
            f.close()
        else:
            log.warn('Got instructions to output to file, but output_filename was None!')
