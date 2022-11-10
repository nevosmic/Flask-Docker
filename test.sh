#!/bin/bash
URL=localhost:5000
RES=`curl -s -I ${URL} | grep HTTP | awk {'print $2'}`
echo $RES
if [ $RES -eq 200 ]
then
        echo "OK !"
else
        echo "TEST NOT PASS"
        echo $RES
        exit 1
fi

