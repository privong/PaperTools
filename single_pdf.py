#!/usr/bin/env python
"""
Combine multiple PDFs into a single PDF, in the order specified on the
command line.

Requires the PyPDF2 module.
"""


import sys
import argparse
try:
    from PyPDF2 import PdfFileReader, PdfFileWriter
except ImportError:
    sys.stderr.write("Error: could not import PyPDF2.\n\n")
    sys.exit(-1)


def main():
    """
    main routine
    """

    parser = argparse.ArgumentParser(description='Combine a bunch of pdf files \
                        into a single pdf file.')
    parser.add_argument('pdfs', type=str, nargs='+', help='PDFs to combine \
                        (in the order of combination).')
    parser.add_argument('-outfile', action='store', default='output.pdf',
                        help='Name of output file.')
    args = parser.parse_args()

    output = PdfFileWriter()

    for pdf in args.pdfs:
        try:
            inpdf = PdfFileReader(open(pdf, 'rb'))
            for i in range(inpdf.getNumPages()):
                output.addPage(inpdf.getPage(i))
        except:
            sys.stderr.write("Error opening " + pdf + "\n")

    output.write(open(args.outfile, "wb"))


if __name__ == "__main__":
    main()
