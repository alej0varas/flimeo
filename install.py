#!/bin/env python

# #
# # Cleanup
# #

# rm -rf tmp
def main():
    import logging
    import platform
    import os
    import tarfile
    import tempfile
    import urllib.request

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
    os.makedirs(FFMPEG_INSTALL_PATH, exist_ok=True)
    logging.debug("created install path")

    #wget $FFMPEG_BINARY_URL --output-document=tmp/ffmpeg.tar.gz
    FFMPEG_BINARY_URL = os.environ.get('FFMPEG_BINARY_URL', 'http://ffmpeg.gusari.org/static/{0}bit/ffmpeg.static.{0}bit.latest.tar.gz'.format(architecture))
    logging.debug("ffmpeg binary url: {}".format(FFMPEG_BINARY_URL))
    local_filename, headers = urllib.request.urlretrieve(FFMPEG_BINARY_URL)
    logging.debug("local filename: {}:".format(local_filename))

    #tar -C tmp -xf tmp/ffmpeg.tar.gz
    content = tarfile.open(local_filename,'r')
    logging.debug("tarfile: {}".format(content))

    #cp tmp/ffmpeg $FFMPEG_INSTALL_PATH
    content.extract('ffmpeg', FFMPEG_INSTALL_PATH)
    content.close()
    urllib.request.urlcleanup()

    #
    # Cleanup
    #

    # rm -rf tmp
    os.rmdir(download_directory)
    logging.debug("deleted: {}".format(download_directory))

if __name__ == "__main__":
    main()
