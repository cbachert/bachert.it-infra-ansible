#!/bin/sh
echo "Setting hard drive idle time to 15 minutes"
sudo hdparm -S 180 /dev/sda
echo "Opening crypto device"
sudo cryptsetup luksOpen /dev/disk/by-uuid/907b24fe-4524-41d1-8b13-dd912f308146 BACKUPPC-PV0
sleep 5
echo "Activating volume groups"
sudo vgchange -a y
sleep 5
echo "Mounting backup file system"
sudo mount -o defaults,noatime,errors=remount-ro /dev/mapper/BACKUPPC--VG-BACKUPPC--LV--DATA /var/lib/backuppc
#echo "Mounting swap file system"
#sudo swapon /dev/BACKUPPC-VG/BACKUPPC-LV-SWAP
echo "Start backuppc"
#sudo systemctl start backuppc
sudo docker start backuppc