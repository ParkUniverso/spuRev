import time
import paramiko

''' array que guarda as olts e os parametros para conexão, os parametros são, respectivamente:
tipo de olt; nome da olt; ip; porta de acesso para consulta; usuario para consulta; senha para consulta;
usuario para modificações; porta para modificações'''
olts = [["zte", "Olt ZTE 1", "10.45.2.2", 22, "donavan", 'Ora@2020!','donavan', 22],
        ["zte", "Olt ZTE 2", "10.45.2.14", 22, "donavan", 'Ora@2020!','donavan', 22],
        ["nokia", "Olt Nokia Vicente Pires", "10.45.8.2", 22, "isadmin", 'ANS#150','SUPERUSER', 1022],
        ["nokia", "Olt Nokia Ceilandia 1", "10.45.4.2", 22, "isadmin", 'ANS#150','SUPERUSER', 1022],
        ["nokia", "Olt Nokia Ceilandia 2", "10.45.4.10", 22, "isadmin", 'ANS#150','SUPERUSER', 1022],
        ["nokia", "Olt Nokia Recando das Emas", "10.45.5.2", 22, "isadmin", 'ANS#150','SUPERUSER', 1022],
        ["nokia", "Olt Nokia Recando das Emas 2", "10.45.5.6", 22, "isadmin", 'ANS#150','SUPERUSER', 1022]]

class conSSL:
    # função que conecta à olt
    def __init__(self, olt, tipoCom):
        # variavel booleana que indica se houve erro na conexão
        self.flagCon = False
        self.oltSel = 0

        # verifica qual a olt selecionada pra ser realizada a conexão
        for x in range(len(olts)):
            if olts[x][1]==olt:
                self.oltSel = x
                print("conexão: " + olts[x][1])
                break

        # trecho a seguir efetivamente realiza a conexão
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if tipoCom == "consulta":
                self.client.connect(olts[self.oltSel][2], port=olts[self.oltSel][3], username=olts[self.oltSel][4],
                               password=olts[self.oltSel][5])
            elif tipoCom == "modificação":
                self.client.connect(olts[self.oltSel][2], port=olts[self.oltSel][7], username=olts[self.oltSel][6],
                               password=olts[self.oltSel][5])
            self.transport = self.client.get_transport()
            self.session = self.transport.open_session()
            self.session.get_pty()
            self.session.invoke_shell()
            time.sleep(0.5)
            self.session.send('\n')
            self.session.recv(8000)
            time.sleep(1)
            self.flagCon = False
        except Exception:
            self.flagCon = True

    # envia um comando para olt
    def enviarComando(self, comando):
        self.comando = comando
        self.session.send(self.comando)
        #time.sleep(0.2)

    # pega a resposta da olt a algum comando
    def receberResposta(self):
        # pega a respota da olt ao comando
        self.resposta = self.session.recv(50000000)

    # encerra a conexão
    def encCon(self):
        self.client.close()

