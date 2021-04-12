# necessário instalar a biblioteca paramiko para rodar o codigo
# necessario instalar a biblioteca cx_freeze para compilar o programa

from tkinter import *
from tkinter.messagebox import *
from manipulacaoDados import *
from scriptAtiv import *
from buscaLos import *
from buscaOnu import *
from apagOnu import *
from win32api import GetSystemMetrics
import time

onuLista = []

def redefVar():
    global onus
    i = len(onus)
    if i > 1:
        del onus[1:i]
    onus[0] = (["", "", "", "", "", ""])

class TelaInicial:
    def __init__(self, toplevel):
        #Seção que cria os containers
        self.containerTitulo = Frame(toplevel,pady=20)
        self.containerTitulo.pack()
        self.containerBotaoProv = Frame(toplevel,pady=3)
        self.containerBotaoProv.pack()
        self.containerBotaoBRomp = Frame(toplevel, pady=3)
        self.containerBotaoBRomp.pack()
        self.containerBotaoBOnu = Frame(toplevel, pady=3)
        self.containerBotaoBOnu.pack()

        #label com texto de titulo
        self.titulo = Label(self.containerTitulo, text='Sistema de Provisionamento Unificado')
        self.titulo['font'] = ('bold')
        self.titulo.pack()

        #botões
        self.botaoProv = Button(self.containerBotaoProv, text='ONUs não provisionadas', background='light grey')
        self.botaoProv['height'] = 3
        self.botaoProv['font'] = ('bold')
        self.botaoProv['width'] = 30
        self.botaoProv.bind("<ButtonRelease-1>", self.abrirProvisionamento)
        self.botaoProv.pack()

        self.botaoBuscaRomp = Button(self.containerBotaoBRomp, text='Buscar Rompimentos', background='light grey')
        self.botaoBuscaRomp['height'] = 3
        self.botaoBuscaRomp['font'] = ('bold')
        self.botaoBuscaRomp['width'] = 30
        self.botaoBuscaRomp.bind("<ButtonRelease-1>", self.abrirBuscaRomp)
        self.botaoBuscaRomp.pack()

        self.botaoBuscaOnu = Button(self.containerBotaoBOnu, text='Buscar ONU', background='light grey')
        self.botaoBuscaOnu['height'] = 3
        self.botaoBuscaOnu['font'] = ('bold')
        self.botaoBuscaOnu['width'] = 30
        self.botaoBuscaOnu.bind("<ButtonRelease-1>", self.abrirBuscaOnu)
        self.botaoBuscaOnu.pack()

    def processoNaoProv(self,event,x):
        if os.path.exists("Data/" + str(x)):
            os.remove("Data/" + str(x))
        data = open("Data/" + str(x), "a")
        data.write("\n")

        data.close()

        con = conSSL(olts[x][1], "consulta")
        # verifica se houve erro na conexão
        if not con.flagCon:
            # verifica se houve erro no envio do comando
            try:

                if olts[x][0] == "zte":
                    con.enviarComando("show gpon onu uncfg\n")
                    time.sleep(2)
                    con.receberResposta()
                elif olts[x][0] == "nokia":
                    con.enviarComando("show pon unprovision-onu\n")
                    time.sleep(2)
                    con.receberResposta()
                resposta = con.resposta
                resposta = resposta.decode('utf-8')

                # abre arquivo de dados
                data = open("Data/" + str(x), "a")
                data.write(resposta)


                data.close()
                con.encCon()
            except:
                showerror("ERRO", "Conexão " + olts[x][1] + " falhou!")
        else:
            # mensagem de erra caso a conexão falhe
            showerror("ERRO", "Conexão " + olts[x][1] + " falhou!")
        return 2

    #função que abre a tela de provisionamento
    def abrirProvisionamento(self, event):
        # iteração que busca onus não provisionadas em todas olts
        processos = [""]
        # verifica se existe a pasta onde fica salvo os dados, se não existir, ele cria ela
        if not os.path.exists("Data"):
            os.makedirs("Data")
        # cria os processos para o programa trabalhar em paralelismo
        for x in range(len(olts)):
            if os.path.exists("Data/" + str(x)):
                os.remove("Data/" + str(x))
            if x > 0:
                #processos.append(multiprocessing.Process(target=self.processoNaoProv,args=(x,)))
                processos.append(threading.Thread(target=self.processoNaoProv, args=(event,x,)))
            else:
                #processos[x] = multiprocessing.Process(target=self.processoNaoProv,args=(x,))
                processos[x] = threading.Thread(target=self.processoNaoProv,args=(event,x,))
            # estabelece a conexão
        # inicia os processos
        for x in range(len(processos)):
            processos[x].start()
        # espera os processos finalizarem
        tempo = 30
        start = time.time()
        for x in range(len(processos)):
            processos[x].join(timeout=tempo)
            end = time.time()
            if end - start >= 30:
                tempo = 1
        print("Interpretador" + datetime.now().strftime('%H:%M:%S'))
        for x in range(len(processos)):
            data = open("Data/" + str(x), 'r')
            data = data.read()
            interpretador = InterpretarDados(olts[x][1], data.encode('utf-8'))
            interpretador.onusNaoProv()
        print(datetime.now().strftime('%H:%M:%S'))
        #destroi o conteiners para limpar a tela antes mudar de tela
        self.containerTitulo.destroy()
        self.containerBotaoProv.destroy()
        self.containerBotaoBRomp.destroy()
        self.containerBotaoBOnu.destroy()
        TelaOnusNaoProv(root)
        root.mainloop()

    # função que abre a tela de busca de rompimentos
    def abrirBuscaRomp(self, event):
        #destroi o conteiners para limpar a tela antes mudar de tela
        self.containerTitulo.destroy()
        self.containerBotaoProv.destroy()
        self.containerBotaoBRomp.destroy()
        self.containerBotaoBOnu.destroy()
        TelaBuscarRompimentos(root)
        root.mainloop()

    # função que abre a tela de busca de onu
    def abrirBuscaOnu(self, event):
        # destroi o conteiners para limpar a tela antes mudar de tela
        self.containerTitulo.destroy()
        self.containerBotaoProv.destroy()
        self.containerBotaoBRomp.destroy()
        self.containerBotaoBOnu.destroy()
        TelaBuscarOnu(root)
        root.mainloop()

