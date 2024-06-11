#!/bin/bash


myrand=$(awk -v min=0 -v max=5 'BEGIN{srand(); print min+rand()*(max-min+1)}')

sleep $myrand


printf "Content-type: text/html\n\n"
printf "Hello World!\n"
printf "Delayed for $myrand seconds\n"
