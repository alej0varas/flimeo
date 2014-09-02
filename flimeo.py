#!/usr/bin/env python

##
## Here we start porting everything to python
##

import argparse
parser = argparse.ArgumentParser(description='Flimeo, the best timelapse generator *ever*')
parser.add_argument('--jpg', dest='ext')


import PIL
import glob
import os



ext=''
jpgext = ['*.jpg', '*.JPG'] 
rawext = ['*.RAW', '*.raw']
for i in jpgext:
  path= os.getcwd() + "/sample_picts/" + i 
  print(path)
  a = glob.glob(path)
  a.sort()
  print(a)


#!/bin/bash
# flimeo.sh

#usage()
#{
#cat <<EOF
#
#Usage: $0 <path> <FPS> <low|med|hig> <raw|jpeg> [output path]
#This script creates a time lapse video.
#EOF
#}
#
#echo "Hello, this is flimeo, the best time lapse generator *ever*"
#if [[ $# -lt 2 ]]
#  #then echo "Usage: $0 <path> <FPS> <low|med|hig> [output path]"
#  then usage
#  exit 0
#fi
#
#pathtopicts=$1
#FPS=$2
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
#case $4 in 
#	jpeg)
#	pformat=JPG
#	;;
#	raw)
#	pformat=DNG
#	find "$pathtopicts" -iname "*.$pformat" -type f -exec convert -verbose {} {}.jpg \;
#	;;
#	*)
#	usage
#esac
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
