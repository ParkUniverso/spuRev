from conSSl import *
import os
from datetime import datetime

class Apagar:
    def __init__(self, onu, serial):
        con = conSSL(onu[5],"modificação")
        self.flagCon = con.flagCon
        if not self.flagCon:
            # verifica se existe a pasta onde fica salvo o log, se não existir, ele cria ela
            main_folder = os.path.join(os.path.expanduser("~"), "Documents")
            if not os.path.exists(main_folder + "/SPU"):
                os.makedirs(main_folder + "/SPU")
            # abre arquivo de log
            log = open(main_folder + "/SPU/logExclusoes.txt", "a")
            # escreve o log
            textoLog = ("Onu " + serial + "/" + onu[0] + "/" + onu[1] + ":" + onu[2] + " excluída " + " da " + onu[5] +
                        " " + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n")
            log.write(textoLog)
            log.write("\n")
            log.close()
            if "ZTE" in onu[5]:
                con.enviarComando("configure terminal\n")
                time.sleep(1)
                con.enviarComando("interface gpon-olt_1/" + onu[0] + "/" + onu[1] + "\n")
                time.sleep(1)
                con.enviarComando("no onu " + onu[2] + "\n")
                time.sleep(1)
                con.receberResposta()
                con.encCon()
            elif "Nokia" in onu[5]:
                con.enviarComando("ED-ONT::ONT-1-1-" + onu[0] + "-" + onu[1] + "-" + onu[2] + ":::::OOS;\n"
                                    "DLT-ONT::ONT-1-1-" + onu[0] + "-" + onu[1] + "-" + onu[2] + "::;\n")
                time.sleep(1)
                con.receberResposta()
                con.encCon()

