#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Converts multipage pdf to text and png files (one txt and png file per page)"
  echo "Usage: `basename $0` [filename.pdf]"
  exit 0
fi
datagensys="/home/maxim/Projects/Doker/sandbox/traindatagen/python/"
datadir=$(dirname "$1")
filename=$(basename "$1")
extension="${filename##*.}"
name="${filename%.*}"
#name=$(echo $1 | cut -f 1 -d '.')
npages=$(pdfinfo $1 | grep Pages | sed 's/[^0-9]*//')
droplast=300
npages=$(($npages-$droplast-1))

mkdir -p $datadir'/'$name'_pages_bin'
mkdir -p $datadir'/'$name'_pages_bin/book/'
cp $1 $datadir'/'$name'_pages_bin'

# change workingdir to the pages directory
cd $datadir'/'$name'_pages_bin'
# loop ove pdf files (usually only one )
for f in $1;
	do
    	page=0
    	for i in $(seq -f "%04g" 0 $npages); 
        	do
        	page=$(($page+1))
        	pdftotext -f "$page" -l $l "$page" -layout $name'.pdf' "${name%.pdf}-$i.txt";
        	pdftk $name'.pdf' cat $page'-'$page output "${name%.pdf}-$i.pdf"
        	#convert -density 300 "${name%.pdf}-$i.pdf" "${name%.pdf}-$i.png" 
    		echo $f "${name%.pdf}-$i.txt" $i "$page"
    		python $datagensys'/utf8normalize.py' "NFC" "${name%.pdf}-$i.txt"
    	done;

    	find . -name '*-*.pdf' | parallel --no-notice -j6 convert -density 300 {} {}.jpg
    	rename 's/\.pdf\.jpg/\.jpg/g' *.pdf.jpg
    	
    	#rename 's/\.pdf\.png/\.png/g' *.pdf.png
    	
    	#noisify 
    	find . -name '*-*.jpg' | parallel --no-notice -j6 python $datagensys'/noisify.py' $datagensys'/GNOISE/' {}
    	find . -name '*-*.jpg' | parallel --no-notice -j6 convert -density 300 {} {}.png
    	rename 's/\.jpg\.png/\.png/g' *.jpg.png
    	
    	#page binarization and segmentation
    	ocropus-nlbin -n --maxskew 0 --parallel 6 './'$name-????.png -o './book/'
    	rm *.png
    	rm *.jpg
    	rm ./book/*.nrm.png
    	ocropus-gpageseg -n --maxseps 0 --maxcolseps 0 --minscale 9 --noise 2 --parallel 6 './book/????.bin.png'
done

echo "Generating ground truth text in" $datadir'/'$name'_pages_bin/book/'
cd $datagensys
/bin/bash ./generate_training_parallel.sh $datadir'/'$name'_pages_bin/'
