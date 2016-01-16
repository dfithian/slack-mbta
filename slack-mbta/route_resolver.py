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

RELEVANT_ROUTE_KEYWORDS=[
    'route',
    'red line',
    'orange line',
    'blue line',
    'green line'
]

def resolve_route(s):
    v = ROUTE_DICTIONARY.get(s.lower(), None)
    return v if v is not None else s
