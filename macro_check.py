#!/usr/bin/env python2
"""
Compare privon_astro.sty entries with entries in a latex file to decide which
macros to copy into a file for submission to journals.
"""

import re
import sys
import os


def main():
    """
    actual script
    """
    # extract list of macros to search for
    macros = {}
    if os.path.isfile(os.environ['HOME'] +
                      '/astro/software/Astronomy/Papers/privon_astro.sty'):
        sty = open(os.environ['HOME'] +
                   '/astro/software/Astronomy/Papers/privon_astro.sty', 'r')
        for line in sty:
            if re.search('newcommand', line):
                macros[line.split('{')[1].split('}')[0]] = line
        sty.close()

    texfile = sys.argv[1]

    if os.path.isfile(texfile):
        inf = open(texfile, 'r')
    else:
        sys.stderr.write('Error opening: ' + texfile + '. Not found.\n')
        sys.exit(-1)

    keeplist = {}
    for line in inf:
        for macro in macros:
            if re.search(macro, line):
                keeplist[macro] = macros[macro]
                macros.pop(macro)
    inf.close()

    sys.stdout.write('Finished searching ' + texfile)
    if len(keeplist):
        sys.stdout.write('. Please copy the following macros into your \
manuscript:\n\n')
        for macro in keeplist:
            sys.stdout.write(keeplist[macro])
    else:
        sys.stdout.write('. No macros need to be copied.\n')


if __name__ == "__main__":
    main()
