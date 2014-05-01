TMPDIR="tmpdata"
mkdir -p $TMPDIR
rm -f $TMPDIR/*

inputfiles=$(find inputdata/ -name *.JPG | sort)
#   7 inputfiles=$(find /media/Gopro/DCIM -type f -iname "*.jpg" -exec ls -1rt {} \;)


c=0
for file in $inputfiles
do
    # echo $file $TMPDIR/$c.JPG
    cp $file $TMPDIR/$c.JPG
    c=$(($c+1))
done
