from netmiko import ConnectHandler
from getpass import getpass
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
from paramiko.ssh_exception import AuthenticationException
import datetime
import time

TNOW = datetime.datetime.now().replace(microsecond=0)

password = getpass("Enter device password:")

	
with open('device_ips') as DEVICE_IP:

	for IP in DEVICE_IP:
			
		RTR = {
			'device_type': 'cisco_ios',
			'host': IP,
			'username': 'anwea',
			'password': password,
			'secret': password}

		print('######Connecting to the device ' + IP)
		try:
			net_connect = ConnectHandler(**RTR)
			net_connect.enable()
		except NetmikoTimeoutException:
			print('Device not reachable')
			continue
		except NetmikoAuthenticationException:
			print('Authentication Failed')
			continue
		except SSHException:
			print('Error reading SSH protocol banner')
			continue
		except AuthenticationException:
			print('Failed Authentication Exception')
			continue
		output = net_connect.send_config_from_file(config_file = 'config_command')
			
		print('\nsaving the configuration##########\n')
		output = net_connect.save_config()
		output = net_connect.send_command('sh run')
		time.sleep(2)
							
		print('Initializing backup...\n')
		time.sleep(2)

		backup = open('BACKUP_' + IP + '_' + str(TNOW), 'w')
		backup.write(output)
		backup.close
		print('Finished backup!\n')


