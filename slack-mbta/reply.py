import abc
import json
import time
import logging
from route_resolver import ROUTE_RELEVANT_STOPS, RELEVANT_ROUTE_KEYWORDS

log = logging.getLogger(__name__)
class Reply(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, config):
        self.config = config
    @abc.abstractmethod
    def __call__(self):
        """Return information from server in a human-readable format"""
    def adopt(self, j):
        try:
            self.dictionary = json.loads(j)
        except Exception:
            log.exception('Got exception loading invalid json {0}'.format(j))
            self.dictionary = dict()

class MBTARouteReply(Reply):
    def filter_route(self, stops, route):
        relevant_stops = ROUTE_RELEVANT_STOPS.get(str(route), [])
        stop_summaries = []
        if stops is not None and len(stops) > 0:
            for stop in stops:
                if stop.get('stop_id', None) in relevant_stops:
                    delta = long(round((long(stop["sch_arr_dt"]) - time.mktime(time.localtime()))/60))
                    stop_name = str(stop.get('stop_name', 'none'))
                    stop_summaries.append("        at {0} in {1} minutes".format(stop_name, str(delta)))
        return stop_summaries
    def filter_trip(self, trips, route):
        trip_summaries = {}
        if trips is not None and len(trips) > 0:
            for trip in trips:
                stop_summaries = self.filter_route(trip.get('stop', None), route)
                if len(stop_summaries) > 0:
                    trip_headsign = str(trip.get('trip_headsign', 'none'))
                    similar_trips = trip_summaries.get(trip_headsign, None)
                    if similar_trips is not None:
                        trip_summaries[trip_headsign].extend(stop_summaries)
                    else:
                        trip_summaries[trip_headsign] = ["    Trip {0}".format(trip_headsign)] + stop_summaries
        return reduce(lambda x,y: x.extend(y), trip_summaries.values()) if len(trip_summaries.values()) > 0 else []
    def filter_direction(self, directions, route):
        direction_summaries = []
        if directions is not None and len(directions) > 0:
            for direction in directions:
                trip_summary = self.filter_trip(direction.get('trip', None), route)
                if trip_summary is not None and len(trip_summary) > 0:
                    direction_summaries.extend(["Direction: {0}".format(str(direction["direction_name"]))] + trip_summary)
        if len(direction_summaries) == 0:
            direction_summaries = ['No predictions']
        return direction_summaries
    def __call__(self):
        try:
            return self.filter_direction(self.dictionary.get('direction', None), self.dictionary.get('route_id'))
        except Exception:
            log.exception('Failed to filter relevant response informaton')
            return ['An error occurred']

class MBTAAlertsReply(Reply):
    def __call__(self):
        headers = self.dictionary.get('alert_headers', None)
        relevant_headers = []
        if headers is not None and len(headers) > 0:
            for header in headers:
                if any(keyword in header.get('header_text', '').lower() for keyword in RELEVANT_ROUTE_KEYWORDS):
                    relevant_headers.append(header["header_text"])
                else:
                    log.debug(header.get('header_text') + ' didnt match anything in RELEVANT_ROUTE_KEYWORDS')
        return (relevant_headers if len(relevant_headers) > 0 else ['No alerts'])

class SlackReply(Reply):
    def __call__(self):
        log.debug('SlackReply object with dictionary {0} invoked'.format(json.dumps(self.dictionary)))
    def adopt(self, j):
        self.dictionary = dict(response_message=j)
