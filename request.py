class Request(object):
    KEY = "UCdH9ujVZUSCBV8GGHh8EQ"
    API_BASE = 'http://realtime.mbta.com/developer/api/v2/'
    BASE_PARAMETERS = { 'format' : 'json' }
    def __init__(self, endpoint, parameters):
        self.endpoint = endpoint
        self.parameters = self.BASE_PARAMETERS.copy()
        self.parameters.update(parameters)
    def __call__(self):
        return (self.API_BASE + '{0}?api_key={1}&{2}').format(self.endpoint, self.KEY, self.serialize_parameters())
    def serialize_parameters(self):
        return '&'.join((k + '=' + v) for k, v in self.parameters.iteritems())

class BusRequest(Request):
    def __init__(self, stop):
        super(BusRequest, self).__init__('predictionsbystop', { 'stop' : stop })

class AlertRequest(Request):
    def __init__(self):
        super(AlertRequest, self).__init__('alerts', { })
