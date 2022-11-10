#!/bin/bash
URL=localhost:5000
RESULT=`curl -s -I ${URL} | grep HTTP | awk {'print $2'}`
echo $RESULT
if [ $RESULT -eq 200 ]
then
	echo " OK !"
else
	echo "TEST NOT PASS !"
	exit 1
fi
