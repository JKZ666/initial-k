#!/bin/sh
# consume all cpu
for i in `seq 1 $(cat /proc/cpuinfo |grep "physical id" |wc -l)`;do dd if=/dev/zero of=/dev/null & done

# free
# pkill dd
