import re

class Match(object):
    def __init__(self, pattern, retVal):
        self.pattern = pattern
        self.retVal = retVal

class KeywordMatch(Match):
    def __init__(self, pattern, retVal):
        super(KeywordMatch, self).__init__(pattern, retVal)
    def matches(self, word):
        return self.pattern == word

class RegexMatch(Match):
    def __init__(self, pattern, retVal):
        super(RegexMatch, self).__init__(re.compile(pattern), retVal)
    def matches(self, word):
        return self.pattern.search(word) is not None

ROUTES={
    KeywordMatch('red', 'Red'),
    KeywordMatch('b', 'Green-B'),
    KeywordMatch('c', 'Green-C'),
    KeywordMatch('d', 'Green-D'),
    KeywordMatch('e', 'Green-E'),
    KeywordMatch('orange', 'Orange'),
    KeywordMatch('blue', 'Blue'),
    KeywordMatch('mattapan', 'Mattapan'),
    RegexMatch('^(.*)fairmount(.*)$', 'CR-Fairmount'),
    RegexMatch('^(.*)fitchburg(.*)$', 'CR-Fitchburg'),
    RegexMatch('^(.*)worcester(.*)$', 'CR-Worcester'),
    RegexMatch('^(.*)franklin(.*)$', 'CR-Franklin'),
    RegexMatch('^(.*)greenbush(.*)$', 'CR-Greenbush'),
    RegexMatch('^(.*)haverhill(.*)$', 'CR-Haverhill'),
    RegexMatch('^(.*)lowell(.*)$', 'CR-Lowell'),
    RegexMatch('^(.*)needham(.*)$', 'CR-Needham'),
    RegexMatch('^(.*)newburyport(.*)$', 'CR-Newburyport'),
    RegexMatch('^(.*)providence(.*)$', 'CR-Providence'),
    RegexMatch('^(.*)kingston(.*)$', 'CR-Kingston'),
    RegexMatch('^(.*)middleborough(.*)$', 'CR-Middleborough'),
    RegexMatch('^(.*)hingham ferry(.*)$', 'Boat-F1'),
    RegexMatch('^(.*)hull ferry(.*)$', 'Boat-F3'),
    RegexMatch('^(.*)charlestown ferry(.*)$', 'Boat-F4')
}

RELEVANT_ROUTE_KEYWORDS=[
    'route',
    'red line',
    'orange line',
    'blue line',
    'green line'
]

def resolve_route(s):
    for match in ROUTES:
        if match.matches(s.lower()):
            return match.retVal
    return s
