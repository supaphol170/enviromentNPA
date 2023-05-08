from netmiko import ConnectHandler
def get_data_from_device(device_params):
    with ConnectHandler(**device_params) as ssh:
        result_shipintbr = ssh.send_command("show cdp nei")
        return result_shipintbr

def get_ip(device_params, intf):
    data = get_data_from_device(device_params)
    result = data.strip().split('\n')
    for line in result[1:]:
        words = line.split()
        if words[0][0] == intf[0] and words[0][-3:] == intf[1:]:
            return words[1]

def get_int(device_params):
    int_lst = []
    data = get_data_from_device(device_params)
    result = data.strip().split('\n')
    for line in result[5:-2]:
        words = line.split()
        int_lst.append([words[0].split('.')[0], str(words[1] + words[2]), str(words[-2] + words[-1])])
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

        interfaces = get_int(device_params)
        conf_desc(device_params, interfaces)
