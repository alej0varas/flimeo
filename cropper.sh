c=0 

for file in $(find /media/usb0/DCIM/ -iname "*.JPG" -type f -exec ls -1rt {} \; | sort)
 do convert -verbose -crop 927x674+868+680 "$file" $c.JPG
 #do echo "$file $c"
 echo "$file $c"
 c=$(($c+1))

done

