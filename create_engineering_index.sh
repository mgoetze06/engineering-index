#!/bin/bash

echo "Hello World"
git pull https://github.com/mgoetze06/engineering-index
cd latex-code
pdflatex -interaction=batchmode main.tex
title="$(date -I)_engineering_index.pdf"
echo "${title}"
cp main.pdf /home/boris/Dokumente/engineering-index/${title}
git add .
git commit -m "index updated, new pdf created"
git push https://github.com/mgoetze06/engineering-index
