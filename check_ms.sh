#!/bin/bash

aspell -t check $1
python /home/george/astro/software/Astronomy/PaperTools/punctuation_check.py $1
python /home/george/astro/software/Astronomy/PaperTools/readability.py $1
python /home/george/astro/software/Astronomy/PaperTools/macro_check.py $1