class TelaOnusNaoProv:
    def __init__(self, toplevel):
        # Seção que cria os containers
        self.containerTitulo = Frame(toplevel, pady=20)
        self.containerTitulo.pack()
        self.containerLista = Frame(toplevel, pady=2)
        self.containerLista.pack()
        self.containerContrato = Frame(toplevel, pady=2)
        self.containerContrato.pack()
        self.containerBotoes = Frame(toplevel)
        self.containerBotoes.pack(ipadx=2, pady=20)

        #texto Titulo
        self.titulo = Label(self.containerTitulo, text='Escolha uma ONU: ')
        self.titulo['font'] = ('bold')
        self.titulo.pack()
        #label contrato do cliente
        self.contratoLabel = Label(self.containerContrato, text='Contrato do cliente: ')
        self.contratoLabel['font'] = ('bold')
        self.contratoLabel.pack(side=LEFT)

        #entrada de texto contrato
        self.contratoEntrada = Entry(self.containerContrato, width=8)
        self.contratoEntrada.focus_force()
        self.contratoEntrada.pack(side=RIGHT)

        #lista de Onus
        self.listbox = Listbox(self.containerLista, width=50)
        for x in range(len(onus)):
            zero = ""
            zero2 = ""
            if onus[x][0] != "":
                if int(onus[x][1]) < 10 and "Nokia" in onus[x][5]: zero = "0"
                if int(onus[x][2]) < 10 and "Nokia" in onus[x][5]: zero2 = "0"
                self.listbox.insert(x, onus[x][0] + "/" + zero + onus[x][1] + "/" + zero2 + onus[x][2] + "   " + onus[x][5])
        self.listbox.selection_set(0)
        self.listbox.pack()

        #botões
        #botão para provionar onu
        self.botaoProv = Button(self.containerBotoes, text='Provisionar', background='light grey', padx=13)
        self.botaoProv['height'] = 2
        self.botaoProv.bind("<ButtonRelease-1>", self.provONU)
        self.botaoProv['font'] = ('bold')
        self.botaoProv.pack(side=LEFT)
        #botão para voltar para tela inicial
        self.botaoVolt = Button(self.containerBotoes, text='Voltar', background='light grey', padx=13)
        self.botaoVolt['height'] = 2
        self.botaoVolt.bind("<ButtonRelease-1>", self.voltarTelaInicial)
        self.botaoVolt['font'] = ('bold')
        self.botaoVolt.pack(side=RIGHT)

    # função que volta para tela inicial
    def voltarTelaInicial(self, event):
        # Limpa a tela
        self.containerTitulo.destroy()
        self.containerLista.destroy()
        self.containerContrato.destroy()
        self.containerBotoes.destroy()

        # redefine as variaveis
        redefVar()

        # volta para tela inicial
        TelaInicial(root)
        root.mainloop()

    # função que provisiona a onu selecionada
    def provONU(self, event):
        # Pega o contrato digitado
        contrato = self.contratoEntrada.get()
        # pega onu selecionada
        onuSel = self.listbox.selection_get()

        idx = 0
        script = ""
        # verfica qual a onu selecionada para ser provisionada
        for x in onuSel.split("/"):
            for y in range(len(onus)):
                if x == onus[y][0]:
                    #variavel que armazena a posição que a onu está no array
                    idx = y
            break

        #estabelece a conexão com a olt
        con = conSSL(onus[idx][5], "consulta")
        if con.flagCon == False:
            try:
                # percorre todas olts para verificar qual o modelo da olt selecionada
                for x in range(len(olts)):
                    if onus[idx][5] == olts[x][1]:
                        if olts[x][0] == "zte":
                            con.enviarComando("show gpon onu state gpon-olt_1/" + str(onus[idx][1]) + "/" + str(onus[idx][2]) + "\n")
                            time.sleep(3)
                            con.receberResposta()
                            respostaOlt = con.resposta

                            # olt zte exbe apenas as 21 primeiras onus em uma pon, necessario dar um enter para exibir cada onu
                            # apos essas 21, esse trecho faz isso
                            if len(con.resposta) > 1300:
                                for x in range(120):
                                    con.enviarComando("\n")
                                    time.sleep(0.7)
                                    con.receberResposta()
                                    if len(con.resposta) < 24:
                                        break
                                    respostaOlt = respostaOlt + con.resposta

                            # encontra uma posição livre na pon onde a onu será provisionada
                            posLivre = InterpretarDados(onus[idx][5],respostaOlt)
                            posLivre.encontrarPosLivre(idx)

                            # gera script que sera utilizado no provisionamento
                            script = scriptZTE(onus[idx][0], onus[idx][1], onus[idx][2], onus[idx][3], onus[idx][5],
                                               contrato, onus[idx][4])
                            #print(script)
                        elif olts[x][0] == "nokia":
                            con.enviarComando("show equipment ont status pon 1/1/" + str(onus[idx][1]) + "/" + str(onus[idx][2]) + "\n")
                            time.sleep(3)
                            con.receberResposta()

                            # encontra uma posição livre na pon onde a onu será provisionada
                            posLivre = InterpretarDados(onus[idx][5], con.resposta)
                            posLivre.encontrarPosLivre(idx)

                            # gera script que sera utilizado no provisionamento
                            script = scriptNokia(onus[idx][0], onus[idx][1], onus[idx][2], onus[idx][3], onus[idx][5],
                                               contrato, onus[idx][4])
                            con.encCon()
                            con = conSSL(onus[idx][5], "modificação")

                        break
                # provisiona a onu
                con.enviarComando("\n")
                time.sleep(2)
                con.enviarComando(script)
                con.enviarComando("\n")
                time.sleep(2)
                con.encCon()

                # verifica se existe a pasta onde fica salvo o log, se não existir, ele cria ela
                main_folder = os.path.join(os.path.expanduser("~"), "Documents")
                if not os.path.exists(main_folder + "/SPU"):
                    os.makedirs(main_folder + "/SPU")
                # abre arquivo de log
                log = open(main_folder + "/SPU/logProvisionamento.txt", "a")
                # escreve o log
                textoLog = ("Onu " + onus[idx][0] + " provisionada " + datetime.now().strftime(
                    '%d/%m/%Y %H:%M') + " na " + onus[idx][5] + "\n")
                # caixa de alerta sinalizando que o provisionamento está concluido
                showinfo("provisionamento", "Provisionamento concluído!")
                log.write(textoLog)
                log.write(script)
                log.write("\n\n")
                log.close()
            except:
                showerror("ERRO", "Conexão " + onus[idx][5] + " falhou!")
        elif con.flagCon:
            showerror("ERRO", "Conexão " + onus[idx][5] + " falhou!")




        #volta para tela inicial
        self.voltarTelaInicial(event)

