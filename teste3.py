import paramiko
import time

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.45.2.2', port=22, username='donavan', password='Ora@2020!')
transport = client.get_transport()
session = transport.open_session()
# session.setblocking(0) # Set to non-blocking mode
session.get_pty()
session.invoke_shell()
session.send('\n')
time.sleep(2)
session.recv(8000)
for x in range (17):
    if x + 1 > 1 and x + 1 < 10 or x + 1 > 11:
        for y in range(16):
            print(x+1)
            session.send("co t\n")
            time.sleep(2)
            session.send(" interface gpon-olt_1/" + str(x + 1) + "/" + str(y + 1) + "\n")
            time.sleep(2)
            session.send(" reset\n")
            time.sleep(2)
            session.send(" exit\n")
            time.sleep(2)
            session.send(" exit\n")
            time.sleep(2)
            output2 = session.recv(100000)
            print(output2.decode('utf-8'))