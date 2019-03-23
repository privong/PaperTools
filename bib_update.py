#!/usr/bin/env python
"""
Load a bibtext file, find the arXiv entries within the past X years and
query ADS to see if the paper has been published. If so, update the bibtex
entry.
"""


import sys
import os
import shutil
import re
import codecs   # for unicode
import argparse
try:
    import ads  # https://github.com/andycasey/ads
except ImportError:
    sys.stderr.write('Error: could not import ads module.\n\n')
    sys.exit(-1)
try:
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.bwriter import to_bibtex
except ImportError:
    sys.stderr.write('Error: could not import bibtexparser module.\n\n')
    sys.exit(-1)


def checkRef(entry, args):
    """
    Check ADS for an updated reference

    If a replacement entry is located, replace the following bibtex keys
        - doi
        - publication year
        - abstract
        - url
        - volume
        - page
        - year
        - pub(lication) (does not currently do abbreviations)
    """
    if 'eprint' in entry.keys():
        res = ads.SearchQuery(q="arXiv:" + entry['eprint'],
                              fl=['pub', 'author', 'title', 'year',
                                  'journal', 'doi', 'abstract', 'url',
                                  'volume', 'page', 'bibcode'])
        res.execute()
        try:
            for i in res:
                try:    # only want things that are published
                    if not(args.quiet):
                        print(i.pub)
                    if re.search('arxiv', i.pub, re.IGNORECASE):
                        continue
                except:
                    continue
                if args.confirm:
                    print(entry['author'].split(',')[0], entry['title'], \
                          entry['year'])
                    print(i.author[0], i.title[0], i.year)
                    sel = raw_input('Is this a match (y/n)? ')
                else:
                    sel = 'y'
                if sel == 'y':  # replace relevant bibtex entries
                    entry['author'] = '{' + entry['author'] + '}'
                    entry['title'] = i.title[0]
                    entry['year'] = i.year
                    entry['journal'] = i.pub
                    try:
                        entry['doi'] = i.doi[0]
                    except:
                        pass
                    try:
                        entry['abstract'] = i.abstract
                    except:
                        pass
                    #entry['link'] = i.url[0]
                    entry['year'] = i.year
                    try:
                        if entry['volume']:
                            entry['volume'] = i.volume
                    except:
                        pass
                    try:
                        entry['pages'] = i.page[0]
                    except:
                        pass
                    entry['adsurl'] = 'http://adsabs.harvard.edu/abs/' + \
                                      i.bibcode
                    if not(re.search(i.year, entry['ID'])):
                        sys.stderr.write("Warning: Updating year of: " +
                                         entry['ID'] +
                                         " to reflect publication year (" +
                                         i.year + ").\n")
                        entry['ID'] = entry['ID'].split('2')[0] + i.year
                    return entry
        except:
            sys.stderr.write("API issue")
        return False

def aref(entry, confirm=False):
    """
    Check ADS for a preprint associated with a published article.
    """
    if 'doi' in entry.keys():
        res = ads.query('doi:' + entry['doi'])
        try:
            for i in res:
                try:
                    for j in i.identifier:
                        if re.search('arXiv:', j):
                            ID = j.split(':')[1]
                            entry['arxivid'] = ID
                            entry['Eprint'] = ID
                            entry['archiveprefix'] = 'arXiv'
                            return entry
                        elif re.search('astro-ph/', j):
                            ID = j
                            entry['arxivid'] = ID
                            entry['Eprint'] = ID
                            entry['archiveprefix'] = 'arXiv'
                            return entry
                except:
                    pass
        except:
            entry['arxivsearched'] = 'True'
            return entry
    entry['arxivsearched'] = 'True'
    return entry



