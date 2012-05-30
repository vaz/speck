from functools import wraps

from .exception import ExpectationNotMet, NoMatcherError


class MatcherTable(object):
    def __init__(self):
        self.matchers = dict()
        self.aliases = dict()

    def add(self, name, matcher):
        self.matchers[name] = matcher

    def alias(self, original, aliases):
        if hasattr(aliases, 'split'):
            aliases = aliases.split()

        for alias in aliases:
            self.aliases[alias] = original

    def __contains__(self, name):
        if name in self.matchers:
            return True
        if name in self.aliases and self.aliases[name] in self.matchers:
            return True
        return False

    def __getitem__(self, name):
        if name in self.matchers:
            return self.matchers[name]
        if name in self.aliases and self.aliases[name] in self.matchers:
            return self.matchers[self.aliases[name]]
        raise AttributeError, "No matcher found for '%s'" % name


class MatcherRegistry(object):
    def __init__(self):
        self.matchers = MatcherTable()

    def add(self, name, matcher):
        self.matchers.add(name, matcher)

    def alias(self, original, aliases):
        self.matchers.alias(original, aliases)

    def get(self, name, negated=False):
        if negated:
            not_name = 'not_' + name
            if not_name in self.matchers:
                return self.get(not_name)

            def _matcher(a, b):
                matcher = self.get(name)
                try:
                    matcher(a, b)
                except ExpectationNotMet:
                    pass
                else:
                    fmt = matcher.failure_message_fmt
                    raise ExpectationNotMet, 'Negated: ' + fmt.format(a, b)
            _matcher.called_as = not_name
            return _matcher

        if name in self.matchers:
            matcher = self.matchers[name]
            matcher.called_as = name
            return matcher

        raise NoMatcherError, name


matchers = MatcherRegistry()


def matcher(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not f(*args, **kwargs):
            d = kwargs
            d['called_as'] = wrapper.called_as
            raise ExpectationNotMet, (wrapper.failure_message_fmt.format(*args, **d))
    wrapper.called_as = '???'
    wrapper.failure_message_fmt = "{0} {called_as} {1}"
    return wrapper


matchers.add('eq', matcher(lambda a, b: a == b))
matchers.add('ne', matcher(lambda a, b: a != b))
matchers.add('lt', matcher(lambda a, b: a <  b))
matchers.add('gt', matcher(lambda a, b: a >  b))
matchers.add('le', matcher(lambda a, b: a <= b))
matchers.add('ge', matcher(lambda a, b: a >= b))
matchers.add('is', matcher(lambda a, b: a is b))

matchers.alias('eq', '== equal equal_to eq_to')
matchers.alias('ne', '!= not_equal not_equal_to not_eq not_eq_to neq')
matchers.alias('lt', '< less_than not_greater_than_or_equal not_gte not_ge not_greater_than_or_equal_to')
matchers.alias('gt', '> greater_than not_less_than_or_equal not_lte not_le not_less_than_or_equal_to')
matchers.alias('le', '<= less_than_or_equal less_than_or_equal_to lte not_greater_than not_gt')
matchers.alias('ge', '>= greater_than_or_equal greater_than_or_equal_to gte not_less_than')
