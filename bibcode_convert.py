#!/usr/bin/env python2
"""
Convert long-form Journal names to the appropriate ApJ bibcode.

Requires the `bibtexparser` module.
"""

import re
import sys
import os
try:
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.bwriter import to_bibtex
except:
    sys.stderr.write('Error: could not load bibtexparser module.')
    sys.exit(-1)

# get ibliographic codes from: http://adsabs.harvard.edu/abs_doc/refereed.html
journals = {'monthly notices of the royal astronomical society': '\mnras',
            'astrophysical journal letters': '\apjl',
            'astrophysical journal supplement': '\apjs',
            'astrophysical journal': '\apj'}
