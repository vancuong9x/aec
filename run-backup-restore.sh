#!/bin/bash
echo "-------------------------------------------------------------------" >>  /home/backup-restored-scb/backup.log 
/usr/bin/python3 /home/backup-restored-scb/backup.py >>  /home/backup-restored-scb/backup.log
sleep 3
echo "-------------------------------------------------------------------" >>  /home/backup-restored-scb/restore.log
/usr/bin/python3 /home/backup-restored-scb/restore.py >> /home/backup-restored-scb/restore.log