class TelaBuscarRompimentos:
    def __init__(self, toplevel):
        # Seção que cria os containers
        self.containerTitulo = Frame(toplevel, pady=20)
        self.containerTitulo.pack()
        self.containerBotaoTodasOlts = Frame(toplevel, pady=3)
        self.containerBotaoTodasOlts.pack()
        self.containerBotaoUmaOlt = Frame(toplevel, pady=3)
        self.containerBotaoUmaOlt.pack()
        self.containerBotaoVoltar = Frame(toplevel, pady=3)
        self.containerBotaoVoltar.pack()


        # label com texto de titulo
        self.titulo = Label(self.containerTitulo, text='Buscar rompimentos')
        self.titulo['font'] = ('bold')
        self.titulo.pack()

        # botões
        self.botaoTodasOlts = Button(self.containerBotaoTodasOlts, text='Buscar em todas olts', background='light grey')
        self.botaoTodasOlts['height'] = 3
        self.botaoTodasOlts['font'] = ('bold')
        self.botaoTodasOlts['width'] = 30
        self.botaoTodasOlts.bind("<ButtonRelease-1>", self.buscaLosTodasOlts)
        self.botaoTodasOlts.pack()

        self.botaoUmaOlt = Button(self.containerBotaoUmaOlt, text='Buscar em uma olt específica', background='light grey')
        self.botaoUmaOlt['height'] = 3
        self.botaoUmaOlt['font'] = ('bold')
        self.botaoUmaOlt['width'] = 30
        self.botaoUmaOlt.bind("<ButtonRelease-1>", self.buscaLosUmaOlt)
        self.botaoUmaOlt.pack()

        self.botaoVoltar = Button(self.containerBotaoVoltar, text='Voltar', background='light grey')
        self.botaoVoltar['height'] = 3
        self.botaoVoltar['font'] = ('bold')
        self.botaoVoltar['width'] = 30
        self.botaoVoltar.bind("<ButtonRelease-1>", self.voltarTelaInicial)
        self.botaoVoltar.pack()

    # volta para tela inicial
    def voltarTelaInicial(self, event):
        # Limpa a tela
        self.containerTitulo.destroy()
        self.containerBotaoTodasOlts.destroy()
        self.containerBotaoUmaOlt.destroy()
        self.containerBotaoVoltar.destroy()

        # volta para tela inicial
        TelaInicial(root)
        root.mainloop()

    def processoLos(self,x):
        los = BuscaLos()
        los.buscaLos(olts[x][1])
        if los.flagCon:
            showerror("erro", "Conexão com a " + olts[x][1] + " falhou!")
        else:
            # verifica se existe a pasta onde fica salvo o log, se não existir, ele cria ela
            main_folder = os.path.join(os.path.expanduser("~"), "Documents")
            if not os.path.exists(main_folder + "/SPU/LOS"):
                os.makedirs(main_folder + "/SPU/LOS")
            # abre arquivo de log
            losTxt = open(main_folder + "/SPU/LOS/los " + olts[x][1] + " " + datetime.now().strftime(
                '%d-%m-%Y--%H-%M') + ".txt", "a")
            losTxt.write(los.resultado)
            losTxt.close()
    # função que busca los em todas olts
    def buscaLosTodasOlts(self, event):
        processos = [""]
        # percorre o array de olts buscando los em cada uma
        for x in range(len(olts)):
            if x > 0:
                # processos.append(multiprocessing.Process(target=self.processoNaoProv,args=(x,)))
                processos.append(threading.Thread(target=self.processoLos, args=(x,)))
            else:
                # processos[x] = multiprocessing.Process(target=self.processoNaoProv,args=(x,))
                processos[x] = threading.Thread(target=self.processoLos, args=(x,))
        # inicia os processos
        for x in range(len(processos)):
            processos[x].start()
        # espera os processos finalizarem
        for x in range(len(processos)):
            processos[x].join()

        # caixa de alerta sinalizando sucesso na busca
        showinfo("Window", "Busca Concluída!")
        self.voltarTelaInicial(event)

    # função que busca em uma olt
    def buscaLosUmaOlt(self, event):
        # Limpa a tela
        self.containerTitulo.destroy()
        self.containerBotaoTodasOlts.destroy()
        self.containerBotaoUmaOlt.destroy()
        self.containerBotaoVoltar.destroy()

        # vai para tela que exibe as olts
        TelaBuscaUmaOlt(root)
        root.mainloop()

