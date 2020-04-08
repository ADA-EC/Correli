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
        

        #Segunda página da interface
        def parametros():
            if not self.listaPortas.curselection():
                msgb.showerror("Erro!", "Escolha uma porta do Arduino!")
            else:
                arduino = serial.Serial(self.listaPortas.get(self.listaPortas.curselection()))  #Utiliza o Arduino selecionado pelo usuário

                #Função para enviar dados para o Arduino
                def enviar(info):
                    arduino.write(info.encode())
                
                
                file = None
                while file is None:
                    #Salvamento do arquivo em um local da pasta desejado pelo usuário
                    files = [('Text Document', '*.txt'), 
                             ('Python Files', '*.py'),
                             ('All Files', '*.*')]      #Tipos de arquivos possíveis para salvar
                    file = asksaveasfile(filetypes = files, defaultextension = files)

                
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
                    enviar(end)
                    file.close()
                    root.destroy()
                    sys.exit()

                #Comandos utilizados para enviar ao documento criado os dados utilizados pelo usuário
                enviar(info)

                self.cont.destroy()

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
                self.cont1.destroy()
                self.cont2.destroy()
                self.cont3.destroy()
                self.cont4.destroy()

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

                    

                #self.primeiroContainer.destroy()
                

        
        
        #Caixas de diálogos presentes na página inicial
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 20
        self.primeiroContainer["padx"] = 20
        self.primeiroContainer.pack()

        num_arduinos=len(arduino_ports)    #Variável que contém o número de arduinos linkados na máquina
        i=0

        '''if num_arduinos==0:
            msgb.showerror("ERRO!", "Não existem Arduinos conectados a esse computador!")
            root.destroy()
            sys.exit()'''

        self.listaPortas = Listbox(self.primeiroContainer, width = 20, heigh = 10)
        while i<num_arduinos:   #Lista todas as portas com Arduino presentes
            self.listaPortas.insert(END, arduino_ports[i])
            i+=1
        self.listaPortas.pack(side=LEFT)
                        
        self.botaoConfirm=Button(self.primeiroContainer, text="Criar arquivo")
        self.botaoConfirm["width"]=10
        self.botaoConfirm.pack(side=RIGHT)
        self.botaoConfirm["command"]=parametros #Quando é apertado o botão, o código vai para parâmetros, que cria outra página

        

        #Containers da segunda página para dividir de uma maneira melhor os elementos da página                
        self.cont1 = Frame (master)
        self.cont1["pady"]=20
        self.cont1["padx"]=30
        self.cont1.pack()

        self.cont2 = Frame (master)
        self.cont2["pady"]=20
        self.cont2["padx"]=10
        self.cont2.pack()

        self.cont3 = Frame (master)
        self.cont3["pady"]=20
        self.cont3["padx"]=10
        self.cont3.pack()

        self.cont4 = Frame (master)
        self.cont4["pady"]=20
        self.cont4["padx"]=10
        self.cont4.pack()

        #Mensagens e botões presentes na 2a página da interface para adicionar os dados

        #COLOCAR UM IF PARA ARQUIVO JA EXISTENTE, PREENCHER TODOS OS CAMPOS E DEIXAR INVIÁVEL PARA USUÁRIO MEXER!
        self.configuracao = Label(self.cont1, text="Descreva o modo de operação")
        self.configuracao["font"] = ("Calibri", "12")
        self.configuracao.pack(side=TOP)

        #Função para escolher apenas uma opção entre força e tempo
        var = tk.IntVar()
        
        self.Tempo = Radiobutton(self.cont1, text = "Tempo", variable = var, value = 1)
        self.Tempo.pack (side = LEFT)
        self.Forca = Radiobutton(self.cont1, text = "Força", variable = var, value = 2)
        self.Forca.pack(side = RIGHT)

        self.msgEscala = Label (self.cont2, text = "Insira o fundo de escala")
        self.msgEscala["font"] = ("Calibri", "12")
        self.msgEscala.pack(side=LEFT)

        self.funesca = Entry(self.cont2)
        self.funesca.pack(side=RIGHT)

        self.mensagem = Label(self.cont3, text="Insira o intervalo (ms ou t)")
        self.mensagem["font"] = ("Calibri", "12")
        self.mensagem.pack(side=LEFT)

        self.intervaloesc = Entry(self.cont3)
        self.intervaloesc.pack(side=RIGHT)

        self.botaoOk = Button (self.cont4, text = "Ok")
        self.botaoOk["width"]=10
        self.botaoOk.pack(side=LEFT)
        self.botaoOk["command"] = pagPreDados

        self.botaoArq = Button (self.cont4, text = "Escolher configuração")
        self.botaoArq.pack(side=RIGHT)
        #self.botaoArq["command"]=   PROCURAR ARQUIVO PARA COMPLETAR OS CAMPOS AUTOMATICAMENTE! -->SHIFT



root = Tk()
root.title("Correli")
Application(root)
root.mainloop()
