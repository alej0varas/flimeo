#!/bin/bash
# http://ffmpeg.org/trac/ffmpeg/wiki/UbuntuCompilationGuide


function wsudo {

sudo apt-get remove ffmpeg x264 libav-tools libvpx-dev libx264-dev yasm
sudo apt-get update
sudo apt-get -y install autoconf automake build-essential checkinstall git libass-dev libfaac-dev \
  libgpac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev librtmp-dev libspeex-dev \
  libtheora-dev libtool libvorbis-dev pkg-config texi2html zlib1g-dev 

# Yasm
# Yasm is an assembler and is recommended for x264 and FFmpeg.

cd
wget http://www.tortall.net/projects/yasm/releases/yasm-1.2.0.tar.gz
tar xzvf yasm-1.2.0.tar.gz
cd yasm-1.2.0
./configure
make
sudo checkinstall --pkgname=yasm --pkgversion="1.2.0" --backup=no \
  --deldoc=yes --fstrans=no --default

# uninstall dpkg -r yasm

# x264
# H.264 video encoder. The following commands will get the current source files, compile, and install x264. See the x264 Encoding Guide for some usage examples.

cd
git clone --depth 1 git://git.videolan.org/x264.git
cd x264
./configure --enable-static
make
sudo checkinstall --pkgname=x264 --pkgversion="3:$(./version.sh | \
  awk -F'[" ]' '/POINT/{print $4"+git"$5}')" --backup=no --deldoc=yes \
  --fstrans=no --default

# uninstall dpkg -r x264

# FFmpeg
# Note: Ubuntu Server users should remove --enable-x11grab from the following command:

# Note II: recent versions of ffmepg doesn't include librtmp, which is not mandatory 
# for timelapse. If compilation fails, try removing '--enable-librtmp' from the following command: 

sudo apt-get install -y libx264-dev 

cd
git clone --depth 1 git://source.ffmpeg.org/ffmpeg
cd ffmpeg
./configure --enable-gpl --enable-libass --enable-libfaac --enable-libmp3lame \
  --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libspeex \
  --enable-librtmp --enable-libtheora --enable-libvorbis --enable-libx264 \
  --enable-nonfree --enable-version3

make
sudo checkinstall --pkgname=ffmpeg --pkgversion="7:$(date +%Y%m%d%H%M)-git" --backup=no \
  --deldoc=yes --fstrans=no --default
hash -r

# uninstall dpkg -r ffmpeg

}


function nosudo {

apt-get remove ffmpeg x264 libav-tools libvpx-dev libx264-dev yasm
apt-get update
apt-get -y install autoconf automake build-essential checkinstall git libass-dev libfaac-dev \
  libgpac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev librtmp-dev libspeex-dev \
  libtheora-dev libtool libvorbis-dev pkg-config texi2html zlib1g-dev

cd
wget http://www.tortall.net/projects/yasm/releases/yasm-1.2.0.tar.gz
tar xzvf yasm-1.2.0.tar.gz
cd yasm-1.2.0
./configure
make
checkinstall --pkgname=yasm --pkgversion="1.2.0" --backup=no \
  --deldoc=yes --fstrans=no --default

# uninstall dpkg -r yasm

cd
git clone --depth 1 git://git.videolan.org/x264.git
cd x264
./configure --enable-static
make
checkinstall --pkgname=x264 --pkgversion="3:$(./version.sh | \
  awk -F'[" ]' '/POINT/{print $4"+git"$5}')" --backup=no --deldoc=yes \
  --fstrans=no --default

# uninstall dpkg -r x264

apt-get install -y libx264-dev 

cd
git clone --depth 1 git://source.ffmpeg.org/ffmpeg
cd ffmpeg
./configure --enable-gpl --enable-libass --enable-libfaac --enable-libmp3lame \
  --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libspeex \
  --enable-librtmp --enable-libtheora --enable-libvorbis --enable-libx264 \
  --enable-nonfree --enable-version3

make
checkinstall --pkgname=ffmpeg --pkgversion="7:$(date +%Y%m%d%H%M)-git" --backup=no \
  --deldoc=yes --fstrans=no --default
hash -r

# uninstall dpkg -r ffmpeg

}

SUDO=$1

set +x
if [ x$SUDO = x"sudo" ]
	then echo "wsudo"
	read a
	wsudo
elif which sudo > /dev/null
	then 
	echo "wich sudo"
	read a 
	wsudo
else 
	echo "nosudo"
	read a
	nosudo
fi
set -x
