#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Makes ground truth from png pages and corresponding txt files"
  #echo "Usage: `basename $0` [pdffile_pages directory (write with slash at the end: /)]"
  echo " PARALLEL: run with command : ls -d ./GDATA/*pages/ | parallel --no-notice -j3 ./generate_training_parallel.sh {}"
  exit 0
fi

#useful trick: passes result of find to identify
# find ./0246/*.png -print0 | xargs -0 identify

# make ground truth text
# NOTE: segmented pages pagenum (in book/[pagenum]/) starts from 1, txt pages start from 0 !
cnt=0
for b in $(ls -p $1/'book/' | grep '/');
	do
		# get correct id, if file sequence has gaps due to the failed previous steps, i.e. page bin. pageseg...
		id=`ls -d $1/book/$b | awk -F '/' '{print $(NF-1)}' | sed -e 's:^0*::'`
		id=`echo $(($id - 1))`
		txt=$(ls $1/*$id.txt | head -1)
		
		#skip pages with number of segments not equal to the number of lines
		nsnippets=$(ls -1 $1/book/$b/*bin.png | wc -l)
		# remove blanck lines
		cat $txt | sed '/ˆ$/d' > out.txt
		cat out.txt > $txt 
		nlines=$(cat $txt | wc -l)	
		if [ $nsnippets != $nlines ]; then
			continue
		fi

		# write gt.txt files, extracting lines from corresponding page txt file
		linecnt=0
		for l in $(ls -1 $1/book/$b/*bin.png | sed -e 's/\.bin.png$//'); #only names, no extentions
			do
				linecnt=$(($linecnt+1))
				echo $l $linecnt $nsnippets $nlines $(sed -n "${linecnt}{p;q;}" $txt)
				$(sed -n "${linecnt}{p;q;}" $txt > $l.gt.txt) 
			done;

		cnt=$(($cnt+1))
	done;
