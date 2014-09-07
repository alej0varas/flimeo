#!/bin/bash

#
# Prepare
#

mkdir -p tmp

#
# Check arch
#

ARCH=`uname -m`

#
# Install ffmpeg
#

# Static Binary
# BINARY_URL=http://0.0.0.0/ffmpeg.tar.gz

####
###  FIX THIS WITH UNAME
####

if [ "$ARCH" = "i686" ]
  then BINARY_URL=http://ffmpeg.gusari.org/static/32bit/ffmpeg.static.32bit.latest.tar.gz
elif [ "$ARCH" = "x86_64" ]
  then BINARY_URL=http://ffmpeg.gusari.org/static/64bit/ffmpeg.static.64bit.latest.tar.gz
fi

wget $BINARY_URL --output-document=tmp/ffmpeg.tar.gz
tar -C tmp -xf tmp/ffmpeg.tar.gz
mkdir -p local/bin
cp tmp/ffmpeg local/bin/

#
# Cleanup
#

rm -rf tmp
