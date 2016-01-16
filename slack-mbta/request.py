import json
import config
from route_resolver import resolve_route

class Request(object):
    def __init__(self, url, payload):
        self.url = url
        self.payload = payload

class MBTARequest(Request):
    KEY = "UCdH9ujVZUSCBV8GGHh8EQ"
    API_BASE = 'http://realtime.mbta.com/developer/api/v2/'
    BASE_PARAMETERS = dict(format='json', api_key=KEY)
    def __init__(self, endpoint, parameters):
        params = self.BASE_PARAMETERS.copy()
        params.update(parameters)
        serialized_params = '&'.join((k + '=' + v) for k, v in params.iteritems())
        url = self.API_BASE + '{0}?{1}'.format(endpoint, serialized_params)
        super(MBTARequest, self).__init__(url, None)

class MBTARouteRequest(MBTARequest):
    def __init__(self, params):
        route = resolve_route(params.text)
        super(MBTARouteRequest, self).__init__('predictionsbyroute', { 'route' : route })

class MBTAAlertRouteRequest(MBTARequest):
    def __init__(self, params):
        route = resolve_route(params.text)
        super(MBTAAlertRouteRequest, self).__init__('alertheadersbyroute', { 'route' : route })

class MBTAAlertsRequest(MBTARequest):
    def __init__(self, params):
        super(MBTAAlertsRequest, self).__init__('alertheaders', { })

class SlackRequest(Request):
    def __init__(self, params, mbta_context):
        channel = '@%s' % (params.user_name) if params.channel_name == 'directmessage' else '#%s' % (params.channel_name)
        text = '```{0}```'.format('\r\n'.join(str(line) for line in mbta_context.reply()))
        super(SlackRequest, self).__init__(config.config['webhook_url'], { 'payload' : json.dumps({ 'text' : text, 'channel' : channel }) })
