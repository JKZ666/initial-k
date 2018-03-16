#!/bin/sh
for ((;;));
do
cat /proc/${1}/status |grep VmRSS;
sleep 5;
done
