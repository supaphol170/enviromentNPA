import pexpect

lb_ads = ['1.1.1.1', '2.2.2.2', '3.3.3.3']
router_ads = ['172.31.104.4', '172.31.104.5', '172.31.104.6']

PROMPT = '#'
IP = "10.0.15.104"
USERNAME = "admin"
PASSWORD = "cisco"

for ip in range(len(router_ads)):
    child = pexpect.spawn("telnet " + router_ads[ip])
    child.expect("Username")
    child.sendline(USERNAME)
    child.expect("Password")
    child.sendline(PASSWORD)
    child.expect(PROMPT)
    child.sendline('conf t')
    child.expect(PROMPT)
    child.sendline('int loop 0')
    child.expect(PROMPT)
    child.sendline('ip add ' + lb_ads[ip] + ' 255.255.255.255')
    child.expect(PROMPT)
    result = child.before
    print(result)
    print()
    print(result.decode('UTF-8'))
    child.sendline("exit")
