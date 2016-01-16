import json

class SlackOutputter(object):
    def format(self, request, reply):
        request_info = "{0}:\r\n".format(str(request))
        reply_info = '```{0}```'.format('\r\n'.join(str(line) for line in reply()))
        text = request_info + reply_info
        return { 'payload' : json.dumps({ 'text' : request_info + reply_info }) }
