#!/usr/bin/env bash

usage()
{
cat <<EOF
usage: $0 -p <path to images> [options]

This script creates a video.

OPTIONS:
   -h      Show this message
   -p      Path to images
   -o      Specify a diferent output dir
   -t      Specify a diferent TMPDIR
   -f      Specify a frame rate
   -n      Specify video file name
   -v      Verbose
EOF
}

# Check arguments
# Get options
FILE_FORMAT="mp4"
ORIGIN_PATH=
OUTPUT_DIR=$(mktemp -d --tmpdir=.)
FRAME_RATE=30
VIDEO_FILE_NAME=$(date +%s%N)
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
    echo Path $ORIGIN_PATH doest not exist
    exit 1
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
tmp_dir=$(mktemp -d --tmpdir=.)

if [[ $VERBOSE == 1 ]]
then
    verbose_option="-v"
    ffmpeg_verbose_option="info"
else
    ffmpeg_verbose_option="quiet"
fi

# Get confirmation from user
echo "Origin path" $ORIGIN_PATH
echo "Output video" $VIDEO_PATH
echo "Temporary directory" $tmp_dir
echo "Frame rate" $FRAME_RATE
echo "Is it ok? (y/N)"
read ans
if [ "$ans" != 'y' ]
  then
  # needs function to createi/delete tmpdirs  here
    exit 0
fi

# Copy original images to a input tmp dir
input_dir=$(mktemp -d --tmpdir=.)
cp $verbose_option $ORIGIN_PATH* $input_dir/


inputfiles=$(find $input_dir -iname *.JPG -type f | sort)

# Rename pictures, workaround to ffmpeg bug
c=0
for file in $inputfiles
do
    cp $verbose_option "$file" $tmp_dir/$c.JPG
    c=$(($c+1))
done

# Call the video creation tool
echo "Starting video encoding"

ffmpeg -loglevel $ffmpeg_verbose_option -r $FRAME_RATE -i $tmp_dir/%d.JPG -s hd480 -vcodec libx264 $VIDEO_PATH

# Clean tmp files
rm -rf $verbose_option $input_dir
rm -rf $verbose_option $tmp_dir

# return video output path
echo $VIDEO_PATH
