# array que guarda os parametros da onu
# serial; slot; pon; posição; modelo de onu; olt;
onus=[["","","","","",""]]
from conSSl import *
class InterpretarDados:
    def __init__(self, olt, texto):
        global onus
        self.texto = texto
        self.olt = olt
        self.posicao = ""

        # verifica que tipo de olt é
        for x in range(len(olts)):
            if olts[x][1]==self.olt:
                self.tipoOlt = olts[x][0]
                break

    # guarda dados das onus não provisionadas
    def onusNaoProv(self):
        # serve para pegar a palavra seguinte a gpon-onu_ nas olt zte, o serial da onu, ou
        # a palavra apos 1/1/x/x/ nas olts nokia, o serial da onu
        flagSerial = False

        if self.tipoOlt == "zte":
            for x in self.texto.decode('utf-8').split():
                if "gpon-onu_" in x:
                    flagSerial = True

                    # verifica se é a primeira onu adicionada ao array, se não for adiciona espaço livre no array
                    if (onus[0][0] != ''):
                        onus.append(["", "", "", "", "", ""])

                    # guarda a olt no array de onu
                    onus[len(onus) - 1][5] = self.olt
                    i = 0

                    # identifica e separa slot e pon
                    for y in x.split("/"):
                        i += 1
                        if i == 2:
                            # salva slot
                            onus[len(onus)-1][1] = y
                        elif i == 3:
                            j = 0
                            for z in y.split(":"):
                                # salva pon
                                onus[len(onus) - 1][2] = z
                                break
                elif flagSerial:
                    # Guarda o serial da onu
                    onus[len(onus) - 1][0] = x

                    # chama função que verifica modelo da onu
                    self.verifModeloOnu(len(onus) - 1)

                    flagSerial = False
        elif self.tipoOlt == "nokia":
            for x in self.texto.decode('utf-8').split():
                if "1/1/" in x:
                    flagSerial = True

                    # verifica se é a primeira onu adicionada ao array, se não for adiciona espaço livre no array
                    print(onus)
                    if (onus[0][0] != ""):
                        onus.append(["", "", "", "", "", ""])

                    # guarda a olt no array de onu
                    onus[len(onus) - 1][5] = self.olt
                    i = 0

                    # identifica e separa slot e pon
                    for y in x.split("/"):
                        i += 1
                        if i == 3:
                            # salva slot
                            onus[len(onus) - 1][1] = y
                        elif i == 4:
                            onus[len(onus) - 1][2] = y
                            break
                # guarda o serial da onu
                elif flagSerial and len(x) == 12:
                    # Guarda o serial da onu
                    onus[len(onus) - 1][0] = x
                    # chama função que verifica modelo da onu
                    self.verifModeloOnu(len(onus) - 1)

                    flagSerial = False
                elif flagSerial and len(onus)>1:
                    del onus[len(onus)-1]
                    flagSerial = False
                elif flagSerial and len(onus)==1:
                    onus[0] = (["", "", "", "", "", ""])
                    flagSerial = False

    # verifica e Guarda o modelo da onu
    def verifModeloOnu(self, idx):
        if "ZTEGC8B" in onus[idx][0]:
            onus[idx][4] = "zte wifi"
        elif "ALCLFB" in onus[idx][0]:
            onus[idx][4] = "nokia"
        elif "ALCLB" in onus[idx][0]:
            onus[idx][4] = "nokia 2"
        else:
            onus[idx][4] = "bridge"

    def encontrarPosLivre(self, idx):
        contOnu = 0
        interrup = False
        if self.tipoOlt == "zte":
            for x in self.texto.decode('utf-8').split():
                # interrope a busca caso ja tenha sido encontrado um posição livre
                if interrup:
                    break

                # contabiliza as onus na pon
                elif "1/" + onus[idx][1] + "/" + onus[idx][2] + ":" in x:
                    contOnu += 1
                    i = 0
                    flag = False
                    for y in x.split(":"):
                        if flag:
                            self.posicao = y
                            if int(y) > contOnu:
                                self.posicao = str(contOnu)
                                interrup = True
                                break
                            else:
                                self.posicao = str(contOnu + 1)
                        flag = True

            # guarda no array a posição livre para ser provisionada a onu
            onus[idx][3] =self.posicao

        elif self.tipoOlt == "nokia":
            tempPos = ""
            flag = False
            for x in self.texto.decode('utf-8').split():
                # interrope a busca caso ja tenha sido encontrado um posição livre
                if interrup:
                    break
                elif "1/1/" + onus[idx][1] + "/" + onus[idx][2] + "/" in x:
                    flag = True
                    tempPos = x
                # filtra se de fato é uma onu da pon, ou um alarme
                elif flag and len(x) == 13:
                    contOnu += 1
                    cont = 0
                    for y in tempPos.split("/"):
                        cont += 1
                        if cont == 5:
                            if int(y) > contOnu:
                                self.posicao = str(contOnu)
                                interrup = True
                                break
                            else:
                                self.posicao = str(contOnu + 1)
                        flag = False
                else:
                    flag = False

            # guarda no array a posição livre para ser provisionada a onu
            onus[idx][3] = self.posicao
            #print(self.posicao)