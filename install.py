#!/usr/bin/env python

'''This is the installer script.
It can download a static 32/64bit linux binary or build ffmpeg from source'''

### TODO

# uname
import platform

ARCH=platform.architecture()[0]
OS=platform.system()


# download
if OS == 'Linux':
  if ARCH == '32bit':
    print("downloading ffmpeg for Linux 32bit")
    BINARY_URL="http://ffmpeg.gusari.org/static/32bit/ffmpeg.static.32bit.latest.tar.gz"
  elif ARCH == '64bit':
    print("downloading ffmpeg for Linux 64bit")
    BINARY_URL="http://ffmpeg.gusari.org/static/64bit/ffmpeg.static.64bit.latest.tar.gz"
  #TODO
  # handle errors
  # http://stackoverflow.com/questions/4028697/how-do-i-download-a-zip-file-in-python-using-urllib2

  import urllib2
  data = urllib2.urlopen(BINARY_URL)
  dl = open('/tmp/toto.tar.gz','wb')
  dl.write(data.read())
  dl.close()
else:
  print("Unable to provide static binary, please build ffmpeg for sources")

# create ~/flimeo/local/bin

# install ffmpeg (built or downloaded)


# clean install traces
import os
os.remove('/tmp/toto.tar.gz')


# create .config file
#example
# lets create that config file for next time...
#cfgfile = open("c:\\next.ini",'w')
# add the settings to the structure of the file, and lets write it out...
#Config.add_section('Person')
#Config.set('Person','HasEyes',True)
#Config.set('Person','Age', 50)
#Config.write(cfgfile)
#cfgfile.close()

#read file
#import ConfigParser
#Config = ConfigParser.ConfigParser()
#Config.read("c:\\tomorrow.ini")
#Config.sections()
