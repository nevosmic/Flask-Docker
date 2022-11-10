#!/bin/bash

VAR1=$1
VAR2="test"

if [ "$VAR1" = "$VAR2" ]; then
    echo "Strings are equal."
else
    echo "Strings are not equal."
fi
