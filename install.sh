#!/bin/bash

#
# Prepare
#

mkdir -p tmp

#
# Install ffmpeg
#

# Static Binary
# BINARY_URL=http://0.0.0.0/ffmpeg.tar.gz
BINARY_URL=http://ffmpeg.gusari.org/static/64bit/ffmpeg.static.64bit.latest.tar.gz
wget $BINARY_URL --output-document=tmp/ffmpeg.tar.gz
tar -C tmp -xf tmp/ffmpeg.tar.gz
mkdir -p local/bin
cp tmp/ffmpeg local/bin/

#
# Cleanup
#

rm -rf tmp
