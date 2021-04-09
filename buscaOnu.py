from conSSl import *
import os
import threading

class BuscarONU:
    def processoBuscaOnu(self,x):
        try:
            if ("ALCLFB" in self.serial or "ALCLB" in self.serial) and olts[x][0] == "nokia":
                self.buscarOnuNokia(olts[x][1])
            else:
                if olts[x][0] == "zte":
                    self.buscarOnuZte(olts[x][1])
                elif olts[x][0] == "nokia":
                    self.buscarOnuNokia(olts[x][1])
        except:
            self.flagCon = True
    def __init__(self, serial):
        # slot, pon, posição, status, potencia, olt
        # self.resultadoBusca = [["","","","","","", False]]
        self.resultadoBusca = [["", "", "", "", "", "", False]]

        self.serialNok = ""
        self.serial = serial
        self.flagCon = False
        self.formartSerialNok()
        processos = [""]
        for x in range(len(olts)):
            if x > 0:
                # processos.append(multiprocessing.Process(target=self.processoNaoProv,args=(x,)))
                processos.append(threading.Thread(target=self.processoBuscaOnu, args=(x,)))
            else:
                # processos[x] = multiprocessing.Process(target=self.processoNaoProv,args=(x,))
                processos[x] = threading.Thread(target=self.processoBuscaOnu, args=(x,))
                # inicia os processos
        for x in range(len(processos)):
            processos[x].start()
        # espera os processos finalizarem
        for x in range(len(processos)):
            processos[x].join()

    def buscarOnuZte(self, olt):
        resultado = [["", "", "", "", "", "", False]]
        con = conSSL(olt,"consulta")
        con.enviarComando("show gpon onu by sn " + self.serial + "\n")
        time.sleep(2)
        con.enviarComando("\n")
        time.sleep(1)
        con.receberResposta()
        resposta = con.resposta.decode('utf-8')
        for x in resposta.split():
            if "gpon-onu_1/" in x:
                '''if self.resultadoBusca[len(self.resultadoBusca) - 1][0] != "":
                    self.resultadoBusca.append(["", "", "", "", "", "", False])'''
                if resultado[len(resultado) - 1][0] != "":
                    resultado.append(["", "", "", "", "", "", False])
                cont = 0
                for y in x.split("/"):
                    cont += 1
                    if cont == 2:
                        # armazena o slot
                        resultado[len(resultado)-1][0] = y
                    elif cont == 3:
                        flag = False
                        for z in y.split(":"):
                            if not flag:
                                flag = True
                                # armazena a pon
                                resultado[len(resultado) - 1][1] = z
                            else:
                                # armazena a posição
                                resultado[len(resultado) - 1][2] = z
                # guarda a olt que foi encontrada a onu
                resultado[len(resultado) - 1][5] = olt

                # verifica a potencia
                con.enviarComando(" show pon power attenuation gpon-onu_1/" + resultado[len(resultado)-1][0] +
                                  "/" + resultado[len(resultado)-1][1] + ":" + resultado[len(resultado)-1][2] + "\n")
                time.sleep(4)
                #con.enviarComando("\n")
                con.receberResposta()
                potencia = con.resposta.decode('utf-8')
                flagPotencia = False
                primeiroRx = False
                for y in potencia.split():
                    if "Rx" in y:
                        flagPotencia = True
                        i = 0

                        # no segundo rx pega a potencia
                        if len(y) > 2:
                            for z in y.split(':'):
                                if i == 1:
                                    j = 0
                                    for w in z:
                                        j += 1
                                        if j <= 5: resultado[len(resultado) - 1][4] += w
                                i += 1
                    elif flagPotencia and primeiroRx:
                        # se não conseguir medir a potencia verifica qual a causa
                        if "N/A" in y:
                            con.enviarComando(" sho gpon onu detail-info gpon-onu_1/" + resultado[len(resultado)-1][0] +
                                  "/" + resultado[len(resultado)-1][1] + ":" + resultado[len(resultado)-1][2] + "\n")
                            time.sleep(2)
                            con.enviarComando("\n")
                            time.sleep(1)
                            con.receberResposta()
                            status = con.resposta.decode('utf-8')
                            i = 0
                            j = 0
                            for z in status.split():
                                i += 1
                                if "Phase" in z:
                                    j = i + 2
                                elif i == j:
                                    if ("LOS" in z):
                                        resultado[len(resultado) - 1][3] = (z)
                                        resultado[len(resultado) - 1][4] = (z)
                                    elif ("OffLine" in z):
                                        resultado[len(resultado) - 1][3] = (z)
                                        resultado[len(resultado) - 1][4] = (z)
                                    else:
                                        resultado[len(resultado) - 1][3] = (z)
                                        resultado[len(resultado) - 1][4] = (z)
                                    break
                        else:
                            i = 0
                            for z in y:
                                i+=1
                                if i == 2: resultado[len(resultado) - 1][3] = "Working"
                        break
                    elif flagPotencia:
                        # a potencia fica apos o segundo rx na resposta da olt
                        flagPotencia = False
                        primeiroRx = True
        print(resultado)
        for x in range(len(resultado)):
            if self.resultadoBusca[0][0] == "":
                self.resultadoBusca = resultado
                break
            else:
                self.resultadoBusca.append(["", "", "", "", "", "", False])
                print(resultado[x])
                self.resultadoBusca[len(self.resultadoBusca)-1] = resultado[x]
        print(self.resultadoBusca)
        con.encCon()


    def buscarOnuNokia(self, olt):
        resultado = [["", "", "", "", "", "", False]]
        con = conSSL(olt,"consulta")
        con.enviarComando("show equipment ont index sn:" + self.serialNok + "\n")
        time.sleep(2)
        con.enviarComando("\n")
        time.sleep(1)
        con.receberResposta()
        resposta = con.resposta.decode('utf-8')
        flag = False
        for x in resposta.split():
            if self.serialNok in x:
                flag = True
            elif flag:
                flag = False
                if "1/1/" in x:
                    cont = 0
                    '''if self.resultadoBusca[len(self.resultadoBusca) - 1][0] != "":
                        self.resultadoBusca.append(["", "", "", "", "", "", False])'''
                    if resultado[len(resultado) - 1][0] != "":
                        resultado.append(["", "", "", "", "", "", False])
                    for y in x.split("/"):
                        cont += 1
                        if cont == 3: resultado[len(resultado)-1][0] = y
                        elif cont == 4: resultado[len(resultado)-1][1] = y
                        elif cont == 5: resultado[len(resultado) - 1][2] = y
                    con.enviarComando(" show equipment ont optics 1/1/" + resultado[len(resultado)-1][0] + "/" +
                             resultado[len(resultado)-1][1] + "/" + resultado[len(resultado) - 1][2] + "\n")
                    time.sleep(2)
                    con.enviarComando("\n")
                    time.sleep(1)
                    con.receberResposta()
                    potencia = con.resposta.decode('utf-8')
                    contagem = False
                    cont = 0
                    for y in potencia.split():
                        if "|rx-signal" in y:
                            contagem = True
                        elif contagem:
                            cont += 1
                        if cont == 13:
                            cont2 = 0
                            if "unknown" in y:
                                con.enviarComando(" show equipment ont operational-data 1/1/" + resultado[len(resultado)-1][0] + "/" +
                                                    resultado[len(resultado)-1][1] + "/" + resultado[len(resultado) - 1][2] + "\n")
                                time.sleep(2)
                                con.enviarComando("\n")
                                time.sleep(1)
                                con.receberResposta()
                                status = con.resposta.decode('utf-8')
                                flag2 = False
                                for z in status.split():
                                    if "ont-idx" in z:
                                        flag2 = True
                                    if flag2:
                                        cont2 += 1
                                    if cont2 == 15:
                                        if "no" in z:
                                            resultado[len(resultado) - 1][3] = ("LOS")
                                            resultado[len(resultado) - 1][4] = ("LOS")
                                        else:
                                            resultado[len(resultado) - 1][3] = ("DyingGasp")
                                            resultado[len(resultado) - 1][4] = ("DyingGasp")
                            else:
                                resultado[len(resultado) - 1][3] = "Working"
                                for z in y:
                                    cont2 += 1
                                    if cont2 <= 5: resultado[len(resultado) - 1][4] += z
                    resultado[len(resultado) - 1][5] = olt
        for x in range(len(resultado)):
            if self.resultadoBusca[0][0] == "":
                self.resultadoBusca = resultado
                break
            else:
                self.resultadoBusca.append(["", "", "", "", "", "", False])
                print(resultado[x])
                self.resultadoBusca[len(self.resultadoBusca)-1] = resultado[x]
        print(self.resultadoBusca)
        con.encCon()


    def formartSerialNok(self):
        i = 0
        for x in self.serial:
            i += 1
            if i == 5:
                self.serialNok += ":" + x
            else:
                self.serialNok += x