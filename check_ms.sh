#!/bin/bash

REGEX_TEX="tex$"
REGEX_HTML="html$"

if [[ $1 =~ $REGEX_TEX ]] ;
then
    aspell -t check $1
elif [[ $1 =~ $REGEX_HTML ]];
then
    aspell -H check $1
fi

echo ""
python /home/george/astro/software/Astronomy/PaperTools/punctuation_check.py $1

if [[ $1 =~ $REGEX_TEX ]] ;
then
    echo ""
    texcount -merge -incbib -dir -sub=none -utf8 -sum $1

    echo ""
    python /home/george/astro/software/Astronomy/PaperTools/macro_check.py $1
fi

echo ""
python /home/george/astro/software/Astronomy/PaperTools/readability.py $1

echo ""
proselint $1

echo ""
echo "SHA384sum of the contents of $1:"
sha384sum $1

echo ""
echo "SHA384sum of the filename $1:"
echo $1 | sha1sum
