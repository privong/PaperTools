#!/usr/bin/env python
"""
Take a list of arXiv IDs (e.g., from vox charta votes) and add those entries to
the bibtex file if they are not already present.
"""


import sys
import os
import shutil
import codecs   # for unicode
import argparse
import datetime
try:
    import ads  # https://github.com/andycasey/ads
except ImportError:
    sys.stderr.write('Error: could not import ads module.\n\n')
    sys.exit(-1)
try:
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.bwriter import BibTexWriter
except ImportError:
    sys.stderr.write('Error: could not import bibtexparser module.\n\n')
    sys.exit(-1)


def getref(arXiv, args):
    """
    Query ADS and return the bibtex for a specified arXiv ID.
    """
    res = ads.SearchQuery(q="arXiv:" + arXiv,
                          fl=['bibcode'])
    res.execute()
    res = ads.ExportQuery(res.articles[0].bibcode)
    refbibtex = res.execute()
    if refbibtex:
        if not args.quiet:
            sys.stdout.write('Retrieved BibTeX for ' + arXiv + '.\n')
        return BibTexParser(refbibtex)

    return False


def updatebibtexkey(parsed_ref):
    """
    Update the BibTeX key so that it is AuthorYear.

    Requires a bibtex parsed entry

    """

    oldkey = parsed_ref.entries[0]['ID']
    # year is the first four entries in the bibcode
    year = oldkey[0:4]
    newkey = getfirstauthor(parsed_ref.entries[0]['author'])
    newkey += year

    # remove spaces in the key
    newkey = ''.join(newkey.split())

    parsed_ref.entries[0]['ID'] = newkey

    return parsed_ref


def getfirstauthor(BTauthorlist):
    """
    Extract the first author's surname from a BibTeX style authorlist
    """

    fa_surname = BTauthorlist.split('}', maxsplit=1)[0].split('{')[-1]

    return fa_surname



def main():
    """
    main routine
    """
    parser = argparse.ArgumentParser(description="Update arXiv entries in a \
bibtex file with subsequently published papers.")
    parser.add_argument('IDfile', action='store', type=str, default=None,
                        help='File containing list of arXiv IDs to search.')
    parser.add_argument('bibfile', action='store', type=str, default=False,
                        help='BibTeX file')
    parser.add_argument('--quiet', action='store_true', default=False,
                        help='Suppress printed output. (Overriden by \
--confirm).')
    parser.add_argument('--owner', action="store", default=None,
                        type=str,
                        help="Name to insert into BibTex entry under the \
'owner' field.")
    args = parser.parse_args()

    bpw = BibTexWriter()

    # get today's timestamp for adding to the BibTex file
    timestamp = datetime.datetime.now().strftime("%Y.%m.%d")

    # make sure we can open the specified files
    if os.path.isfile(args.IDfile):
        IDs = open(args.IDfile, 'r')
    else:
        sys.stderr.write("Error, could not open: " + args.IDfile + ".\n")

    if os.path.isfile(args.bibfile):
        bib = codecs.open(args.bibfile, 'r', 'utf-8')
        bp = BibTexParser(bib.read(), common_strings=True)
        bib.close()
    else:
        sys.stderr.write("Error, could not open: " + args.bibfile + ".\n")
        sys.exit(1)

    # back up library before we start
    shutil.copy2(args.bibfile, args.bibfile + '-vox_votes_adder.bak')

    arxivlist = []
    # first get a list of arXiv IDs already in the library
    for article in bp.entries:
        if 'eprint' in article.keys():
            if not article['eprint'] in arxivlist:
                arxivlist.append(article['eprint'])

    # open the bibtex file, we'll just append new entires
    outf = codecs.open(args.bibfile, 'a', 'utf-8')
    newcount = 0
    # now get bibtex entries from ADS for all new articles
    for ID in IDs:
        ID = ID.rstrip('\n')
        if ID in arxivlist or ID[0] == "#":
            # skip entries that we already have and comments
            continue

        # get ADS entry
        newref = getref(ID, args)
        # add owner information
        if args.owner is not None:
            newref.entries[0]['owner'] = args.owner
        # add timestamp information
        newref.entries[0]['timestamp'] = timestamp
        newcount += 1
        newref = updatebibtexkey(newref)

        outf.write(bpw.write(newref))

    outf.close()

    if newcount and not args.quiet:
        sys.stdout.write('{0:d} reference(s) added.\n'.format(newcount))


if __name__ == "__main__":
    main()
