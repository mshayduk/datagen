#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Converts multipage pdf to text and png files (one txt and png file per page)"
  echo "Usage: `basename $0` [filename.pdf]"
  exit 0
fi
datagensys="./"
datadir=$(dirname "$1")
filename=$(basename "$1")
extension="${filename##*.}"
name="${filename%.*}"
#name=$(echo $1 | cut -f 1 -d '.')
npages=$(pdfinfo $1 | grep Pages | sed 's/[^0-9]*//')
droplast=50
npages=$(($npages-$droplast-1))

mkdir -p $datadir'/'$name'_pages'
#find $name'_pages/*' -print0 | xargs -0 rm -rv
cp $1 $datadir'/'$name'_pages'
cd $datadir'/'$name'_pages'

for f in $1;
	do
    	page=0
    	for i in $(seq -f "%04g" 0 $npages); 
        	do
        	page=$(($page+1))
        	pdftotext -f "$page" -l $l "$page" -layout $name'.pdf' "${name%.pdf}-$i.txt";
        	pdftk $name'.pdf' cat $page'-'$page output "${name%.pdf}-$i.pdf"
        	convert -density 300 "${name%.pdf}-$i.pdf" "${name%.pdf}-$i.png" 
    		#echo $f "${name%.pdf}-$i.txt" $i "$page"
    		python $datagensys'/utf8normalize.py' "NFC" "${name%.pdf}-$i.txt"
    	done; 
done

#convert -density 300 $name.pdf $name-%04d.png 
