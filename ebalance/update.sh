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
script="${path}/time_serie.cgi"
sensors='PYG_T_BOT_AVG'
for s in $sensors; do
  arg="${arguments}&sensor=${s}"
  echo $arg
  echo -n $arg | REQUEST_METHOD='POST' python $script
done
