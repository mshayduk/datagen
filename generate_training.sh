#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Makes ground truth from png pages and corresponding txt files"
  echo "Usage: `basename $0` [pdffile_pages directory (write with slash at the end: /)]"
  exit 0
fi

mkdir -p $1'/book/'

prefix=`echo $1 | sed -e "s/\_pages\/$//" | awk -F '/' '{print $NF}'`
echo $prefix
# binarize pages
#ocropus-nlbin -n $1/test-????.png -o $1'/book/'

# segment pages
#ocropus-gpageseg -n $1'/book/????.bin.png'

# make ground truth text
# NOTE: segmented pages pagenum (in book/[pagenum]/) starts from 1, txt pages start from 0 !
cnt=0
for b in $(ls -p $1/'book/' | grep '/');
	do
		txt=$(ls $1/*$cnt.txt | head -1)
		#cp $txt $1/book/$b/ 
		
		echo $1/book/$b $cnt $npages $txt
		#splitting txt to gt.txt lines
		#for l in $1/book/$b/*.png;
		
		linecnt=0
		for l in $(ls -1 $1/book/$b/*bin.png | sed -e 's/\.bin.png$//'); #only names, no extentions
			do
				linecnt=$(($linecnt+1))
				echo $l $linecnt $(sed -n "${linecnt}{p;q;}" $txt)
				# $(sed -n "${linecnt}{p;q;}" $txt > $l.gt.txt) 
			done;

		cnt=$(($cnt+1))
	done;
