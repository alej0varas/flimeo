#!/usr/bin/env bash

# check arguments, must be called with a path
if [ $@ ]
then
    origin=$@
else
    echo Must provide a path to the images without trailing slash
    exit 0
fi

# import pictures from path
if [ ! -e $origin ]
then
    echo Path doest not exist
    exit 0
fi

# mktemp -d $user-XXXXXXXXX --tmpdir
input_dir=$(mktemp -d)
# echo Copying files to $input_dir 
cp -v $origin/* $input_dir/

# rename pictures, workaround to ffmpeg bug
tmp_dir=$(mktemp -d)
# echo Renaming files to $tmp_dir 
mkdir -vp $tmp_dir

inputfiles=$(find $input_dir -iname *.JPG -type f | sort)

c=0
for file in $inputfiles
do
    # echo $file $TMPDIR/$c.JPG
    cp -v $file $tmp_dir/$c.JPG
    c=$(($c+1))
done

output_dir=$(mktemp -d)

video_path=$output_dir/$(date +%s%N).mp4

# call the video creation tool
echo "starting video encoding"

ffmpeg -loglevel quiet -r 15 -i $tmp_dir/%d.JPG -s hd480 -vcodec libx264 $video_path

# clean tmp files
rm -rfv $input_dir
rm -rfv $tmp_dir

# return video output path
echo "$video_path"
