#!/bin/bash

#bssid=$1

#nmcli dev wifi list bssid $bssid

outfile='nmcli_scan3.txt'
datfile='outdat3.csv'
echo '' > $outfile
echo 'dat,ssid,val,,,' > $datfile


for i in $(seq 1 1000)
do
   echo Scan $i
   ts=$(date +%s)
   echo time_scan_start $(date +%s)  >> $outfile
   nmcli dev wifi list --rescan yes  >> $outfile
   echo scan_$i,--,$ts,,, >> $datfile
   nmcli -f BSSID,SSID,SIGNAL dev wifi list | grep -v BSSID | sed -e 's/[^\ ]\ [^\ ]/_/g' -e 's/\ \ /\ /g' -e 's/\ /,/g' >> $datfile
   echo time_scan_end $(date +%s)    >> $outfile
done

cat $datfile | sed -e 's/,,,//g' >> mod_$datfile