class TelaBuscaUmaOlt:
    def __init__(self, toplevel):
        # Seção que cria os containers
        self.containerTitulo = Frame(toplevel, pady=20)
        self.containerTitulo.pack()
        self.containerLista = Frame(toplevel, pady=2)
        self.containerLista.pack()
        self.containerBotoes = Frame(toplevel)
        self.containerBotoes.pack(ipadx=2)

        # texto Titulo
        self.titulo = Label(self.containerTitulo, text='Escolha uma OLT: ')
        self.titulo['font'] = ('bold')
        self.titulo.pack()

        # lista de OLTs
        self.listbox = Listbox(self.containerLista, width=45)
        for x in range(len(olts)):
            self.listbox.insert(x, olts[x][1])
        self.listbox.selection_set(0)
        self.listbox.pack()

        # botões
        # botão para provionar onu
        self.botaoProv = Button(self.containerBotoes, text='Buscar', background='light grey', padx=13)
        self.botaoProv['height'] = 2
        self.botaoProv.bind("<ButtonRelease-1>", self.buscarLos)
        self.botaoProv['font'] = ('bold')
        self.botaoProv.pack(side=LEFT)
        # botão para voltar para tela inicial
        self.botaoVolt = Button(self.containerBotoes, text='Voltar', background='light grey', padx=13)
        self.botaoVolt['height'] = 2
        self.botaoVolt.bind("<ButtonRelease-1>", self.voltarTelaInicial)
        self.botaoVolt['font'] = ('bold')
        self.botaoVolt.pack(side=RIGHT)

    # função que volta para tela inicial
    def voltarTelaInicial(self, event):
        # Limpa a tela
        self.containerTitulo.destroy()
        self.containerLista.destroy()
        self.containerBotoes.destroy()

        # volta para tela inicial
        TelaInicial(root)
        root.mainloop()

    def buscarLos(self, event):
        oltSel = self.listbox.selection_get()

        los = BuscaLos()
        los.buscaLos(oltSel)
        if los.flagCon:
            showerror("erro", "Conexão com a " + oltSel + " falhou!")
        else:
            # verifica se existe a pasta onde fica salvo o log, se não existir, ele cria ela
            main_folder = os.path.join(os.path.expanduser("~"), "Documents")
            if not os.path.exists(main_folder + "/SPU/LOS"):
                os.makedirs(main_folder + "/SPU/LOS")
            # abre arquivo onde vair armazenar os los, nome do arquivo é: nome da olt + data + hora
            losTxt = open(main_folder + "/SPU/LOS/los " + oltSel + " " + datetime.now().strftime(
                '%d-%m-%Y--%H-%M') + ".txt", "a")
            losTxt.write(los.resultado)
            losTxt.close()
            showinfo("Window", "Busca Concluída!")
        self.voltarTelaInicial(event)

