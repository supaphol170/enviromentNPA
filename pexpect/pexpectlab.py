import pexpect

PROMPT = '#'
IP = "10.0.15.104"
USERNAME = "admin"
PASSWORD = "cisco"
COMMAND = "show ip int b"

child = pexpect.spawn("telnet " + IP)
child.expect("Username")
child.sendline(USERNAME)
child.expect("Password")
child.sendline(PASSWORD)
child.expect(PROMPT)
child.sendline(COMMAND)
child.expect(PROMPT)
result = child.before
print(result)
print()
print(result.decode('UTF-8'))
child.sendline("exit")
