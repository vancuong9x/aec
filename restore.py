from netmiko import ConnectHandler
import colorama
from colorama import Fore
import logging
import datetime
import paramiko
import time
import datetime
from threading import Thread
import configparser
import requests
config = configparser.ConfigParser()
config.read(r'/home/backup-restored-scb/varscb.ini')

devices=config.sections()

ip3cxdc=config.get('scb','ip3cxdc')
ip3cxdr=config.get('scb','ip3cxdr')
iphealthcheck=config.get('scb','iphealthcheck')
userlogin3cxdc=config.get('scb','userlogin3cxdc')
passlogin3cxdc=config.get('scb','passlogin3cxdc')
userlogin3cxdr=config.get('scb','userlogin3cxdr')
passlogin3cxdr=config.get('scb','passlogin3cxdr')
userloginhc=config.get('scb','userloginhc')
passloginhc=config.get('scb','passloginhc')
#backup 3cx

logging.basicConfig(filename='netmiko.log', level=logging.DEBUG)
logger = logging.getLogger('netmiko')



pbxdc = {
        'device_type': 'linux',
        'ip': ip3cxdc,
        'username': userlogin3cxdc,
        'password': passlogin3cxdc,
        'port': 22,
        'secret': passlogin3cxdc,         # 3cxdc
        'verbose':True

        }


pbxdr = {
        'device_type': 'linux',
        'ip': ip3cxdr,
        'username': userlogin3cxdr,
        'password': passlogin3cxdr,
        'port': 22,
        'secret': passlogin3cxdr,         # 3cxdr
        'verbose':True
        }


#rsync files backup full no recording
ssh_client = paramiko.SSHClient()

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(ip3cxdc, port=22, username=userlogin3cxdc, password=passlogin3cxdc, look_for_keys=False, allow_agent=False)


stdin, stdout, stderr = ssh_client.exec_command('sudo rsync -auv -e ssh --progress --rsync-path="sudo rsync" /opt/backup_full_norecording.zip '+userlogin3cxdr+'@'+ip3cxdr+':/opt/', get_pty=True)
time.sleep(3)
stdin.write(passlogin3cxdr+'\n')

output = stdout.read().decode()
print(output)


ssh_client.close()


#restore

connection = ConnectHandler(**pbxdr)

# Will execute 'sudo su' (will pass the secret as the password for the sudo)
print(Fore.GREEN+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Start 3CX Restore.')
connection.send_command('set length 0')
connection.send_command_timing('cd /tmp')
output = connection.send_command('sudo -u phonesystem /usr/sbin/3CXRestoreCmd --file=/opt/backup_full_norecording.zip --log=/tmp/restore.log',max_loops=2000, delay_factor=20)

output=connection.send_command('sudo tail -n 50 /tmp/restore.log')
print(output)

if 'Reindexing' in output:
        print(Fore.GREEN+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Restore Successfully.')
else:   
        print(Fore.GREEN+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Restore fail fail fail fail fail fail.')
print("---------------------------------------------------------------------------------------------------------------")

connection.disconnect()

