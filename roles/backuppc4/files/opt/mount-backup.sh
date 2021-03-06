#!/bin/sh
echo "Setting hard drive idle time to 15 minutes"
sudo hdparm -S 180 /dev/sda
echo "Opening crypto device"
sudo cryptsetup luksOpen /dev/disk/by-uuid/1ae70e66-8cf1-45a1-827a-d99b02b5fa02 BACKUPPC-PV0
sleep 5
echo "Activating volume groups"
sudo vgchange -a y
sleep 5
echo "Mounting backup file system"
sudo mount /dev/mapper/BACKUPPC--VG-BACKUPPC--LV--DATA /var/lib/backuppc
#echo "Mounting swap file system"
#sudo swapon /dev/BACKUPPC-VG/BACKUPPC-LV-SWAP
echo "Start backuppc"
#sudo systemctl start backuppc
sudo docker start backuppc