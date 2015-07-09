

# Coconut Header: --------------------------------------------------------------

from __future__ import with_statement, print_function, absolute_import, unicode_literals, division
try: from future_builtins import *
except ImportError: pass
try: xrange
except NameError: pass
else:
    range = xrange
try: ascii
except NameError: ascii = repr
try: unichr
except NameError: unichr = chr
try: unicode
except NameError: pass
else:
    bytes, str = str, unicode
    _coconut_print = print
    def print(*args, **kwargs):
        """Wraps _coconut_print."""
        return _coconut_print(*(str(x).encode("utf8") for x in args), **kwargs)
try: raw_input
except NameError: pass
else:
    _coconut_input = raw_input
    def input(*args, **kwargs):
        """Wraps _coconut_input."""
        return _coconut_input(*args, **kwargs).decode("utf8")

"""Built-in Coconut Functions."""

import functools
partial = functools.partial
reduce = functools.reduce

import operator
itemgetter = operator.itemgetter
attrgetter = operator.attrgetter
methodcaller = operator.methodcaller

import itertools
chain = itertools.chain
islice = itertools.islice
takewhile = itertools.takewhile
dropwhile = itertools.dropwhile
tee = itertools.tee

import collections
data = collections.namedtuple

try:
    import collections.abc as abc
except ImportError:
    abc = collections

def recursive(func):
    """Tail Call Optimizer."""
    state = [True, None]
    recurse = object()
    @functools.wraps(func)
    def tailed_func(*args, **kwargs):
        """Tail Recursion Wrapper."""
        if state[0]:
            state[0] = False
            try:
                while True:
                    result = func(*args, **kwargs)
                    if result is recurse:
                        args, kwargs = state[1]
                        state[1] = None
                    else:
                        return result
            finally:
                state[0] = True
        else:
            state[1] = args, kwargs
            return recurse
    return tailed_func
