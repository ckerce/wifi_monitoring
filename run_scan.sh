#!/bin/bash

N='NULL'
while (( "$#" )); do
  case "$1" in
    -n|--num_scans)
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        N=$2
        shift 2
	echo "Setting number of scans N=$N"
      else
	N=1000
	echo "Using default number of scans N=1000"
      fi
  esac
done

if [ 'NULL' == $N ] ; then
	N=1000
	echo "Using default number of scans N=1000"
fi



outfile='nmcli_scan.txt'
datfile='outdat.csv'
echo '' > $outfile
echo 'dat,ssid,val,,,' > $datfile


for i in $(seq 1 $N)
do
   echo Scan $i
   ts=$(date +%s)
   echo time_scan_start $(date +%s)  >> $outfile
   nmcli dev wifi list --rescan yes  >> $outfile
   echo scan_$i,--,$ts,,, >> $datfile
   nmcli -f BSSID,SSID,SIGNAL dev wifi list ifname wlx5ca6e6a78898 | grep -v BSSID | sed -e 's/[^\ ]\ [^\ ]/_/g' -e 's/\ \ /\ /g' -e 's/\ /,/g' >> $datfile
   echo time_scan_end $(date +%s)    >> $outfile
done

#cat $datfile | sed -e 's/,,,//g' >> mod_$datfile
num=$(ls -lahtr working*.csv | wc -l)
workingfile=working_$num.csv
cat $datfile | sed -e 's/,,,/,/g' -e 's/,,,/,/g' -e 's/,,/,/g' -e 's/,,/,/g' -e 's/,$//g' -e 's/_,/_/g' > $workingfile
