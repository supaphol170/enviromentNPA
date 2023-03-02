import time
import paramiko

username = 'admin'
password = 'cisco'

devices_ip = ['172.31.104.1', '172.31.104.2', '172.31.104.3', '172.31.104.4', '172.31.104.5', '172.31.104.6']

for ip in devices_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=username, password=password, look_for_keys=False, disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})
    print(f"Connecting to {ip}")
    with client.invoke_shell() as ssh:
        print(f"Connected to {ip}")

        ssh.send("terminal length 0\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("show ip int b\n")
        time.sleep(1)
        result = ssh.recv(2000).decode('ascii')
        print(result)
