#!/bin/bash
cp --help
cd latex-code
echo $(date -I)
title="$(date -I)_engineering_index.pdf"
newfile="C:\Users\Maurice\Documents\Engineering*Index\${title}"
echo "${newfile}"
cp main.pdf ${newfile}
read
