from netmiko import ConnectHandler

device_ip = '172.31.104.4'
username = 'admin'
password = 'cisco'

device_params = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'password': password
}

commands = [
    "int lo0",
    "ip add 1.1.1.1 255.255.255.255",
    "no shut"
]

with ConnectHandler(**device_params) as ssh:
    result = ssh.send_config_set(commands)
    print(result)