def main():
    """
    main routine
    """
    parser = argparse.ArgumentParser(description="Update arXiv entries in a \
bibtex file with subsequently published papers.")
    parser.add_argument('bibfile', action='store', type=str, default=False,
                        help='BibTeX file')
    parser.add_argument('--confirm', '-c', action='store_true', default=False,
                        help='If passed, confirm each entry.')
    parser.add_argument('--arXiv', '-a', action='store_true', default=False,
                        help='For published entries, Search ADS for an arXiv \
entries if not present.')
    parser.add_argument('--quiet', action='store_true', default=False,
                        help='Suppress printed output. (Overriden by \
--confirm).')
    args = parser.parse_args()

    if os.path.isfile(args.bibfile):
        bib = codecs.open(args.bibfile, 'r', 'utf-8')
        bp = BibTexParser(bib.read(), common_strings = True)
        bib.close()
    else:
        sys.stderr.write("Error, could not open: " + args.bibfile + ".\n")
        sys.exit(1)

    # back up library before we start
    shutil.copy2(args.bibfile, args.bibfile + 'ads_updater.bak')

    upcount = 0
    acount = 0
    match = False
    aphsearch = False
    j = 0
    for j in range(len(bp.entries)):
        thisref = bp.entries[j]
        if thisref['ENTRYTYPE'] == 'article':  # not interested in other types 
            if 'journal' in thisref.keys():
                if re.search('arxiv', thisref['journal'], re.IGNORECASE):
                    match = True
                elif 'eprint' not in thisref.keys() and args.arXiv:
                    aphsearch = True
            elif 'Journal' in thisref.keys():
                if re.search('arxiv', thisref['Journal'], re.IGNORECASE):
                    match = True
                elif 'eprint' not in thisref.keys() and args.arXiv:
                    aphsearch = True
            else:
                if 'arxivid' in thisref.keys():
                    match = True
                else:
                    if not(args.quiet):
                        sys.stdout.write(thisref['ID'] + \
                                         ' does not have a journal entry or \
arXiv ID.\n')

            if match:
                match = False   # reset
                if not(args.quiet):
                    sys.stdout.write('Searching for update to ' + 
                                     thisref['ID'] + '...')
                res = checkRef(thisref, args)
                if res:
                    upcount += 1
                    bp.entries[j] = res
                    if not(args.quiet):
                        sys.stdout.write(thisref['ID'] +
                                         " updated. Please verify changes.\n")
                    newbib = to_bibtex(bp)
                    if upcount + acount % 20 == 0:
                        outf = codecs.open(args.bibfile, 'w', 'utf-8')
                        outf.write(newbib)
                        outf.close()

                else:
                    if not(args.quiet):
                        sys.stdout.write("No new version found.\n")

            if aphsearch and \
               (not('arxivsearched' in thisref.keys()) or \
               (not('Eprint' in thisref.keys()) or \
                not('eprint' in thisref.keys()))) and \
               thisref['year'] >= '1991':
                aphsearch = False
                if not(args.quiet):
                    sys.stdout.write('No preprint associated with ' +
                                     thisref['ID'] + ', checking...\n')
                res = aref(thisref, args.confirm)
                if res and not('arxivsearched' in thisref.keys()):
                    acount += 1
                    bp.entries[j] = res
                    if not(args.quiet):
                        sys.stdout.write(thisref['ID'] +
                                         " updated with a preprint. Please \
verify changes.\n")
                    newbib = to_bibtex(bp)
                    if upcount + acount % 20 == 0:
                        outf = codecs.open(args.bibfile, 'w', 'utf-8')
                        outf.write(newbib)
                        outf.close()
                elif 'arxivsearched' in thisref.keys():
                    if not(args.quiet):
                        sys.stdout.write("No preprint found. Will not search \
again.\n")
                else:
                    if not(args.quiet):
                        sys.stdout.write("No preprint found.\n")

    outf = codecs.open(args.bibfile, 'w', 'utf-8')
    try:
        outf.write(newbib)
    except:
        outf.write(to_bibtex(bp))
    outf.close()

    if not(args.quiet):
        sys.stdout.write(str(upcount) +
                         ' reference(s) updated with journal articles.\n')
    if args.arXiv and not(args.quiet):
        sys.stdout.write(str(acount) + 
                         ' reference(s) updated with preprints.\n')


if __name__ == "__main__":
    main()
