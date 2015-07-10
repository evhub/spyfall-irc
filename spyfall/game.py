#!/usr/bin/env python

# Compiled with Coconut version 0.2.3-dev [Guam]



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

import sys as _coconut_sys
import os.path as _coconut_os_path
_coconut_sys.path.append(_coconut_os_path.dirname(_coconut_os_path.abspath(__file__)))
import __coconut__

reduce = __coconut__.reduce
itemgetter = __coconut__.itemgetter
attrgetter = __coconut__.attrgetter
methodcaller = __coconut__.methodcaller
takewhile = __coconut__.takewhile
dropwhile = __coconut__.dropwhile
tee = __coconut__.tee
recursive = __coconut__.recursive

# Compiled Coconut: ------------------------------------------------------------

import random

class game(__coconut__.data('game', 'location, players')):
    def roles(self):
        out = [""]
        roles = list(self.location.roles)
        random.shuffle(roles)
        for i in range(0, self.players - 1):
            if i < len(roles):
                out.append(roles[i])
            else:
                out.append(random.choice(roles))
        random.shuffle(out)
        return out
    def messages(self):
        for role in self.roles():
            if role:
                yield "You have been given the role " + role + " at the location " + self.location.name + "."
            else:
                yield "You are the spy!"

def new_game(locations, players):
    return game(random.choice(locations), players)
