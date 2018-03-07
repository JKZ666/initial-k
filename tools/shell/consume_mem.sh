#!/bin/sh
# cousumer 1024M memory for 1 hour, need root authority
mkdir /tmp/memory
mount -t tmpfs -o size=1024M tmpfs /tmp/memory
dd if=/dev/zero of=/tmp/memory/block
sleep 3600
rm /tmp/memory/block
umount /tmp/memory
rmdir /tmp/memory
