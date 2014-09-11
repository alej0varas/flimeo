#!/usr/bin/env python

##
## Here we start porting everything to python
##

import argparse
parser = argparse.ArgumentParser(description='Flimeo, the best timelapse generator *ever*')
parser.add_argument('--source', help="set the source files type (jpeg, raw", choices=['jpeg','raw'])
parser.add_argument('--path', help="path to source files", dest="path")
parser.add_argument('--FPS', help="frames per second of the video", type=int, dest="fps", default=25)
parser.add_argument('--quality', help="output video quality low|med|hig", type=str, dest="videoq", default="med")


import PIL
import glob
import os
import sys

args= parser.parse_args()
#print(args.source)

ext=args.source
if ext == 'raw':
  ext = ['*.RAW', '*.raw']
elif ext == 'jpeg':
  ext = ['*.jpg', '*.JPG'] 
else:
  parser.print_help()
  sys.exit(0)

fps = args.fps
for i in ext:
  path= os.getcwd() + "/sample_picts/" + i 
  #print(path)
  a = glob.glob(path)
  a.sort()
  if a != []:
    #print(a)
    pictlist = a
    #print pictlist
    pictnum = len(pictlist)
    timelapseduration = pictnum / fps
    print("frames: %s, frames per second: %d,\ntime-lapse duration: %s" %(pictnum,fps,timelapseduration))
    ## TODO
    ## add yes/no loop 
    ans = raw_input("Is it ok? (y/N)")
    if ans == "y":
      print("doing it")
      #call ffmpeg and so on
    else:
      print("set new fps value")

#case $3 in
#	low)
#	quality=hd480
#	;;
#	med)
#	quality=hd720
#	;;
#	hig)
#	quality=hd1080
#	;;
#	*)
#	quality=hd480
#esac 
#
#
#pictnumber=$(find "$pathtopicts" -iname "*.JPG" -type f -print | wc -l)
#
#function timelength {
#duration=`expr $pictnumber / $FPS `
#echo "estimated video duration: $duration s"
#echo "is it ok? (y/N)"
#read ans
#if [ "$ans"x == 'x' ]
#  then ans="n"
#fi
#}
#
#timelength
#while [ $ans == 'n' ]
#  do echo "set new FPS value: "
#  read FPS
#  if [ "$FPS"x == 'x' ]
#    then FPS=5
#  fi 
#  timelength
#done
#
#
#
## Check arguments
## Get options
#FILE_FORMAT="mp4"
#ORIGIN_PATH=$pathtopicts
#OUTPUT_DIR=$(mktemp -d --tmpdir=.)
#FRAME_RATE=$FPS
#VIDEO_FILE_NAME=$(date +%s%N)
#VERBOSE=1
## Must be called with a path
#if [[ -z $ORIGIN_PATH ]]
#then
#     usage
#     exit 1
#fi
#
## Check origin path
#if [ ! -e $ORIGIN_PATH ]
#then
#    echo Path $ORIGIN_PATH doest not exist
#    exit 1
#fi
#
## Check video file name does't exist
#VIDEO_PATH=$OUTPUT_DIR/$VIDEO_FILE_NAME.$FILE_FORMAT
#count=1
#while [ -e $VIDEO_PATH ]
#do
#    VIDEO_PATH=$OUTPUT_DIR/"$VIDEO_FILE_NAME"_"$count"_.$FILE_FORMAT
#    count=$((count+1))
#done
#
## Get and create tmpdir
#tmp_dir=$(mktemp -d --tmpdir=.)
#
#if [[ $VERBOSE == 1 ]]
#then
#    verbose_option="-v"
#    ffmpeg_verbose_option="info"
#else
#    ffmpeg_verbose_option="quiet"
#fi
#
## Copy original images to a input tmp dir
#input_dir=$(mktemp -d --tmpdir=.)
##cp $verbose_option $ORIGIN_PATH* $input_dir/
#
#
## Rename pictures, workaround to ffmpeg bug
#c=0
##for file in $inputfiles
#for file in $(find $ORIGIN_PATH -iname "*.JPG" -type f -exec ls -1rt {} \; | sort)
#do
#    #cp $verbose_option "$file" $tmp_dir/$c.JPG
#    ln -s $verbose_option "$file" $tmp_dir/$c.JPG
#    c=$(($c+1))
#done
#
## Call the video creation tool
#echo "Starting video encoding"
#
#ffmpeg -loglevel $ffmpeg_verbose_option -r $FRAME_RATE -i $tmp_dir/%d.JPG -s $quality -vcodec libx264  $VIDEO_PATH
##ffmpeg -loglevel $ffmpeg_verbose_option -r $FRAME_RATE -i $tmp_dir/%d.JPG -s $quality -vcodec libx264  -pix_fmt yuv420p $VIDEO_PATH
#
## Clean tmp files
##rm -rf $verbose_option $input_dir
#rm -rf $verbose_option $tmp_dir
#
## return video output path
#echo $VIDEO_PATH
#du -h $VIDEO_PATH
