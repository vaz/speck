import functools

from .exception import ExpectationNotMet, NoMatcherError
from .util import words, callable


class MatcherRegistry(object):
    def __init__(self):
        self.matchers = dict()

    def add(self, matcher, names):
        names = words(names)
        for name in names:
            self.matchers[name] = matcher

    def remove(self, names, include_aliases=False):
        names = words(names)
        for name in names:
            self.remove_one(name, include_aliases)

    def remove_one(self, name, include_aliases=False):
        f = self.matchers.pop(name)
        if include_aliases:
            for n, m in self.matchers:
                if m == f:
                    self.remove_one(n)

    def alias(self, original, aliases):
        self.matchers.alias(original, aliases)

    def __len__(self):
        return len(self.matchers)

    def __iter__(self):
        return iter(self.matchers)

    def __contains__(self, name):
        return name in self.matchers

    def get(self, name):
        return self.matchers.get(name).clone(name)

    def __getitem__(self, name):
        # don't try/except because we want a cleaner traceback
        if name in self.matchers:
            return self.matchers[name].clone(name)
        raise NoMatcherError(name)


matchers = MatcherRegistry()


class Matcher(object):
    def __init__(self, callable, name=None):
        self.wrapped = callable
        functools.wraps(callable)(self)

        if name is None:
            name = callable.__name__

        self.__name__ = name

    def clone(self, name):
        return Matcher(self.wrapped, name=name)

    def __call__(self, expr, *args, **kwargs):
        result = MatcherResult(self, expr, *args, **kwargs)
        result.raise_if_failed()
        return result

    def __str__(self):
        return self.__name__.replace("_", " ")


class MatcherResult(object):
    def __init__(self, matcher, expr, *args, **kwargs):
        self.negated = expr.is_negated
        self.noop = expr.is_noop
        self.matcher = matcher
        self.expr = expr
        self.args = args
        self.kwargs = kwargs
        self.passed = self.negated ^ self.matcher.wrapped(expr.value, *args, **kwargs)

    def __str__(self):
        opts = ""
        if self.kwargs:
            opts = "({})".format("{k}={v}".format(k=k, v=v)
                                 for k, v in self.kwargs)
        return "{} {} {}{}".format(self.expr, self.matcher, self.args[0], opts)

    def raise_if_failed(self):
        if not (self.passed or self.noop):
            raise ExpectationNotMet(self)


def matcher(callable_or_names, names=None):
    """
    Implicitly registers it with function's __name__, "be_a_dog":

    @matcher
    def be_a_dog(x):
        return type(x) == dog

    Explicitly registers it with names "be_a_dog" and "be_canine"

    @matcher("be_a_dog, be_canine")
    def whatever(x):
        return type(x) == dog

    matcher(f, "be_a_dog be_canine")

    """
    if callable(callable_or_names):
        # called directly as a decorator
        if 'lambda' in callable_or_names.__name__ and names:
            callable_or_names.__name__ = words(names)[0]
        matchers.add(Matcher(callable_or_names), names)

    else:
        # called as a decorator factory
        decorator = functools.partial(matcher, names=callable_or_names)
        functools.wraps(matcher)(decorator)
        return decorator


matcher(lambda a, b: a == b, '== equal equal_to')
matcher(lambda a, b: a != b, '!= not_equal not_equal_to')
matcher(lambda a, b: a <  b, '< less_than not_greater_than_or_equal not_greater_than_or_equal_to')
matcher(lambda a, b: a >  b, '> greater_than not_less_than_or_equal not_less_than_or_equal_to')
matcher(lambda a, b: a <= b, '<= less_than_or_equal less_than_or_equal_to not_greater_than')
matcher(lambda a, b: a >= b, '>= greater_than_or_equal greater_than_or_equal_to not_less_than')
matcher(lambda a, b: a is b, 'be is be_identical be_identical_to')
matcher(lambda inst, cls: isinstance(inst, cls), 'be_a be_an be_an_instance_of be_instance_of')
matcher(lambda inst, cls: issubclass(inst, cls), 'be_kind_of be_a_kind_of be_subclass_of be_a_subclass_of')
