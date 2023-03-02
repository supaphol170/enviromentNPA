import time
import paramiko

USERNAME = 'admin'
PASSWORD = 'cisco'

devices_ip = ['172.31.104.4', '172.31.104.5', '172.31.104.6']

for ip in devices_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=USERNAME, password=PASSWORD, look_for_keys=False, disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})

    commands = ["show ip int b"]
    for command in commands:
        print(f"Excuting {command}")
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        print("Errors")
        print(stderr.read().decode())
        time.sleep(1)
    client.close()
