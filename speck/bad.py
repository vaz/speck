# horrible stuff
"""
@property
def _(self):
    return self.__speck_value

# now try to get it to behave like the original in every other way
# this is possibly dangerous

def __getattribute__(self, name):
    if name in ('should', 'should_not', '_should', '_should_not'):
        # If the wrapped object has should or should_not already,
        # we won't clobber them.  It's up to the user to know
        # this and to use _should and _should_not instead.
        if name.startswith('_') and hasattr(self.__speck_value, name[1:]):
            return object.__getattribute__(self, name[1:])
        elif hasattr(self.__speck_value, name):
            return self.__speck_value.name
        else:
            return object.__getattribute__(self, name)

__repr__    = lambda s: repr(s.__speck_value)
__str__     = lambda s: str(s.__speck_value)
__unicode__ = lambda s: unicode(s.__speck_value)
__lt__      = lambda s, o: s.__speck_value <  o
__le__      = lambda s, o: s.__speck_value <= o
__eq__      = lambda s, o: s.__speck_value == o
__ne__      = lambda s, o: s.__speck_value != o
__gt__      = lambda s, o: s.__speck_value >  o
__ge__      = lambda s, o: s.__speck_value >= o
__cmp__     = lambda s, o: s.__speck_value.__cmp__(o)
__hash__    = lambda s: hash(s.__speck_value)
__nonzero__ = lambda s: bool(s.__speck_value)
__getattr__ = lambda s, n: getattr(s.__speck_value, n)
__setattr__ = lambda s, n, v: setattr(s.__speck_value, n, v)
__delattr__ = lambda s, n: s.__speck_value.__delattr__(n)
# __instancecheck__
# __subclasscheck__
__call__    = lambda s,*a,**kw: s.__speck_value(*a, **kw)
__len__     = lambda s: len(s.__speck_value)
__getitem__ = lambda s, k: s.__speck_value[k]
__setitem__ = lambda s, k, v: s.__speck_value.__setitem__(k,v)
__delitem__ = lambda s, k: s.__speck_value.__delitem__(k)
__iter__    = lambda s: iter(s.__speck_value)
__reversed__= lambda s: reversed(s.__speck_value)
__contains__= lambda s, i: i in s.__speck_value
__getslice__= lambda s, i, j: s.__speck_value[i:j]
__setslice__= lambda s, i, j, l: s.__speck_value.__setslice__(i,j,l)
__delslice__= lambda s, i, j: s.__speck_value.__delslice__(i,j)
__add__     = lambda s, o: s.__speck_value + o
__sub__     = lambda s, o: s.__speck_value - o
__mul__     = lambda s, o: s.__speck_value * o 
__floordiv__= lambda s, o: s.__speck_value // o 
__mod__     = lambda s, o: s.__speck_value % o
__divmod__  = lambda s, o: divmod(s.__speck_value, o)
__pow__     = lambda s, *a: pow(s.__speck_value, *a)
__lshift__  = lambda s, o: s.__speck__value << o
__rshift__  = lambda s, o: s.__speck__value >> o
__and__     = lambda s, o: s.__speck__value & o
__xor__     = lambda s, o: s.__speck__value ^ o
__or__      = lambda s, o: s.__speck__value | o
__div__     = lambda s, o: s.__speck__value / o
__truediv__ = lambda s, o: s.__speck__value / o
__radd__     = lambda s, o: o + s.__speck_value
__rsub__     = lambda s, o: o - s.__speck_value
__rmul__     = lambda s, o: o * s.__speck_value
__rfloordiv__= lambda s, o: o // s.__speck_value
__rmod__     = lambda s, o: o % s.__speck_value
__rdivmod__  = lambda s, o: divmod(o, s.__speck_value)
__rpow__     = lambda s, o: o ** s.__speck_value
__rlshift__  = lambda s, o: o << s.__speck__value
__rrshift__  = lambda s, o: o >> s.__speck__value
__rand__     = lambda s, o: o & s.__speck__value
__rxor__     = lambda s, o: o ^ s.__speck__value
__ror__      = lambda s, o: o | s.__speck__value
__iadd__    = lambda s, o: s.__speck_value.__iadd__(o)
__isub__    = lambda s, o: s.__speck_value.__isub__(o)
__imul__    = lambda s, o: s.__speck_value.__imul__(o)
__idiv__    = lambda s, o: s.__speck_value.__idiv__(o)
__itruediv__ = lambda s, o: s.__speck_value.__itruediv__(o)
__ifloordiv__ = lambda s, o: s.__speck_value.__ifloordiv__(o)
__imod__    = lambda s, o: s.__speck_value.__imod__(o)
__ipow__    = lambda s, o: s.__speck_value.__ipow__(o)
__ilshift__ = lambda s, o: s.__speck_value.__ilshift__(o)
__irshift__ = lambda s, o: s.__speck_value.__irshift__(o)
__iand__    = lambda s, o: s.__speck_value.__iand__(o)
__ixor__    = lambda s, o: s.__speck_value.__ixor__(o)
__ior__     = lambda s, o: s.__speck_value.__ior__(o)
__neg__     = lambda s: -s.__speck_value
__pos__     = lambda s: +s.__speck_value
__abs__     = lambda s: abs(s.__speck_value)
__invert__  = lambda s: ~s.__speck_value
__complex__ = lambda s: complex(s.__speck_value)
__int__     = lambda s: int(s.__speck_value)
__long__    = lambda s: long(s.__speck_value)
__float__   = lambda s: float(s.__speck_value)
__oct__     = lambda s: oct(s.__speck_value)
__hex__     = lambda s: hex(s.__speck_value)
__index__   = lambda s: s.__speck_value.__index__()
__coerce__  = lambda s, o: s.__speck_value.__coerce__(o)
__enter__   = lambda s: s.__speck_value.__enter__()
__exit__    = lambda s, a, b, c: s.__speck_value.__exit__(a,b,c)
"""
