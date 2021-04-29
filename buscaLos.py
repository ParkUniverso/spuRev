from conSSl import *
from datetime import datetime

class BuscaLos:
    def __init__(self):
        self.texto = ""
        self.resultado = ""
        self.flagCon = False
    def buscaLos(self, olt):
        self.olt = olt

        # identifica modelo da olt
        for x in range(len(olts)):
            if olts[x][1] == self.olt:
                self.modeloOlt = olts[x][0]
                self.idx = x

        if self.modeloOlt == "zte":
            con = conSSL(self.olt, "consulta")
            if not con.flagCon:
                try:
                    con.enviarComando("sho gpon onu state\n")
                    time.sleep(0.5)
                    con.enviarComando("\n")
                    time.sleep(2)
                    con.receberResposta()
                    self.respostaOlt = con.resposta.decode('utf-8')
                    # olt zte exbe apenas as 21 primeiras onus em uma pon, necessario dar um enter para exibir cada onu
                    # apos essas 21, esse trecho faz isso
                    print(datetime.now().strftime('%H:%M'))
                    if len(self.respostaOlt) > 1300:
                        for z in range(36000):
                            con.enviarComando("\n")
                            time.sleep(0.035)
                            con.enviarComando("\n")
                            time.sleep(0.035)
                            con.enviarComando("\n")
                            time.sleep(0.035)
                            con.receberResposta()
                            if len(con.resposta) == 69:
                                break
                            self.respostaOlt += con.resposta.decode('utf-8')
                    print(datetime.now().strftime('%H:%M:%S'))
                    # x será o slot no comando
                    for x in range(18):
                        flag = False
                        self.losPorSlot = 0
                        self.texto = ""
                        # y + 1 será a pon no comando
                        for y in range(16):
                            if (x >= 2 and x <= 9 or x >= 12):
                                self.los = 0
                                self.onu = 0
                                pon = False

                                # condicional que verifica se a olt possui o slot
                                if not "Invalid input detected" in self.respostaOlt:
                                    flag = True
                                    for z in self.respostaOlt.split():
                                        # soma cada slot na pon
                                        if ("LOS" in z or "OffLine" in z) and pon:
                                            self.los += 1
                                            pon = False
                                        # soma cada onu na pon
                                        elif "1/" + str(x) + "/" + str(y+1) + ":" in z:
                                            self.onu += 1
                                            pon = True
                                        elif "GPON" in z:
                                            pon = False
                                    # armazena o total de los por slot
                                    self.losPorSlot += self.los
                                    # guarda os los e o total de onus por pon ja formatdo como sera salvo no txt
                                    self.texto = self.texto + "  Pon " + str(y+1) + ": " + str(self.los) + "/" + str(self.onu) + "\n"
                        if flag:
                            zero = ""
                            if x < 10: zero = "0"
                            self.resultado += "Total Los slot " + zero + str(x) + ": " + str(self.losPorSlot) + "\n" + self.texto + "\n"
                    print(datetime.now().strftime('%H:%M:%S'))
                except:
                    self.flagCon = True
            else:
                self.flagCon = True
            con.encCon()
        elif self.modeloOlt == "nokia":
            flag = False
            con = conSSL(self.olt, "consulta")
            if not con.flagCon:
                try:
                    con.enviarComando("show equipment ont operational-data\n")
                    time.sleep(20)
                    con.receberResposta()
                    print(con.resposta.decode('utf-8'))
                    print(self.idx)
                    self.respostaOlt = con.resposta.decode('utf-8')
                    for y in range(8):
                        self.texto = ""
                        self.losPorSlot = 0
                        for z in range(16):
                            cont = 0
                            self.los = 0
                            self.onu = 0
                            for x in self.respostaOlt.split():
                                if flag:
                                    cont += 1
                                elif "1/1/" + str(y+1) + "/" + str(z+1) + "/" in x:
                                    flag = True
                                if cont == 5:
                                    if "yes" in x:
                                        self.onu += 1
                                    elif "no" in x:
                                        self.onu += 1
                                        cont = 0
                                        flag = False
                                elif cont == 6:
                                    cont = 0
                                    flag = False
                                    if "no" in x:
                                        self.los += 1
                            self.losPorSlot += self.los
                            self.texto = self.texto + "  Pon " + str(z + 1) + ": " + str(self.los) + "/" + str(self.onu) + "\n"
                        self.resultado += "Total Los slot 0" + str(y + 1) + ": " + str(self.losPorSlot) + "\n" + self.texto + "\n"
                except:
                    self.flagCon = True
            else:
                self.flagCon = True
            con.encCon()
