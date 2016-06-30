#!/usr/bin/env python

import re
import os
import sys
import argparse


parser = argparse.ArgumentParser(description="Scan a (La)TeX file to find lines that \
are missing terminating punctuation.")
parser.add_argument('texfile', type=str, default=None,
                    help="Name of (La)TeX file to scan.")
args = parser.parse_args()


if not(os.path.isfile(args.texfile)):
    sys.stderr.write(args.texfile + " could not be located.\n")
    sys.exit(1)

texfile = open(args.texfile, 'r')

n = 1
for line in texfile.readlines():
    line = line.rstrip('\n')
    if len(line) < 2:
        # empty or uninteresting line, skip
        skip = 1
    elif line[0] == '\\':
        # LaTex command, skip line
        # this is potentially dangerous, if the line starts with a macro
        skip = 1
    elif line[-1] == '}' or line[-2:] == '\\\\':
        # end of a command, skip line
        skip = 1
    else:
        if re.search(';', line[-2:]) or \
           re.search(',', line[-2:]):
            sys.stdout.write("Line {0:d} may have the wrong puctuation:\n".format(n))
            print('\t' + line[-10:])
        elif not(re.search('\.', line[-3:])) and \
             not(re.search('\?', line[-3:])) and \
             not(re.search('\!', line[-3:])):
            sys.stdout.write("Line {0:d} may be missing end punctuation:\n".format(n))
            print('\t' + line[-10:])
    n = n + 1

texfile.close()
