#!/usr/bin/env python

import logging
import platform
import os
import sys
import tarfile
import tempfile
try:
  import urllib.request as urllib
except ImportError:
  import urllib


FAIL_TO_DOWNLOAD = 1


def cleanup(directory):
    """Removes temporary files created during install"""
    os.rmdir(directory)
    logging.debug("deleted: {}".format(directory))


def main():

    logging.basicConfig(level=logging.DEBUG)

    #
    # Prepare
    #

    # mkdir -p tmp
    download_directory = tempfile.mkdtemp()
    logging.debug("created: {}".format(download_directory))

    #
    # Install ffmpeg
    #

    # ARCH=`getconf LONG_BIT`
    architecture = platform.architecture()[0][0:2]
    logging.debug("architecture: {}".format(architecture))

    # OS=platform.system()

    #mkdir -p $FFMPEG_INSTALL_PATH
    FFMPEG_INSTALL_PATH = os.environ.get('FFMPEG_INSTALL_PATH', 'local/bin')
    logging.debug("ffmpeg install path: {}".format(FFMPEG_INSTALL_PATH))
    if os.path.isdir(FFMPEG_INSTALL_PATH):
      print('ffmpeg install path already exist {}'.format(FFMPEG_INSTALL_PATH))
      exit(1)
    os.makedirs(FFMPEG_INSTALL_PATH)
    logging.debug("created install path")

    #wget $FFMPEG_BINARY_URL --output-document=tmp/ffmpeg.tar.gz
    FFMPEG_BINARY_URL = os.environ.get('FFMPEG_BINARY_URL', 'http://ffmpeg.gusari.org/static/{0}bit/ffmpeg.static.{0}bit.latest.tar.gz'.format(architecture))
    logging.debug("ffmpeg binary url: {}".format(FFMPEG_BINARY_URL))
    try:
        local_filename, headers = urllib.urlretrieve(FFMPEG_BINARY_URL)
    except:
        sys.stdout.write('Failed to download ffmpeg\n')
        cleanup(download_directory)
        sys.exit(FAIL_TO_DOWNLOAD)

    logging.debug("local filename: {}:".format(local_filename))

    #tar -C tmp -xf tmp/ffmpeg.tar.gz
    content = tarfile.open(local_filename,'r')
    logging.debug("tarfile: {}".format(content))

    #cp tmp/ffmpeg $FFMPEG_INSTALL_PATH
    content.extract('ffmpeg', FFMPEG_INSTALL_PATH)
    content.close()
    urllib.urlcleanup()

    cleanup(download_directory)


if __name__ == "__main__":
    main()
