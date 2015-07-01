import abc
import json
import time
import logging
from route_resolver import ROUTE_RELEVANT_STOPS, RELEVANT_ROUTE_KEYWORDS

"""Represents a reply object from the server"""
log = logging.getLogger(__name__)
class Reply(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, config):
        self.config = config
    @abc.abstractmethod
    def __call__(self):
        """Return information from server in a human-readable format"""

class MBTAReply(Reply):
    def adopt(self, j):
        try:
            self.dictionary = json.loads(j)
        except Exception:
            log.exception('Got exception loading invalid json %r' % (j))
            self.dictionary = dict()

class MBTABusReply(MBTAReply):
    def filter_route(self, stops, route):
        relevant_stops = ROUTE_RELEVANT_STOPS.get(str(route), [])
        stop_summaries = []
        if stops is not None and len(stops) > 0:
            for stop in stops:
                if stop.get('stop_id', None) in relevant_stops:
                    delta = long(round((long(stop["sch_arr_dt"]) - time.mktime(time.localtime()))/60))
                    stop_summaries.append("    %r in %r minutes" % (str(stop["stop_name"]), str(delta)))
        return stop_summaries
    def filter_trip(self, trips, route):
        trip_summaries = []
        if trips is not None and len(trips) > 0:
            for trip in trips:
                stop_summaries = self.filter_route(trip.get('stop', None), route)
                if len(stop_summaries) > 0:
                    trip_summaries.extend(["Trip %r" % str(trip.get('trip_headsign', None))] + stop_summaries)
        return trip_summaries
    def filter_direction(self, directions, route):
        direction_summaries = []
        if directions is not None and len(directions) > 0:
            for direction in directions:
                trip_summary = self.filter_trip(direction.get('trip', None), route)
                if len(trip_summary) > 0:
                    direction_summaries.extend([("Direction: %r" % str(direction["direction_name"]))] + trip_summary)
        else:
            direction_summaries = ['No predictions']
        return direction_summaries
    def __call__(self):
        return self.filter_direction(self.dictionary.get('direction', None), self.dictionary.get('route_id'))

class MBTAAlertsReply(MBTAReply):
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
