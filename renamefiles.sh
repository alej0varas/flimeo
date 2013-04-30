TMPDIR="tmpdata"
mkdir -p $TMPDIR
rm -f $TMPDIR/*

inputfiles=$(find inputdata/ -name *.JPG | sort)

c=0
for file in $inputfiles
do
    # echo $file $TMPDIR/$c.JPG
    cp $file $TMPDIR/$c.JPG
    c=$(($c+1))
done
