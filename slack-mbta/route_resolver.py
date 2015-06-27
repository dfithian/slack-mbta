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

def resolve_route(s):
    v = getattr(ROUTE_DICTIONARY, s, None)
    return v if v is not None else s
