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

class MBTABusRequest(MBTARequest):
    def __init__(self, route):
        self.route = route
        super(MBTABusRequest, self).__init__('predictionsbyroute', { 'route' : route })
    def __str__(self):
        return "*/bus {0}*".format(str(self.route))

class MBTAAlertRouteRequest(MBTARequest):
    def __init__(self, route):
        self.route = route
        super(MBTAAlertRouteRequest, self).__init__('alertheadersbyroute', { 'route' : route })
    def __str__(self):
        return "*/alert {0}*".format(str(self.route))

class MBTAAlertsRequest(MBTARequest):
    def __init__(self):
        super(MBTAAlertsRequest, self).__init__('alertheaders', { })
    def __str__(self):
        return ("*/alerts*")

class SlackRequest(Request):
    WEBHOOK_URL = 'https://hooks.slack.com/services/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'
    def __init__(self, payload):
        super(SlackRequest, self).__init__(self.WEBHOOK_URL, payload)
