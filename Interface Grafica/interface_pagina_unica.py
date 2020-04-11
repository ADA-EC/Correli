from tkinter import *
import tkinter as tk
from tkinter.filedialog import asksaveasfile    #Biblioteca utilizada para salvar o arquivo na pasta que o usuário escolher 
from tkinter import messagebox as msgb
import datetime	#Biblioteca utilizada para pegar o horário e data de início do teste
import serial
import sys  #Biblioteca usada para reiniciar o programa
import os   #Biblioteca usada para reiniciar o programa
import warnings
import serial.tools.list_ports

#Função que descobre as portas do computador que estão com o Arduino conectadas
if os.name == 'nt': #Utilizada para descobrir qual o sistema operacional do computador (Windows)
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'USB-SERIAL CH340' in p.description
    ]
    
else:   #Ubuntu
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'USB2.0-Serial' in p.description
    ]


#Pagina inicial da interface
class Application:
    def __init__(self, master=None):
        tempoinicio=datetime.datetime.now() #Trecho utilizado para salvar o horário atual em que o programa foi aberto, para salvá-lo como dado
        file = None
        self.nomearq = tk.StringVar()
        self.nomearq.set("")
        self.enderecoarq = tk.StringVar()
        self.enderecoarq.set("")
        
        #Função para enviar dados para o Arduino
        def enviar(info):
            arduino.write(info.encode())

        #Segunda página da interface
        def parametros():
            file = None
            while file is None:
                #Salvamento do arquivo em um local da pasta desejado pelo usuário
                files = [('Text Document', '*.txt'), 
                         ('Python Files', '*.py'),
                         ('All Files', '*.*')]      #Tipos de arquivos possíveis para salvar
                file = asksaveasfile(filetypes = files, defaultextension = files)

                #TEM QUE ARRUMAR PARA SÓ COLOCAR O ENDEREÇO!!!!!
                self.enderecoarq.set(str(file)) #Muda variável enderecoarq para o endereço do arquivo criado


                
        #Terceira página
        def pagPreDados():

            
            #Quarta página presente na interface, com a tabela que mostra os dados enviados pelo Arduino
            def pagina_dados():
                '''
                Após definido o intervalo, a 2a página é fechada, a primeira é limpa e os dados gerados
                pela prensa são printados na tela da interface
                '''
                def fechar():       #função que fecha o programa
                    end = '0'   #variável enviada para o arduino, para que ele finalize o programa
                    enviar(end).close()
                    root.destroy()
                    sys.exit()

                #Comandos utilizados para enviar ao documento criado os dados utilizados pelo usuário
                enviar(info)

                #self.cont.destroy()

                #Criação dos containers presentes na página de dados e posicionamento dos mesmos
                self.containerlist = Frame(master)
                self.containerlist["pady"] = 1
                self.containerlist["padx"] = 1
                self.containerlist.pack(fill=BOTH, expand=1)
                
                self.containerbotao = Frame(master)
                self.containerbotao["pady"] = 1
                self.containerbotao["padx"] = 1
                self.containerbotao.pack()

                self.botaofechar = Button(self.containerbotao, text="Fechar",)
                self.botaofechar.pack(side=LEFT)
                self.botaofechar["command"]=fechar
                
                self.listbox=Listbox(self.containerlist, width=50, height=20)

                
                #Função para receber o arduino e imprimir informações na listbox
                def imprime():
                    x=(arduino.readline().strip())  #Recebe os dados enviados do arduino e os coloca na variável x
                    self.listbox.insert(END, x) #Insere os dados recebidos no final da listbox
                    self.listbox.yview(END)
                    root.after(100, imprime)
                    file.write(x.decode("utf-8") + "\n")

                
                #Dados inseridos no início da listbox, com as informações criadas pelo usuário
                self.listbox.insert(END, 'Projeto Correli')
                self.listbox.insert(END, 'Horário de início do ensaio: '+str(tempoinicio))

                file.write("Projeto Correli\n")
                file.write("Horário de início do ensaio: "+str(tempoinicio)+"\n")

                if modo=='f':
                    self.listbox.insert(END, 'Escolha de intervalo: Força')
                    file.write("Escolha de intervalo: Força\n")
                else:
                    self.listbox.insert(END, 'Escolha de intervalo: Tempo')
                    file.write("Escolha de intervalo: Tempo\n")

                self.listbox.insert(END, 'Intervalo escolhido: '+str(interv))
                self.listbox.insert(END, 'Fundo de escala: '+str(fundo_escala))
                self.listbox.insert(END, ' ')

                file.write("Intervalo escolhido: "+str(interv)+"\n")
                file.write("Fundo de escala: "+str(fundo_escala)+"\n\n")


                #Imprime do arduino
                root.after(100, imprime)

                #Comandos para criar uma barra de rolagem para ficar melhor para o usuário visualizar as informações que estão sendo acrescentadas
                self.scrollbar = Scrollbar(self.containerlist)
                self.scrollbar.pack(side=RIGHT, fill=Y)
                self.listbox.config(yscrollcommand=self.scrollbar.set)
                self.scrollbar.config(command=self.listbox.yview)
                self.listbox.pack(fill=BOTH, expand=1)


            #Terceira página para iniciar o programa com os dados já inseridos
            if var.get() == 1:  #Condição utilizada para salvar o modo de medição escolhido pelo usuário
                modo = 't'
            elif var.get()==2: 
                modo = 'f'

            if self.intervaloesc.get()=="" or self.funesca.get()=="" or (var.get()!=1 and var.get()!=2) or not self.intervaloesc.get().isnumeric() or not self.funesca.get().isnumeric():
                #Teste para conferir que o usuário não deixou nenhum campo de preenchimento em branco ou se digitou alguma letra ao invés de número
                msgb.showerror("ERRO!", "Insira um valor!")

            elif modo == 'f' and float(self.intervaloesc.get())>float(self.funesca.get()):
                #Teste para conferir que a pessoa nao inseriu um intervalo maior do que o fundo de escala
                msgb.showerror("ERRO!", "Insira um intervalo menor do que o fundo de escala!")

            else:   #Caso o usuário tenha inserido todos os valores corretamente
                #Recupera os dados colocados pelo usuário, para usá-los como parâmetro
                interv=self.intervaloesc.get()
                fundo_escala=self.funesca.get()
                info = modo + "," +str(interv) + "," + str(fundo_escala)+"\n"

                #Limpar a página de dados
                '''self.cont1.destroy()
                self.cont2.destroy()
                self.cont3.destroy()
                self.cont4.destroy()'''

                #Atualiza tamanho da página, para comportar a mensagem
                self.cont = Frame (master)
                self.cont["pady"]=50
                self.cont["padx"]=10
                self.cont.pack()

                self.msgIni = Label (self.cont, text = "Aperte o botão para iniciar o programa")
                self.msgIni["font"] = ("Calibri", "12", "bold")
                self.msgIni.pack()

                self.botIni = Button (self.cont, text = "Iniciar")
                self.botIni.pack(side = BOTTOM)
                self.botIni["command"] = pagina_dados

                    

                #self.contensaio.destroy()

        #Página inical da interface, com os dados para salvar o arquivo e iniciar o programa
        num_arduinos=len(arduino_ports)    #Variável que contém o número de arduinos linkados na máquina
        i=0

        if num_arduinos==0:
            msgb.showerror("ERRO!", "Não existem Arduinos conectados a esse computador!")
            root.destroy()
            sys.exit()

        #Container com informações do arquivo de ensaio
        self.cont1=Frame(master)
        self.cont1["pady"]=1
        self.cont1.pack()

        #Container definindo parte do projeto
        self.contensaio = Frame(self.cont1)
        self.contensaio["pady"] = 1
        self.contensaio["padx"] = 0
        self.contensaio.pack()

        self.ensaio=Label(self.contensaio, text="Ensaio")
        self.ensaio["font"] = ("Calibri", "12", "bold")
        self.ensaio.pack(side=LEFT)

        self.nada=Label(self.contensaio, text="", width=60)
        self.nada.pack(side=RIGHT)


        #Container com informações do arquivo
        self.contArquivo = Frame(self.cont1)
        self.contArquivo["pady"]=5
        self.contArquivo["padx"]=20
        self.contArquivo.pack()

        self.Arquivo=Label(self.contArquivo, text="Nome do arquivo:")
        self.Arquivo["font"] = ("Calibri", "12")
        self.Arquivo.pack(side=LEFT)

        self.nomeArquivo=Label(self.contArquivo, textvariable=self.nomearq, bg="gray88", width=30)
        self.nomeArquivo.pack(side=RIGHT)


        #Container com o local do arquivo
        self.contLocArq=Frame(self.cont1)
        self.contLocArq["pady"]=5
        self.contLocArq["padx"]=1
        self.contLocArq.pack()
        
        self.local=Label(self.contLocArq, text="Local:")
        self.local["font"]=("Calibri", "12")
        self.local.pack(side=LEFT)

        self.localArquivo=Label(self.contLocArq, textvariable=self.enderecoarq, bg="gray88", width=50)
        self.localArquivo["font"]=("Calibri", "10")
        self.localArquivo.pack(side=LEFT)

        self.botaoLocal=Button(self.contLocArq, text="Alterar")
        self.botaoLocal["width"]=10
        self.botaoLocal.pack(side=RIGHT)
        self.botaoLocal["command"]=parametros #Quando é apertado o botão, o código vai para parâmetros, que cria outra página


        #Lista de portas de Arduino disponíveis
        self.contarduino = Frame(self.cont1)
        self.contarduino["pady"] = 5
        self.contarduino["padx"] = 0
        self.contarduino.pack()
        
        portaEscolhida=StringVar()
        portaEscolhida.set("Portas Arduino") # default value
        self.listaArduinos=OptionMenu(self.contarduino, portaEscolhida, arduino_ports)
        self.listaArduinos.config(width=15)
        self.listaArduinos.pack(side=BOTTOM)


        #Espaçamento entre o ensaio e os parâmetros do ensaio
        self.contvazio=Frame(self.cont1)
        self.contvazio["padx"]=10
        self.contvazio.pack()

        self.labelvazia=Label(self.contvazio, text="", height=1)
        self.labelvazia.pack()


        #Container com informações do arquivo de parâmetros
        self.cont2=Frame(master)
        self.cont2["pady"]=10
        self.cont2.pack()

        #Container definindo parte do projeto
        self.contparametro = Frame(self.cont2)
        self.contparametro["pady"] = 1
        self.contparametro["padx"] = 0
        self.contparametro.pack()

        self.parametro=Label(self.contparametro, text="Parâmetros")
        self.parametro["font"] = ("Calibri", "12", "bold")
        self.parametro.pack(side=LEFT)

        self.nada1=Label(self.contparametro, text="", width=55)
        self.nada1.pack(side=RIGHT)


        #Botões para definir salvamento do arquivo de parâmetros
        self.contbotaopar=Frame(self.cont2)
        self.contbotaopar["pady"] = 1
        self.contbotaopar["padx"] = 0
        self.contbotaopar.pack()

        self.botaosalvar = Button (self.contbotaopar, text = "Salvar Parâmetros")
        self.botaosalvar.pack(side=LEFT)
        #self.botaosalvar["command"]=   SALVAR CONFIG --> SHIFT

        self.nada2=Label(self.contbotaopar, text="", width=20)
        self.nada2.pack(side=LEFT)

        self.botaoCarreg = Button (self.contbotaopar, text = "Carregar Parâmetros")
        self.botaoCarreg.pack(side=RIGHT)
        #self.botaoCarreg["command"]=   CARREGAR CONFIGURAÇÕES --> SHIFT


        #Nome do arquivo de parâmetros
        self.contnomepar = Frame(self.cont2)
        self.contnomepar["pady"]=15
        self.contnomepar["padx"]=20
        self.contnomepar.pack()
        
        self.Arquivo=Label(self.contnomepar, text="Nome do arquivo:")
        self.Arquivo["font"] = ("Calibri", "12")
        self.Arquivo.pack(side=LEFT)

        self.nomeArquivo=Label(self.contnomepar, textvariable=self.nomearq, bg="gray88", width=30)
        self.nomeArquivo.pack(side=RIGHT)


        #Container com o local do arquivo
        self.contLocPar=Frame(self.cont2)
        self.contLocPar["pady"]=1
        self.contLocPar["padx"]=1
        self.contLocPar.pack()
        
        self.local=Label(self.contLocPar, text="Local:")
        self.local["font"]=("Calibri", "12")
        self.local.pack(side=LEFT)

        self.localArquivo=Label(self.contLocPar, textvariable=self.enderecoarq, bg="gray88", width=50)
        self.localArquivo["font"]=("Calibri", "10")
        self.localArquivo.pack(side=LEFT)

        #Containers com modo e escala de teste
        self.contModo = Frame(self.cont2)
        self.contModo["pady"]=5
        self.contModo.pack()

        self.respModo=Frame(self.cont2)
        self.respModo["pady"]=1
        self.respModo.pack()

        #COLOCAR UM IF PARA ARQUIVO JA EXISTENTE, PREENCHER TODOS OS CAMPOS E DEIXAR INVIÁVEL PARA USUÁRIO MEXER!
        self.configuracao = Label(self.contModo, text="Modo de operação")
        self.configuracao["font"] = ("Calibri", "12")
        self.configuracao.pack()

        #Função para escolher apenas uma opção entre força e tempo
        var = tk.IntVar()
        self.Tempo = Radiobutton(self.contModo, text = "Tempo", variable = var, value = 1)
        self.Tempo.pack (side = LEFT)
        self.Forca = Radiobutton(self.contModo, text = "Força", variable = var, value = 2)
        self.Forca.pack(side = RIGHT)

        '''self.nada=Label(self.contModo, text="", width=15)
        self.nada.pack(side=LEFT)

        self.nada=Label(self.respModo, text="", width=14)
        self.nada.pack(side=LEFT)'''

        self.msgEscala = Label (self.respModo, text = "Fundo de escala")
        self.msgEscala["font"] = ("Calibri", "12")
        self.msgEscala.pack(side=LEFT)

        self.funesca = Entry(self.respModo)
        self.funesca.pack(side=RIGHT)


        #Função para escolher o intervalo
        self.contInt=Frame(self.cont2)
        self.contInt["pady"]=10
        self.contInt["padx"]=5
        self.contInt.pack()

        self.mensagem = Label(self.contInt, text="Intervalo (ms ou t)")
        self.mensagem["font"] = ("Calibri", "12")
        self.mensagem.pack(side=LEFT)

        self.intervaloesc = Entry(self.contInt)
        self.intervaloesc.pack(side=RIGHT)

        
        #Botões de fechamento do programa ou rodagem do mesmo
        self.contBotao=Frame(self.cont2)
        self.contBotao["pady"]=20
        self.contBotao.pack()

        self.botaoFechar=Button(self.contBotao, text="Fechar")
        self.botaoFechar["width"]=10
        self.botaoFechar.pack(side=LEFT)
        #self.botaoFechar["command"]=       Criar função fechar programa

        self.nada=Label(self.contBotao, text="", width=40)
        self.nada.pack(side=LEFT)
        
        self.botaoOk = Button (self.contBotao, text = "Iniciar")
        self.botaoOk["width"]=10
        self.botaoOk.pack(side=RIGHT)
        self.botaoOk["command"] = pagPreDados



root = Tk()
root.title("Correli")
Application(root)
root.mainloop()
