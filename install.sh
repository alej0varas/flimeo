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
FFMPEG_INSTALL_PATH=${FFMPEG_INSTALL_PATH-local/bin}
FFMPEG_BINARY_URL=${FFMPEG_BINARY_URL-http://ffmpeg.gusari.org/static/"$ARCH"bit/ffmpeg.static."$ARCH"bit.latest.tar.gz}
wget $FFMPEG_BINARY_URL --output-document=tmp/ffmpeg.tar.gz
tar -C tmp -xf tmp/ffmpeg.tar.gz
mkdir -p $FFMPEG_INSTALL_PATH
cp tmp/ffmpeg $FFMPEG_INSTALL_PATH

#
# Cleanup
#

rm -rf tmp
