import json
import time
import logging
from operator import add
from const import SECONDS_TO_MINUTES
from route_resolver import RELEVANT_ROUTE_KEYWORDS

log = logging.getLogger(__name__)
class Reply(object):
    def adopt(self, j):
        try:
            self.dictionary = json.loads(j)
        except Exception:
            log.exception('got exception loading invalid json {0}'.format(j))
            self.dictionary = dict()

class MBTARouteReply(Reply):
    def __init__(self):
        self.current_time = time.mktime(time.localtime())
        self.times_by_stop = {}
        self.stops_by_trip = {}
        self.trips_by_direction = {}
        self.directions = []
    def filter_time_for_stop(self, key, eta):
        delta = long(round((long(eta) - self.current_time)/60))
        if delta > 0:
            times = self.times_by_stop.get(key, [])
            self.times_by_stop[key] = times + [delta]
    def format_times(self, key, depth):
        deltas = map(str, sorted(self.times_by_stop.get(key, [])))
        return ['    '*depth + 'at {0}: {1} minutes'.format(key, ', '.join(deltas))]

    def filter_stops_for_trip(self, key, stops):
        for stop in stops:
            stop_name = stop['stop_name']
            stop_sequence = int(stop['stop_sequence'])
            self.filter_time_for_stop(stop_name, stop['sch_arr_dt'])
            other_stops = self.stops_by_trip.get(key, [])
            if len(filter(lambda stop: stop[0] == stop_name, other_stops)) == 0:
                self.stops_by_trip[key] = other_stops + [(stop_name, stop_sequence)]
    def format_stops(self, key, depth):
        stops = sorted(self.stops_by_trip.get(key, []), key=lambda stop: stop[1])
        f = lambda (stop, _): self.format_times(stop, depth)
        return reduce(add, map(f, stops), [])

    def filter_trips_for_direction(self, key, trips):
        for trip in trips:
            trip_name = trip['trip_headsign']
            stops = trip['stop']
            self.filter_stops_for_trip(trip_name, stops)
            other_trips = self.trips_by_direction.get(key, [])
            if trip_name not in other_trips:
                self.trips_by_direction[key] = other_trips + [trip_name]
    def format_trips(self, key, depth):
        trips = self.trips_by_direction.get(key, [])
        f = lambda trip: ['    '*depth + 'to {0}'.format(trip)] + self.format_stops(trip, depth + 1)
        return reduce(add, map(f, trips), [])

    def filter_directions(self, directions):
        for direction in directions:
            direction_name = direction['direction_name']
            trips = direction['trip']
            self.filter_trips_for_direction(direction_name, trips)
            if direction_name not in self.directions:
                self.directions.append(direction_name)
    def format_directions(self, depth):
        directions = self.directions
        f = lambda dir: ['    '*depth + '{0}'.format(dir)] + self.format_trips(dir, depth + 1)
        return reduce(add, map(f, directions), [])

    def __call__(self):
        try:
            self.filter_directions(self.dictionary['direction'])
            return self.format_directions(0)
        except Exception:
            log.exception('failed to filter relevant response information')
            return ['an error occurred']

class SlackReply(Reply):
    def __call__(self):
        log.debug('SlackReply object with dictionary {0} invoked'.format(json.dumps(self.dictionary)))
    def adopt(self, j):
        self.dictionary = dict(response_message=j)
