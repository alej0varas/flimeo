#!/bin/bash

#
# Prepare
#

mkdir -p tmp

#
# Install ffmpeg
#

# Static Binary
ARCH=`getconf LONG_BIT`
# BINARY_URL=http://0.0.0.0:8000/ffmpeg-"$ARCH"bit.tar.gz
BINARY_URL=http://ffmpeg.gusari.org/static/"$ARCH"bit/ffmpeg.static."$ARCH"bit.latest.tar.gz
wget $BINARY_URL --output-document=tmp/ffmpeg.tar.gz
tar -C tmp -xf tmp/ffmpeg.tar.gz
mkdir -p local/bin
cp tmp/ffmpeg local/bin/

#
# Cleanup
#

rm -rf tmp
