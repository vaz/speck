import functools

from .util import callable
from .matcher import matchers

#from .matcher import matchers  #, start_with, end_with


# "shouldnt" because should.not.be is a syntax error
# "not" negates the expectation
# "eventually" or "later" or "maybe" makes matchers not raise (or catches exceptions)
# "be" as a terminal element calls the is-ness matcher
# "be" anywhere else does nothing
# "have" changes matchers to return another smart object
#     ...have(3).whatevers
#     ...have.less_than(10).things
#     ...have(3).more.things.than(lst)
# "all" or "each" calls the matcher on each element
# "never" - any use?

# _(x).should == 4
# _(x).should_not == 4
# _(x).shouldnt == 4
# _(x).should.be(4)
# _(x).should.not_be(4)
# _(x).shouldnt.be(4)
# _(x).shouldnt.be < 4
# _(x).shouldnt.be == 4
# _(x).should.be_an(int)
# _(x).should.be_a_kind_of(object)
# _(x).should.have(3)
# _(x).should.have(3).things
# _(x).should.have.less_than(3).things
# (_(x).should.have < 3).things # yucky but probably possible
# _(x).should.have.no.things
# _(x).should.have.a.name
# _(x).should.have.an.age
# _(x).should.have(3).more.things.than(you)
# _(x).should.have(3).things.less_than(you)
# _(x).should.have(3).or_more.things
# _(x).shoud.have.at.least(3).things



# total other direction: test doubles using "will" ?

# _() ideas
# if first arg is a callable, rest is args
# otherwise if more than one arg, treat as list

# matcher ideas
# "fail" - raise a StandardError
# "warn" - raise a Warning
# "use_deprecated_code" - raise DeprecationWarning or PendingDeprecationWarning
# take_longer_than - left operand is a callable, right is some time
# "return" -lvalue is callable, right is expected return


class Expectation(object):
    """
    Expectation base class.

    This class is abstract by convention.  It handles most of the
    really dynamic stuff about expectations and the chaining
    of fragments.
    """
    _precedes = ["not_", "eventually"]

    def __init__(self, prev, name=None, negated=False):
        if name is None:
            name = type(self).__name__.lower()

        self.prev = prev
        self.name = name
        self._noop = False
        self._negated = negated

    def __repr__(self):
        return repr(self.prev) + " " + self.name

    def __getattr__(self, name):
        attr = self._eat_prefixes(name)

        if attr is self:
            return self.matcher(name)
        else:
            return attr

    def _eat_prefixes(self, name):
        for fragment in self._precedes:
            prefix = fragment

            if not fragment.endswith("_"):
                prefix += "_"

            if name.startswith(prefix):
                return getattr(getattr(self, fragment), name[len(prefix):])

        return self

    @property
    def is_negated(self):
        return self._negated ^ self.prev.is_negated

    @property
    def is_noop(self):
        return self._noop or self.prev.is_noop

    @property
    def value(self):
        return self.prev.value

    @property
    def not_(self):
        return Not(self)

    def _negate(self):
        self._negated = not self._negated
        return self

    def matcher(self, name):
        return functools.partial(matchers[name], self)


class _(Expectation):
    """
    The first segment in the main expectation clause: the tested
    (wrapped) value.

    This fragment is to be followed by a Should-style fragment.
    """
    _precedes = ["should", "shouldnt"]

    def __init__(self, value, *args, **kwargs):
        """
        3 cases:
        _(value)
        _(callable, arg1, arg2, k=v, k2=v2)
        _(some, list, of, things)
        """
        if callable(value):
            #self._args = args
            #self._kwargs = kwargs
            raise NotImplementedError("_(callable)")

        elif args:
            value = [value] + args

        self._value = value

        super().__init__(None)


    def __getattr__(self, name):
        attr = self._eat_prefixes(name)

        if attr is self:
            raise AttributeError("Expected 'should', etc., not a matcher.")
        else:
            return attr

    def __repr__(self):
        return str(self.value)

    @property
    def is_negated(self):
        return False

    @property
    def is_noop(self):
        return False

    @property
    def value(self):
        return self._value

    @property
    def should(self):
        return Should(self)

    @property
    def should_not(self):
        return Not(Should(self))

    @property
    def shouldnt(self):
        return Should(self, "shouldn't")._negate()


class Should(Expectation):
    """
    Should and subclasses are non-terminal expectation fragments.

    Other Expectation subclasses (not deriving from Should) are
    generally terminal segments that will call a matcher, or a
    transitional fragment like "have" that leads to a secondary
    clause.  Should fragments can lead into other Should subclasses
    which modify the expectation in various ways (negation, no-op,
    etc), or they can lead into a terminal (e.g. "be") or
    transitional (e.g. "have") fragment.
    """
    _precedes = Expectation._precedes + ['be']

    @property
    def be(self):
        return Be(self)

    @property
    def eventually(self):
        return Eventually(self)

    @property
    def maybe(self):
        return Maybe(self)

    __eq__  = lambda self, other: self.matcher('==')(other)
    __ne__  = lambda self, other: self.matcher('!=')(other)


class Not(Should):
    """
    A Not fragment behaves like a Should, except that it
    negates the expectation.  Multiple Nots in the same
    expectation will alternate negativity as you would expect.
    """
    def __init__(self, prev, name=None):
        super().__init__(prev, name=name)
        self._negated = True


class Eventually(Should):
    """
    An Eventually fragment behaves like a Should, except that
    it makes the entire expectation as a no-op.
    """
    def __init__(self, prev, name=None):
        super().__init__(prev, name=name)
        self._noop = True


class Maybe(Eventually):
    """
    A Maybe fragment behaves exactly like an Eventually fragment,
    marking the expectation as a no-op, though the output is
    different and its use is semantically different.
    """


class Be(Expectation):
    """
    A Be fragment is a terminal fragment.

    As a terminal fragment, it either precedes a matcher or is used as
    a matcher itself (a special case, calling the "be" matcher to
    check for identity).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hidden = False

    def __call__(self, other):
        self.hidden = True
        return self.matcher("be")(other)

    def __repr__(self):
        if self.hidden:
            return repr(self.prev)
        else:
            return repr(self.prev) + " " + self.name

    __eq__  = lambda self, other: self.matcher('==')(other)
    __ne__  = lambda self, other: self.matcher('!=')(other)
    __lt__  = lambda self, other: self.matcher('<' )(other)
    __le__  = lambda self, other: self.matcher('<=')(other)
    __gt__  = lambda self, other: self.matcher('>' )(other)
    __ge__  = lambda self, other: self.matcher('>=')(other)
