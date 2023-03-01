import getpass
import telnetlib
import time

host = "172.31.104.4"
user = input("Enter username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(host, 23, 5)

tn.read_until(b"Username:")
tn.write(user.encode('ascii') + b"\n")
time.sleep(1)

tn.read_until(b"Password:")
tn.write(password.encode('ascii') + b"\n")
time.sleep(1)

tn.write(b"conf t\n")
time.sleep(1)
tn.write(b"int g0/1\n")
time.sleep(1)
tn.write(b"ip add 172.31.104.17 255.255.255.240\n")
time.sleep(1)
tn.write(b"no shut\n")
time.sleep(1)
tn.write(b"exit\n")
time.sleep(1)

output = tn.read_very_eager()
print(output.decode('ascii'))

tn.close()
