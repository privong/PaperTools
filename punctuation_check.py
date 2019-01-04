#!/usr/bin/env python
"""
Scan a (La)TeX or Markdown file to find missing puctuation.
Assumes the file is created with a single sentence per line.
"""

import re
import os
import sys
import argparse


def getargs():
    """
    Parse and return command line arguments
    """
    parser = argparse.ArgumentParser(description="Scan a (La)TeX or \
Markdown file to find lines that are missing terminating punctuation.")
    parser.add_argument('infile', type=str, default=None,
                        help="Name of (La)TeX or Markdown file to scan.")
    return parser.parse_args()


def main():
    """
    main routine
    """

    args = getargs()

    if not os.path.isfile(args.infile):
        sys.stderr.write(args.infile + " could not be located.\n")
        sys.exit(1)

    infile = open(args.infile, 'r')

    nlines = 1
    YAMLhead = False
    for line in infile.readlines():
        line = line.rstrip('\n')
        if len(line) < 2:
            # empty or uninteresting line, skip
            continue
        elif line[:3] == '---':
            # YAML header block
            if not YAMLhead:
                YAMLhead = True
            else:
                YAMLhead = False
        elif YAMLhead:
            continue
        elif line[0] == '\\':
            # LaTex command, skip line
            # this is potentially dangerous, if the line starts with a macro
            continue
        elif line[-1] == '}' or line[-2:] == '\\\\':
            # end of a command, skip line
            continue
        elif line[0] == '%' or line[0] == '#':
            # skip lines that are entirely comments, for TeX and markdown
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

    infile.close()


if __name__ == "__main__":
    main()
