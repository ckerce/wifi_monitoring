#!/bin/bash

cat outdat.csv | sed -e 's/,,,/,/g' -e 's/,,,/,/g' -e 's/,,/,/g' -e 's/,,/,/g' -e 's/,$//g' -e 's/_,/_/g' > tmp.csv && python proc_logfile.py -f tmp.csv
