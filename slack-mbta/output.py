import abc
import json
import datetime
import logging
from config import OutputType

"""Formats output depending on environment (console or slack)"""
log = logging.getLogger(__name__)
class OutputFactory(object):
    outputters = {}
    @staticmethod
    def get_outputter(config):
        outputter = OutputFactory.outputters.get(config.output_type, None)
        if outputter is None:
            if config.output_type is OutputType.SLACK:
                outputter = SlackOutputter(config)
            elif config.output_type is OutputType.FILE:
                outputter = FileOutputter(config)
            else:
                log.error('output_type was type {0} but was expecting one of OutputType'.format(type(config.output_type)))
                sys.exit(1)
        OutputFactory.outputters[config.output_type] = outputter
        return outputter

class Output(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, config):
        self.config = config
    @abc.abstractmethod
    def format(reply):
        """Output some reply from the server to an appropriate format"""
        return

class SlackOutputter(Output):
    def format(self, request, reply):
        request_info = "Request {0} response:\r\n".format(str(request))
        reply_info = '```{0}```'.format('\r\n'.join(str(line) for line in reply()))
        text = request_info + reply_info
        return { 'payload' : json.dumps({ 'text' : request_info + reply_info }) }

class FileOutputter(Output):
    def format_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    def format(self, reply):
        if self.config.output_filename is not None:
            t = self.format_datetime()
            f = open(self.config.output_filename, 'a')
            f.write('\n'.join(t + str(line) for line in reply()))
            f.write('\n') # end with newline
            f.close()
        else:
            log.warn('Got instructions to output to file, but output_filename was None!')
