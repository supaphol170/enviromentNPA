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

        # Configure DHCP on G0/2 of R3
        if ip == '172.31.104.6':
            print("Configuring DHCP on R3")
            ssh.send("conf t\n")
            ssh.send("int g0/2\n")
            ssh.send("ip add dhcp\n")
            ssh.send("end\n")
            time.sleep(1)
            result = ssh.recv(2000).decode('ascii')

        
        # Configure OSPF on R1-R3 on Control/Data Plane (except G0/2 of R3)
        if ip in ['172.31.104.4','172.31.104.5','172.31.104.6']:
            print("Configuring OSPF on Routers")
            ssh.send("conf t\n")
            ssh.send("router ospf 1\n")
            time.sleep(1)
            result = ssh.recv(2000).decode('ascii')
            print(result)

            # OSPF network on R1
            if ip == "172.31.104.4":
                ssh.send("network 172.31.104.16 0.0.0.15 area 0\n")
                ssh.send("network 172.31.104.32 0.0.0.15 area 0\n")
                # Loopback on R1
                ssh.send("network 1.1.1.1 0.0.0.0 area 0\n")
                time.sleep(1)
                result = ssh.recv(2000).decode('ascii')
                print(result)
                print("Configure OSPF on R1 Done")
            # OSPF network on R2
            elif ip == "172.31.104.5":
                ssh.send("network 172.31.104.32 0.0.0.15 area 0\n")
                ssh.send("network 172.31.104.48 0.0.0.15 area 0\n")
                # Loopback on R2
                ssh.send("network 2.2.2.2 0.0.0.0 area 0\n")
                time.sleep(1)
                result = ssh.recv(2000).decode('ascii')
                print(result)
                print("Configure OSPF on R2 Done")
            # OSPF network on R3
            elif ip == "172.31.104.6":
                ssh.send("network 172.31.104.48 0.0.0.15 area 0\n")
                # Loopback on R3
                ssh.send("network 3.3.3.3 0.0.0.0 area 0\n")
                ssh.send("default-info originate\n")
                time.sleep(1)
                result = ssh.recv(2000).decode('ascii')
                print(result)
                print("Configure OSPF on R3 Done")
                ssh.send("exit\n")

                # Advertise a default route to the NAT cloud on R3 into the OSPF at R3
                print("Configuring R3 to advertise a deafult route")
                ssh.send("ip route 0.0.0.0 0.0.0.0 g0/2\n")
                ssh.send("do show ip route static\n")
                time.sleep(1)
                result = ssh.recv(2000).decode('ascii')
                print(result)
                print("Configure static default route Done")

                # Configure PAT on R3
                print("Configuring PAT on R3")



