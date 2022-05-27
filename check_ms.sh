#!/bin/bash

REGEX_TEX="tex$"
REGEX_HTML="html$"
REGEX_MUTT="/mutt-*"
REGEX_MD="md$"

CHECK_PREFIX="$HOME/astro/software/PaperTools/"

if [[ $1 =~ $REGEX_TEX ]] ;
then
    aspell -t check $1
elif [[ $1 =~ $REGEX_HTML ]];
then
    aspell -H check $1
elif [[ $1 =~ $REGEX_MUTT ]];
then
    aspell -e check $1
elif [[ $1 =~ $REGEX_MD ]];
then
    aspell -M check $1
else
    aspell check $1
fi

if [[ $1 =~ $REGEX_MUTT ]];
then
    echo "Skipping line check for mutt email message."
    echo "Removing 'Disarmed', 'External' tags from subject lines."
    sed -i -e 's/{Disarmed}//' $1
    sed -i -e 's/{External}//' $1
else
    echo ""
    python $CHECK_PREFIX/punctuation_check.py $1
fi

if [[ $1 =~ $REGEX_TEX ]] ;
then
    echo ""
    texcount -merge -incbib -dir -sub=none -utf8 -sum $1

    echo ""
    python $CHECK_PREFIX/macro_check.py $1
fi

echo ""
python $CHECK_PREFIX/readability.py $1

echo ""
proselint $1

echo ""
echo "SHA384sum of the contents of $1:"
sha384sum $1

echo ""
echo "SHA384sum of the filename $1:"
echo $1 | sha1sum
