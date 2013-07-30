#!/usr/bin/env bash

# Check arguments
# Must be called with a path
if [ "$1"x == x ]
then
    echo Must provide a path to the images
    exit 0
else
    origin=$1
fi

# Can specifie a diferent output dir
if [ "$2"x == x ]
 then
    output_dir=$(mktemp -d)
else
    output_dir=$2
fi

# Can specifie a diferent TMPDIR
if [ "$3" ]
 then
    export TMPDIR=$3
fi

# Can specifie a frame rate
if [ "$4"x == x ]
then
    frame_rate=30
else
    frame_rate=$4
fi

# Check origin path
if [ ! -e $origin ]
then
    echo Path doest not exist
    exit 0
fi

# Get tmpdir
tmp_dir=$(mktemp -d --tmpdir flimeo.XXXXXXXXXX)

mkdir -vp $tmp_dir

# Get output file name
video_path=$output_dir$(date +%s%N).mp4

# Get confirmation from user
echo "Temporary directory" $tmp_dir
echo "Output video" $video_path
echo "Frame rate" $frame_rate
echo "Is it ok? (y/N)"
read ans
if [ "$ans" != 'y' ]
  then
    exit 0
fi

# Copy original images to a input tmp dir
# mktemp -d $user-XXXXXXXXX --tmpdir
input_dir=$(mktemp -d)
# echo Copying files to $input_dir 
cp -v $origin* $input_dir/

inputfiles=$(find $input_dir -iname *.JPG -type f | sort)

# Rename pictures, workaround to ffmpeg bug
c=0
for file in $inputfiles
do
    # echo $file $TMPDIR/$c.JPG
    cp -v $file $tmp_dir/$c.JPG
    c=$(($c+1))
done

# Call the video creation tool
echo "starting video encoding"

ffmpeg -loglevel quiet -r $frame_rate -i $tmp_dir/%d.JPG -s hd480 -vcodec libx264 $video_path

# Clean tmp files
rm -rfv $input_dir
rm -rfv $tmp_dir

# return video output path
echo "$video_path"
