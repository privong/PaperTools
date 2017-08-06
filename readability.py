#!/usr/bin/env python
"""
Take an input file and print out the Flesch reading ease score and the
Flesch-Kincaid reading grade.

Requires the 'textstat' module.
https://pypi.python.org/pypi/textstat
"""

import sys
try:
    from textstat.textstat import textstat
except ImportError:
    sys.stderr.write("Error: could not import textstat module.\n\n")
    sys.exit(-1)


def main():
    """
    Evaluate and print Readability scores
    """

    if len(sys.argv) > 1:
        inf = open(sys.argv[1], 'r')
    else:
        sys.stderr.write('Error: specify input file.\n')
        sys.exit()

    text = inf.read()
    inf.close()

    lexcount = textstat.lexicon_count(text)

    sys.stdout.write('Lexicon count: {0:d}\n'.format(lexcount))
    
    # reading time in minutes
    # assumes 180 WPM plus some offset
    tread = (lexcount + 250) / 180.

    sys.stdout.write('Estimating reading time: {0:1.1f} minutes.\n'.format(tread))

    ease = textstat.flesch_reading_ease(text)
    grade = textstat.flesch_kincaid_grade(text)

    sys.stdout.write('Flesch reading ease score: {0:1.1f}\n'.format(ease))
    sys.stdout.write('Flesch-Kincaid grade: {0:1.1f}\n'.format(grade))


if __name__ == '__main__':
    main()
