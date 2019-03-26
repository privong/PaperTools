# Papers

Scripts and LaTeX files for assistance in writing papers.

## Contents

* `add_arXiv_IDs_to_library.py` Given a list of arXiv IDs, retrieve BibTex records for those from NASA ADS
* `bib_update.py`	Search a bibtex file and query ADS to update arXiv records w/ published references
* `bibcode_convert.py` Convert long-form journal names into the ApJ short form requivalents. (IN PROGRESS)
* `check_ms.sh` Run through the final manuscript checks (spelling, complete sentences).
* `macro_check.py` Figure out which macros to copy from privon_astro.sty into a manuscript for self-contained submission
* `privon_astro.sty` A collection of macros for LaTeX documents
* `punctuation_check.py` Simple checking for the existence of sentence-ending punctuation at the end of lines in LaTeX files, to catch incomplete sentences.
* `readability.py` Compute the [Flesch–Kincaid readability tests](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests) on a given text. Requires the [textstat](https://pypi.python.org/pypi/textstat) python module.
* `single_pdf.py` Combine multiple pdfs into a single file. (Useful for proposals which lack TeX templates).

`check_ms.sh` tries to run [proselint](https://github.com/amperser/proselint/), so install that if you would like writing commentary.
