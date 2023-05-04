from netmiko import ConnectionHandler
def get_data_from_device(device_params):
    with ConnectionHandler(**device_params) as ssh:
        result_shipintbr = ssh.send_command("show ip int b")
        return result_shipintbr

def get_ip(device_params, intf):
    data = get_data_from_device(device_params)
    result = data.strip().split('\n')
    for line in result[1:]:
        words = line.split()
        if words[0][0] == intf[0] and words[0][-3:] == intf[1:]:
            return words[1]

if __name__ == "__main__":
    device_ip = "172.31.104.4"
    username = "admin"
    password = "cisco"

    device_params = {
        "device_type": "cisco_ios",
        "username": username,
        "password": password
    }

    print(get_ip(device_params, "G0/0"))
