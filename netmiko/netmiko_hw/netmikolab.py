import re
from netmiko import ConnectHandler

def get_data_from_device(device_params, cmd: str):
    with ConnectHandler(**device_params) as ssh:
        result_shipintbr = ssh.send_command(cmd)
        return result_shipintbr

def get_ip(device_params):
    int_dict = {}
    data = get_data_from_device(device_params, "show ip int b")
    result = data.strip().split('\n')
    for line in result[1:]:
        match = re.search("(\w)+.*((\w)+ | (\d{1,3}\.){3}(\d{1,3}))", line).group().split()
        int_dict[match[0]] = match[1]
    return int_dict

def get_int(device_params):
    int_lst = []
    data = get_data_from_device(device_params)
    result = data.strip().split('\n')
    for line in result[5:-2]:
        dev = re.search("^(\w\d)", line)
        match = re.search("(\w)+ (\d+/\d+).*(\w)+ (\d+/\d+)", line).group().split()
        local, remote = str(match[0] + match[1]), str(match[-2] + match[-1])
        int_lst.append([local,remote])
    return int_lst

def conf_desc(device_params, int_lst: list):
    with ConnectHandler(**device_params) as ssh:
        for int in int_lst:
            desc = f"Connect to {int[-1]} of {int[0]}"
            cmd = [f"int {int[1]}", f"desc {desc}", "end"]
            result = ssh.send_config_set(cmd)
            print(result)

if __name__ == "__main__":
    device_ip = ["172.31.104.4", "172.31.104.5", "172.31.104.6"]
    username = "admin"
    password = "cisco"

    for ip in device_ip:
        device_params = {
            "ip": ip,
            "device_type": "cisco_ios",
            "username": username,
            "password": password
        }
        #interfaces = get_int(device_params)
        #conf_desc(device_params, interfaces)
    print(get_ip(device_params))
