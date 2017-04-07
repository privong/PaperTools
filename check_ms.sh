#!/bin/bash

aspell -t check $1
python /home/george/astro/software/Astronomy/PaperTools/punctuation_check.py $1
python /home/george/astro/software/Astronomy/PaperTools/readability.py $1
sha384sum $1
echo $1 | sha1sum
