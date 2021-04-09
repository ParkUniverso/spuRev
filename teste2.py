import paramiko
import time
onuMud = ["", "", ""]
onu = ["3","4","6","7","13","21"]

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
for x in range(17):
    if x+1 > 16:
    #if x + 1 > 1 and x + 1 < 10 or x + 1 > 11:
        for y in range(16):
            pos = [""]
            session.send("sho gpon onu state gpon-olt_1/" + str(x+1) + "/" + str(y+1) + "\n")
            time.sleep(3)
            output = session.recv(100000)
            if len(output) > 1300:
                session.send("\n")
                for z in range(36000):
                    session.send("\n")
                    time.sleep(0.055)
                    session.send("\n")
                    time.sleep(0.055)
                    session.send("\n")
                    time.sleep(0.055)
                    session.send("\n")
                    var = session.recv(100000)
                    output += var
                    if len(var) == 69:
                        break
            print(output)
            j = 0
            for z in output.decode('utf-8').split():
                if j > 0:
                    j += 1
                if "1/" + str(x+1) + "/" + str(y+1) in z and "gpon-olt" not in z:
                    i = 0
                    j += 1
                    for w in z.split(":"):
                        if i == 1:
                            if pos[0] == "":
                                pos[0] = w
                            else:
                                pos.append(w)
                        i = 1
                if j == 4 :
                    j = 0
                    if "OffLine" not in z:
                        if len(pos) > 1:
                            del pos[len(pos)-1]
                        else:
                            pos[0] = ""
                    else:
                        print(z)

            print(pos)
            print("teste")
            if pos[0] != "":
                session.send("co t\n")
                time.sleep(1)
                session.send(" interface gpon-olt_1/" + str(x + 1) + "/" + str(y + 1) + "\n")
                time.sleep(1)
                for z in range(len(pos)):
                    session.send(" no onu " + pos[z] + "\n")
                    time.sleep(1)
                session.send(" exit\n")
                time.sleep(1)
                session.send(" exit\n")
                time.sleep(1)
                output2 = session.recv(100000)
                print(output2)

'''session.send("\n")
time.sleep(1)
output = session.recv(100000)
print(len(output))
for x in range(100):
    session.send('\n')
    time.sleep(0.035)
    session.send('\n')
    time.sleep(0.035)
    session.send('\n')
    time.sleep(0.035)
    output = session.recv(100000)
    print(len(output))'''