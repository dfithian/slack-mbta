"""Resolver for route_id based on bus or subway line"""

ROUTE_DICTIONARY={
    'red':'Red',
    'b':'Green-B',
    'c':'Green-C',
    'd':'Green-D',
    'e':'Green-E',
    'orange':'Orange',
    'blue':'Blue'
}

# List of stop_ids that we care about
ROUTE_RELEVANT_STOPS={
    '59':['8171','8186'],
    '57':['900'],
    '71':['8178'],
    '70':['8297']
}

RELEVANT_ROUTE_KEYWORDS=[
    'route 57',
    'route 59',
    'route 70',
    'route 71',
    'red line',
    'orange line',
    'blue line',
    'green line'
]

def resolve_route(s):
    v = ROUTE_DICTIONARY.get(s.lower(), None)
    return v if v is not None else s
