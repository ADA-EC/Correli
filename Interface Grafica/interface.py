from tkinter import *
import tkinter as tk
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

arduino = serial.Serial(arduino_ports[0])


#Pagina inicial da interface
class Application:
    def __init__(self, master=None):
        tempoinicio=datetime.datetime.now() #Trecho utilizado para salvar o horário atual em que o programa foi aberto, para salvá-lo como dado

        #Caixas de diálogos presentes na página inicial
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 50
        self.primeiroContainer["padx"] = 100
        self.primeiroContainer.pack()

        #Caixa de mensagem da página inicial
        self.widget = Frame(master)
        self.msg = Label(self.primeiroContainer, text="Qual o nome do arquivo?")
        self.msg["font"] = ("Calibri", "14", "bold")
        self.msg.pack(side=TOP)

        self.nome = Entry(self.primeiroContainer)
        self.nome["width"] = 30
        self.nome["font"] = ("Calibri", "10")
        self.nome.pack(side=TOP)


        #Função para enviar dados para o Arduino
        def enviar(info):
            arduino.write(info.encode())

        #Segunda página da interface
        def parametros():
            if self.nome.get()=="":	#Teste para conferir que há algo escrito no nome do arquivo a ser gerado
                    msgb.showerror("ERRO!", "Insira o nome do arquivo!")
            else:
                self.paginanova=Toplevel() #cria nova pagina
                self.paginanova.wm_geometry("350x300")
                file=open(self.nome.get()+".txt", "w+") #Cria um arquivo com o nome escolhido pelo usuário

                #Containers para dividir de uma maneira melhor os elementos da página                
                self.cont1 = Frame (self.paginanova)
                self.cont1["pady"]=20
                self.cont1["padx"]=30
                self.cont1.pack()

                self.cont2 = Frame (self.paginanova)
                self.cont2["pady"]=20
                self.cont2["padx"]=10
                self.cont2.pack()

                self.cont3 = Frame (self.paginanova)
                self.cont3["pady"]=20
                self.cont3["padx"]=10
                self.cont3.pack()

                self.cont4 = Frame (self.paginanova)
                self.cont4["pady"]=20
                self.cont4["padx"]=10
                self.cont4.pack()

                def pagPreDados():  #Página que inicia a câmera
                    

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
                            print("oi")
                        

                        '''interv=self.intervaloesc.get()
                        fundo_escala=self.funesca.get()'''

                        #Comandos utilizados para enviar ao documento criado os dados utilizados pelo usuário 
                        '''info = modo + "," +str(interv) + "," + str(fundo_escala)+"\n"'''
                        enviar(info)

                        '''
                        Criação dos containers presentes na página de dados e posicionamento dos mesmos
                        '''
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
                        
                        '''interv=self.intervaloesc.get()
                        fundo_escala=self.funesca.get()'''
                        self.paginanova.destroy()
                        self.primeiroContainer.destroy()
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


                    #Página para iniciar o programa com os dados já inseridos
                    if var.get() == 1:  #Condição utilizada para salvar o modo de medição escolhido pelo usuário
                        modo = 't'
                        print("tempo")
                    else: 
                        modo = 'f'

                    
                    if self.intervaloesc.get()=="" or self.funesca.get()=="":
                        #Teste para conferir que o usuário não deixou nenhum campo de preenchimento em branco
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
                        self.paginanova.wm_geometry("300x150")
                        self.cont = Frame (self.paginanova)
                        self.cont["pady"]=50
                        self.cont["padx"]=10
                        self.cont.pack()

                        self.msgIni = Label (self.cont, text = "Aperte o botão para iniciar o programa")
                        self.msgIni["font"] = ("Calibri", "12", "bold")
                        self.msgIni.pack()

                        self.botIni = Button (self.cont, text = "Iniciar")
                        self.botIni.pack(side = BOTTOM)
                        self.botIni["command"] = pagina_dados
                        


            #Mensagens e botões presentes na 2a página da interface para adicionar os dados

            #COLOCAR UM IF PARA ARQUIVO JA EXISTENTE, PREENCHER TODOS OS CAMPOS E DEIXAR INVIÁVEL PARA USUÁRIO MEXER!
            self.configuracao = Label(self.cont1, text="Descreva o modo de operação")
            self.configuracao["font"] = ("Calibri", "12")
            self.configuracao.pack(side=TOP)

            #Função para escolher apenas uma opção entre força e tempo
            var = tk.IntVar()
            def tipo():
                print (str(var.get()))
            
            self.Tempo = Radiobutton(self.cont1, text = "Tempo", variable = var, value = 1, command = tipo)
            self.Tempo.pack (side = LEFT)
            self.Forca = Radiobutton(self.cont1, text = "Força", variable = var, value = 2, command = tipo)
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

            self.botaoArq = Button (self.cont4, text = "Escolher arquivo")
            self.botaoArq.pack(side=RIGHT)
            #self.botaoArq["command"]=   PROCURAR ARQUIVO PARA COMPLETAR OS CAMPOS AUTOMATICAMENTE! -->SHIFT
            
                        
        self.botaoConfirm=Button(self.primeiroContainer, text="Criar arquivo")
        self.botaoConfirm["width"]=10
        self.botaoConfirm.pack(side=BOTTOM)
        self.botaoConfirm["command"]=parametros #Quando é apertado o botão, o código vai para parâmetros, que cria outra página


root = Tk()
root.title("Correli")
Application(root)
root.mainloop()
