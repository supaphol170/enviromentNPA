from netmiko import ConnectHandler

device_ip = '172.31.104.4'
username = 'admin'
password = 'cisco'

device_params = {'device_type': 'cisco_ios',
                'ip': device_ip,
                'username': username,
                'password': password
}

with ConnectHandler(**device_params) as ssh:
    result = ssh.send_command('show ip int b')
    print(result)
    result = ssh.send_command('show cdp nei')
    print(result)
    result = ssh.send_command('show int desc')
    print(result)
