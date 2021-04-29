import paramiko
import time
import threading
import multiprocessing
slot = ""
pon = ""
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.45.2.2', port=22, username='donavan', password='Ora@2020!')
#client.connect('10.45.2.14', port=22, username='donavan', password='Ora@2020!')
transport = client.get_transport()
session = transport.open_session()
# session.setblocking(0) # Set to non-blocking mode
session.get_pty()
session.invoke_shell()
session.send('\n')
session.recv(8000)
session.send("co t")
time.sleep(1)
session.send('\n')
print("agora")
time.sleep(20)
session.send("show gpon onu state gpon-olt_1/" + slot + "/" + pon + "\n")
time.sleep(3)
output = session.recv(100000)
print(output)
client.close()
