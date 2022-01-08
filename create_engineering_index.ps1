$destination_file = Get-Location
git pull https://github.com/mgoetze06/engineering-index



$date=(Get-Date).ToString("yyyy_MM_dd")
$newfile = $destination_file.path + "\" + $date + "_engineering_index.pdf"
Set-Location -Path latex-code
pdflatex -interaction=batchmode main.tex

Copy-Item "main.pdf" $newfile
Set-Location -Path $destination_file.path
git add .
git commit -m "index updated, new pdf created"
git push https://github.com/mgoetze06/engineering-index