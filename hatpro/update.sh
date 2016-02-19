#!/bin/bash
# Author: Chuan Miao
# Date: 2016.2.19
#
# ./update.sh [-s campaign] [-t date]
#
# [date] in the format of 'yyyy-mm-dd'. If not specified, 
# the current date is used.


server='HEADS'
date=$(date +%Y-%m-%d)

while getopts s:t: opt; do
  case $opt in
    s)
      server=$OPTARG
      ;;
    t)
      date=$OPTARG
   esac
done


path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
arguments="server=${server}&date=${date}"

#hatpro_time
script="${path}/hatpro_time.cgi"
sensors='L2A.ATM.WAT.VAP.CNT L2A.ATM.LIQ.WAT.CNT L1B.BRIGHT.TEMP.IR L1B.BRIGHT.TEMP'
for s in $sensors; do
  arg="${arguments}&sensor=${s}"
  echo -n $arg | REQUEST_METHOD='POST' python $script
done

#hatpro_contour
script="${path}/hatpro_contour.cgi"
sensors='L2C.AIR.POT.TEM.PRF L2C.REL.HUM.PRF'
for s in $sensors; do
  arg="${arguments}&sensor=${s}"
  echo -n $arg | REQUEST_METHOD='POST' python $script
done

#script="${path}/hatpro_content.cgi"
#sensors='L2C.AIR.POT.TEM.PRF L2C.REL.HUM.PRF'
#for s in $sensors; do
#  arg="${arguments}&sensor=${s}"
#  echo -n $arg | REQUEST_METHOD='POST' python $script
#done

