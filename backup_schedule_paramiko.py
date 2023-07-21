import paramiko
import time
import datetime
import schedule
import getpass


username = getpass('Enter device Username: ')
password = getpass('Enter device password: ')

def BACKUP():
	TNOW = datetime.datetime.now().replace(microsecond=0)
	DEVICE_IP = open('device_ips'):
	for IP in DEVICE_IP:
		ssh_session = paramikoSSHClient()
		ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_session.connect(IP,port=22,
				    username=username,
				    password=password,
				    allow_agent=False,
				    look_for_keys=False)

		ACCESS_DEVICE = ssh_session.invoke_shell()
		ACCESS_DEVICE.send('enable\n')
		ACCESS_DEVICE.send('02anwe05\n')
		ACCESS_DEVICE.send(b'config t\n')
		ACCESS_DEVICE.send(b'terminal len 0\n')
		ACCESS_DEVICE.send(b'vlan 100\n')
		ACCESS_DEVICE.send(b'name Test_Vlan\n')
		ACCESS_DEVICE.send(b'sh run\n')
		
		time.sleep(2)
		output = ACCESS_DEVICE.recv(65000)

		print(output.decode('ascii'))
		
		SAVE_FILE = open('ROUTER_' + IP + str(TNOW), 'w')
		SAVE_FILE.write(output.decode('ascii'))
		SAVE_FILE.close

		ssh_session.close

schedule.every(1).minutes.do(BACKUP)

while True:
    schedule.run_pending()
    time.sleep(1)
