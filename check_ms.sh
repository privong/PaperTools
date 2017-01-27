#!/bin/bash

aspell -t check $1
python /home/george/astro/software/Astronomy/PaperTools/punctuation_check.py $1
