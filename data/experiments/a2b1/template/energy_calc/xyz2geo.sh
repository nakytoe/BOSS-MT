#!/bin/bash
#
# Milica Todorovic (2015)
# Bash script to convert xyz into geometry.in (no PBC) 
# Use: ./Zconstrain.sh < filename.in 
#
# (handles comments/empty spaces)

# loop through all lines:
while read line

do
# repeat each line
#echo "$line"

# read in each field field
element=$(awk '{print $1}' <<<"$line")
xcoo=$(awk '{print $2}' <<<"$line")
ycoo=$(awk '{print $3}' <<<"$line")
zcoo=$(awk '{print $4}' <<<"$line")

# output all  
echo "atom " $xcoo $ycoo $zcoo $element 

done  


