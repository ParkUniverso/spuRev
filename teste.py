import paramiko
import time
import threading
import multiprocessing
onuMud = ["", "", ""]
onu = ["3","4","6","7","13","21"]
output =""
output2 =""
out = ""
def pros1(resultado):
    global out
    global output
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
    session.recv(8000)
    session.send("co t")
    time.sleep(1)
    session.send('\n')
    print("agora")
    time.sleep(20)
    session.send("show gpon onu state gpon-olt_1/2/2\n")
    time.sleep(3)
    output = session.recv(100000)
    resultado += output.decode('utf-8')
    client.close()
def pros2(resultado):
    global out
    global output2
    client2 = paramiko.SSHClient()
    client2.load_system_host_keys()
    client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client2.connect('10.45.2.14', port=22, username='donavan', password='Ora@2020!')
    transport2 = client2.get_transport()
    session2 = transport2.open_session()
    # session.setblocking(0) # Set to non-blocking mode
    session2.get_pty()
    session2.invoke_shell()
    session2.send('\n')
    session2.recv(8000)
    session2.send("co t")
    time.sleep(1)
    session2.send('\n')
    print("agora")
    time.sleep(20)
    session2.send("show gpon onu state gpon-olt_1/2/2\n")
    time.sleep(3)
    output2 = session2.recv(100000)
    resultado += output2.decode('utf-8')
    client2.close()


'''t1 = threading.Thread(target=pros1)
t2 = threading.Thread(target=pros2)
t1.start()
t2.start()'''
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=pros1)
    p2 = multiprocessing.Process(target=pros2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
#zte 1: 1685, 95, 23