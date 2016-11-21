#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Converts multipage pdf to text files (one txt file per page)"
  echo "Usage: `basename $0` [filename.pdf]"
  exit 0
fi

name=$(echo $1 | cut -f 1 -d '.')
npages=$(pdfinfo $1 | grep Pages | sed 's/[^0-9]*//')
npages=$(($npages-1))

mkdir -p $name'_pages'
#find $name'_pages/*' -print0 | xargs -0 rm -rv
cp $1 $name'_pages'
cd $name'_pages'

for f in $1;
	do
    	page=0
    	for i in $(seq -f "%04g" 0 $npages); 
        	do
        	page=$(($page+1))
        	pdftotext -f "$page" -l $l "$page" -layout $f "${f%.pdf}-$i.txt";  
    		#echo "${f%.pdf}-$i.txt" $i "$page"
    	done; 
done

#convert -density 300 $name.pdf $name-%04d.png 
