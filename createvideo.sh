#!/usr/bin/env bash

usage()
{
cat <<EOF
usage: $0 -p <path to images> [options]

This script run creates a video.

OPTIONS:
   -h      Show this message
   -p      Path to images
   -o      Specifie a diferent output dir
   -t      Specifie a diferent TMPDIR
   -f      Specifie a frame rate
   -n      Specifie video file name
   -v      Verbose
EOF
}

# Check arguments
# Get options
FILE_FORMAT="mp4"
ORIGIN_PATH=
OUTPUT_DIR=$(mktemp -d)
FRAME_RATE=30
VIDEO_FILE_NAME=$(date +%s%N).mp4
VERBOSE=
while getopts “hp:o:t:f:n:v” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         p)
             ORIGIN_PATH=$OPTARG
             ;;
         o)
             OUTPUT_DIR=$OPTARG
             ;;
         t)
             export TMPDIR=$OPTARG
             ;;
         f)
             FRAME_RATE=$OPTARG
             ;;
         n)
             VIDEO_FILE_NAME=$OPTARG
             ;;
         v)
             VERBOSE=1
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

# Must be called with a path
if [[ -z $ORIGIN_PATH ]]
then
     usage
     exit 1
fi

# Check origin path
if [ ! -e $ORIGIN_PATH ]
then
    echo Path doest not exist
    exit 0
fi

# Check video file name does't exist
VIDEO_PATH=$OUTPUT_DIR/$VIDEO_FILE_NAME.$FILE_FORMAT
count=1
while [ -e $VIDEO_PATH ]
do
    VIDEO_PATH=$OUTPUT_DIR/"$VIDEO_FILE_NAME"_"$count"_.$FILE_FORMAT
    count=$((count+1))
done

# Get and create tmpdir
tmp_dir=$(mktemp -d --tmpdir flimeo.XXXXXXXXXX)

# Get confirmation from user
echo "Origin path" $ORIGIN_PATH
echo "Temporary directory" $tmp_dir
echo "Output video" $VIDEO_PATH
echo "Frame rate" $FRAME_RATE
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
cp -v $ORIGIN_PATH* $input_dir/

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

echo ffmpeg -loglevel quiet -r $FRAME_RATE -i $tmp_dir/%d.JPG -s hd480 -vcodec libx264 $VIDEO_PATH

ffmpeg -loglevel quiet -r $FRAME_RATE -i $tmp_dir/%d.JPG -s hd480 -vcodec libx264 $VIDEO_PATH

# Clean tmp files
rm -rfv $input_dir
rm -rfv $tmp_dir

# return video output path
echo $VIDEO_PATH
