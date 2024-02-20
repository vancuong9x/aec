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


connection = ConnectHandler(**pbxdc)
connection.send_command_timing('cd /tmp')
connection.send_command_timing('rm -f /opt/backup_full_norecording.zip')
print(Fore.GREEN+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Start 3CX Backup.')
output = connection.send_command('sudo -u phonesystem /usr/sbin/3CXBackupCmd --file=/opt/backup_full_norecording.zip --options=FW,CH,FQDN,PROMPTS --log=/tmp/backup_full_norecording.log',max_loops=2000, delay_factor=20)
output=connection.send_command('sudo tail -n 100 /tmp/backup_full_norecording.log')
print(output)
if 'is succeeded' in output:
        print(Fore.GREEN+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' Backup full Successfully.')
else: 
        print(Fore.GREEN+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'Backup full fail fail fail fail fail fail fail.')

connection.disconnect()

