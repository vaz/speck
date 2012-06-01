import sys
import itertools

# import print_statement and unicode_literals


if sys.version_info < (3, 0):
    range = xrange
    zip = itertools.izip
    map = itertools.imap
    filter = itertools.ifilter
    # use functools.reduce