#tela resultado da busca de onu
class TelaBuscarOnu:
    def __init__(self, toplevel):
        # cria os conteiners
        self.containerOnu = Frame(toplevel, pady=23)
        self.containerOnu.pack()
        self.containerBotoesBusca = Frame(toplevel)
        self.containerBotoesBusca.pack(ipadx=2)
        self.containerTitulo = Frame(toplevel, pady=20)
        self.containerTitulo.pack()
        self.containerLista = Frame(toplevel, pady=2)
        self.containerLista.pack()
        self.containerBotoes = Frame(toplevel)
        self.containerBotoes.pack(ipadx=2, pady=30)

        # label de texto
        self.labelOnu = Label(self.containerOnu, text='Digite o serial da ONU: ')
        self.labelOnu['font'] = ('bold')
        self.labelOnu['width'] = 20
        self.labelOnu['height'] = 4
        self.labelOnu.pack(side=LEFT)

        # caixa de entrada de texto para serial da onu a ser buscada
        self.serialEntrada = Entry(self.containerOnu, width=14)
        self.serialEntrada.focus_force()
        self.serialEntrada.pack(side=RIGHT)

        # botões
        # botão para provionar onu
        self.botaoBusca = Button(self.containerBotoesBusca, text='Buscar', background='light grey', padx=13)
        self.botaoBusca['height'] = 2
        self.botaoBusca.bind("<ButtonRelease-1>", self.resultadoOnu)
        self.botaoBusca['font'] = ('bold')
        self.botaoBusca.pack(side=LEFT)
        # botão para voltar para tela inicial
        self.botaoVolt = Button(self.containerBotoesBusca, text='Voltar', background='light grey', padx=13)
        self.botaoVolt['height'] = 2
        self.botaoVolt.bind("<ButtonRelease-1>", self.voltarTelaInicial)
        self.botaoVolt['font'] = ('bold')
        self.botaoVolt.pack(side=RIGHT)

    def resultadoOnu(self, event):
        global onuLista
        # pega o serial digitado
        self.serial = self.serialEntrada.get()
        self.serial = self.serial.strip()
        self.serial = self.serial.replace(":",'')
        # realiza busca
        busca = BuscarONU(self.serial)

        # limpa a tela
        self.containerOnu.destroy()
        self.containerBotoesBusca.destroy()

        # texto Titulo
        # label titulo
        self.titulo = Label(self.containerTitulo, text='Resultado da Busca: ')
        self.titulo['font'] = ('bold')
        self.titulo.pack()
        # label tabela
        self.labelTabela = Label(self.containerLista, text='Posição     Status          Potencia             OLT      '
                                                           '                           ')
        self.labelTabela['width'] = 56
        self.labelTabela.pack()

        onuLista = busca.resultadoBusca

        if busca.flagCon:
            showerror("busca onu","Conexão Falhou!")

        #print(busca.resultadoBusca)
        # lista de Onus
        self.listbox = Listbox(self.containerLista, width=56)
        for x in range(len(busca.resultadoBusca)):
            print(x)
            # espaço em branco que organizam o resultado na listbox
            espacos = ["", "", ""]
            #print(busca.resultadoBusca[x][0] + busca.resultadoBusca[x][1] + busca.resultadoBusca[x][2])
            for y in range(11 - len(busca.resultadoBusca[x][0] + busca.resultadoBusca[x][1] + busca.resultadoBusca[x][2])):
                espacos[0] += " "
            for y in range(15 - len(busca.resultadoBusca[x][3])):
                espacos[1] += " "
            for y in range(16 - len(busca.resultadoBusca[x][4])):
                espacos[2] += " "
            if "ZTE" in busca.resultadoBusca[x][4]:
                espacos[2] += "             "
            stripOlt = busca.resultadoBusca[x][5].strip("Olt ")
            stripOlt = stripOlt.strip("Nokia ")

            if busca.resultadoBusca[x][0] != "":
                self.listbox.insert(x, str(x+1) + ":  " + busca.resultadoBusca[x][0] + "/" + busca.resultadoBusca[x][1] + ":" +busca.resultadoBusca[x][2] +
                                    espacos[0] + busca.resultadoBusca[x][3] + espacos[1] + busca.resultadoBusca[x][4] + espacos[2] + stripOlt)
        self.listbox.selection_set(0)
        self.listbox.pack()

        # botões
        # botão para apagar a onu
        self.botaoApagar = Button(self.containerBotoes, text='Apagar', background='light grey', padx=13)
        self.botaoApagar['height'] = 2
        self.botaoApagar.bind("<ButtonRelease-1>", self.confApagarOnu)
        self.botaoApagar['font'] = ('bold')
        self.botaoApagar.pack(side=LEFT)
        # botão para voltar para tela inicial
        self.botaoVolt = Button(self.containerBotoes, text='Voltar', background='light grey', padx=13)
        self.botaoVolt['height'] = 2
        self.botaoVolt.bind("<ButtonRelease-1>", self.voltarTelaInicial)
        self.botaoVolt['font'] = ('bold')
        self.botaoVolt.pack(side=RIGHT)

    # volta para tela inicial
    def voltarTelaInicial(self, event):
        # Limpa a tela
        self.containerTitulo.destroy()
        self.containerLista.destroy()
        self.containerBotoes.destroy()
        self.containerOnu.destroy()
        self.containerBotoesBusca.destroy()
        # volta para tela inicial
        TelaInicial(root)
        root.mainloop()

    # confirma se quer apagar a onu
    def confApagarOnu(self, event):
        decisaoUser = askokcancel("Apagar ONU", "Certerza que excluir a onu?!", icon="warning")
        if decisaoUser:
            self.apagarOnu(event)
        else:
            self.voltarTelaInicial(event)

    # função para apagar a onu
    def apagarOnu(self, event):
        # pega onu selecionada
        onuSel = self.listbox.selection_get()
        for x in onuSel.split(":"):
            apag = Apagar(onuLista[int(x)-1], self.serial)
            break

        showinfo("Apagar ONU", "Exclusão Realizada!")
        self.voltarTelaInicial(event)
root = Tk()
root.iconbitmap('ico/spu.ico')
root.title("Sistema de Provisionamento Unificado (Ísis)")
TelaInicial(root)

# posiciona a janela de acordo com a resolução da tela
if GetSystemMetrics(1) == 1080:
    root.geometry("550x385-650+300")
elif GetSystemMetrics(1) == 768 or GetSystemMetrics(1) == 720:
    root.geometry("550x385-400+150")
else:
    root.geometry("550x385")
root.mainloop()