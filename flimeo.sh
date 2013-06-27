#!/bin/bash
# flimeo.sh

echo "Hello, this is flimeo, the best time lapse generator *ever*"
if [[ $# -lt 2 ]]
  then echo "Usage: $0 <path> FPS <output path>"
  exit 0
fi

pathtopicts=$1
FPS=$2
if [ "$3"x == x ]
 then outputpath="/tmp/inyourface"
else
outputpath=$3
fi
generator="test.sh"


pictnumber=$(find "$pathtopicts" -iname "*.JPG" -type f -print | wc -l)

function timelength {
duration=`expr $pictnumber / $FPS `
echo "estimated video duration: $duration s"
echo "is it ok? (y/N)"
read ans
if [ "$ans"x == 'x' ]
  then ans="n"
fi
}

timelength
while [ $ans == 'n' ]
  do echo "set new FPS value: "
  read FPS
  if [ "$FPS"x == 'x' ]
    then FPS=5
  fi 
  timelength
done


bash $generator $pathtopicts $FPS $outputpath $outputname
