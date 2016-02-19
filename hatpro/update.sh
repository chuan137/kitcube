#!/bin/bash

server='HEADS'

if [ -n "$1" ]; then
  date=$1
else
  date=$(date +%Y-%m-%d)
fi

path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
arguments="server=${server}&date=${date}"

echo $path

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

