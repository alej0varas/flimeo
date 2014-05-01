#!/bin/bash
# flimeo.sh

echo "Hello, this is flimeo, the best time lapse generator *ever*"
if [[ $# -lt 2 ]]
  then echo "Usage: $0 <path> FPS <output path>"
  exit 0
fi

pathtopicts=$1
FPS=$2
#if [ "$3"x == x ]
# then outputpath="/tmp/inyourface"
#else
#outputpath=$3
#fi


pictnumber=$(find "$pathtopicts" -iname "*.JPG" -type f -print | wc -l)

function timelength {
duration=`expr $pictnumber / $FPS `
echo "estimated video duration: $duration s"
echo "is it ok? (y/N)"
read ans
if [ "$ans"x == 'x' ]
  then ans="n"
fi
}

timelength
while [ $ans == 'n' ]
  do echo "set new FPS value: "
  read FPS
  if [ "$FPS"x == 'x' ]
    then FPS=5
  fi 
  timelength
done


usage()
{
cat <<EOF
usage: $0 <path to images> <FPS> [output dir] 

This script creates a video.
EOF
}

# Check arguments
# Get options
FILE_FORMAT="mp4"
ORIGIN_PATH=$pathtopicts
OUTPUT_DIR=$(mktemp -d --tmpdir=.)
FRAME_RATE=$FPS
VIDEO_FILE_NAME=$(date +%s%N)
VERBOSE=1
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

# Copy original images to a input tmp dir
input_dir=$(mktemp -d --tmpdir=.)
#cp $verbose_option $ORIGIN_PATH* $input_dir/


# Rename pictures, workaround to ffmpeg bug
c=0
#for file in $inputfiles
for file in $(find $ORIGIN_PATH -iname "*.JPG" -type f -exec ls -1rt {} \;)
do
    #cp $verbose_option "$file" $tmp_dir/$c.JPG
    ln -s $verbose_option "$file" $tmp_dir/$c.JPG
    c=$(($c+1))
done

# Call the video creation tool
echo "Starting video encoding"

ffmpeg -loglevel $ffmpeg_verbose_option -r $FRAME_RATE -i $tmp_dir/%d.JPG -s hd1080 -vcodec libx264  -pix_fmt yuv420p $VIDEO_PATH

# Clean tmp files
#rm -rf $verbose_option $input_dir
rm -rf $verbose_option $tmp_dir

# return video output path
echo $VIDEO_PATH
