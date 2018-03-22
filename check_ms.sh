#!/bin/bash

aspell -t check $1
echo ""
python /home/george/astro/software/Astronomy/PaperTools/punctuation_check.py $1
echo ""
python /home/george/astro/software/Astronomy/PaperTools/readability.py $1
echo ""
proselint $1
echo ""
python /home/george/astro/software/Astronomy/PaperTools/macro_check.py $1
echo ""
echo "SHA384sum of the contents of $1:"
sha384sum $1
echo ""
echo "SHA384sum of the filename $1:"
echo $1 | sha1sum
