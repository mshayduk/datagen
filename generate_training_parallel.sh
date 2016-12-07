#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Makes ground truth from png pages and corresponding txt files"
  #echo "Usage: `basename $0` [pdffile_pages directory (write with slash at the end: /)]"
  echo " PARALLEL: run with command : ls -d ./GDATA/*pages/ | parallel --no-notice -j3 ./generate_training_parallel.sh {}"
  exit 0
fi

#useful trick: passes result of find to identify
# find ./0246/*.png -print0 | xargs -0 identify

#mkdir -p $1'/book/'

prefix=`echo $1 | sed -e "s/\_pages\/$//" | awk -F '/' '{print $NF}'`
echo $prefix

# binarize pages (no skew is assumed, no fancy threshold estimation)
#echo 'binarization in $1 '
#ocropus-nlbin -n --maxskew 0 --escale 0 --lo 0 --hi 1 --parallel 6 $1/$prefix-????.png -o $1'/book/'
#exit

# segment pages (only one column assumed, no noise removal )
#echo 'segmentation in $1'
#ocropus-gpageseg -n --maxseps 0 --maxcolseps 0 --minscale 10 --noise 0 --parallel 5 $1'/book/????.bin.png'
#exit
#ocropus-gpageseg -n --maxseps 0 --maxcolseps 0 --csminheight 90 --minscale 10 --noise 0 --parallel 6 './GDATA/qcr_tiny_regular_pages/book/????.bin.png'

# make ground truth text
# NOTE: segmented pages pagenum (in book/[pagenum]/) starts from 1, txt pages start from 0 !
cnt=0
for b in $(ls -p $1/'book/' | grep '/');
	do
		# get correct id, if file sequence has gaps due to the failed previous steps
		id=`ls -d $1/book/$b | awk -F '/' '{print $(NF-1)}' | sed -e 's:^0*::'`
		id=`echo $(($id - 1))`
		txt=$(ls $1/*$id.txt | head -1)
		#txt=$(ls $1/*$cnt.txt | head -1)
		#cp $txt $1/book/$b/ 

		#echo 'making gt: ' $1/book/$b  'id='$id 'cnt='$cnt $txt
		#splitting txt to gt.txt lines
		#for l in $1/book/$b/*.png;
		
		#skip pages with number of segments not equal to the number of lines
		nsnippets=$(ls -1 $1/book/$b/*bin.png | wc -l)
		nlines=$(cat $txt | wc -l)	
		if [ $nsnippets != $nlines ]; then
			continue
		fi

		linecnt=0
		for l in $(ls -1 $1/book/$b/*bin.png | sed -e 's/\.bin.png$//'); #only names, no extentions
			do
				linecnt=$(($linecnt+1))
				echo $l $linecnt $nsnippets $nlines $(sed -n "${linecnt}{p;q;}" $txt)
				$(sed -n "${linecnt}{p;q;}" $txt > $l.gt.txt) 
			done;

		cnt=$(($cnt+1))
	done;
