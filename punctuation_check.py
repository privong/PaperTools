#!/usr/bin/env python
"""
Scan a (La)TeX file to find missing puctuation.
Assumes the file is created with a single sentence per line.
"""

import re
import os
import sys
import argparse


def main():
    """
    main routine
    """
    parser = argparse.ArgumentParser(description="Scan a (La)TeX file to \
find lines that are missing terminating punctuation.")
    parser.add_argument('texfile', type=str, default=None,
                        help="Name of (La)TeX file to scan.")
    args = parser.parse_args()


    if not os.path.isfile(args.texfile):
        sys.stderr.write(args.texfile + " could not be located.\n")
        sys.exit(1)

    texfile = open(args.texfile, 'r')

    nlines = 1
    for line in texfile.readlines():
        line = line.rstrip('\n')
        if len(line) < 2:
            # empty or uninteresting line, skip
            continue
        elif line[0] == '\\':
            # LaTex command, skip line
            # this is potentially dangerous, if the line starts with a macro
            continue
        elif line[-1] == '}' or line[-2:] == '\\\\':
            # end of a command, skip line
            continue
        elif line[0] == '%':
            # skip lines that are entirely comments
            continue
        else:
            if re.search(';', line[-2:]) or \
               re.search(',', line[-2:]):
                sys.stdout.write("Line {0:d} may have the wrong \
puctuation:\n".format(nlines))
                sys.stdout.write('\t' + line[-10:] + '\n')
            elif not re.search('\.', line[-3:]) and \
                 not re.search('\?', line[-3:]) and \
                 not re.search('\!', line[-3:]):
                sys.stdout.write("Line {0:d} may be missing end \
punctuation:\n".format(nlines))
                sys.stdout.write('\t' + line[-25:] + '\n')
        nlines += 1

    texfile.close()


if __name__ == "__main__":
    main()
