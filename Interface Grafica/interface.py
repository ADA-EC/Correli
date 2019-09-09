from tkinter import *
import tkinter as tk
from tkinter import messagebox as msgb
import datetime	#Biblioteca utilizada para pegar o horário e data de início do teste
import serial
import sys  #Biblioteca usada para reiniciar o programa
import os   #Biblioteca usada para reiniciar o programa

arduino = serial.Serial('COM5', 9600)

class Application:
    def __init__(self, master=None):
            tempoinicio=datetime.datetime.now()

            #Caixas de diálogos presentes na primeira página de dados
            self.primeiroContainer = Frame(master)
            self.primeiroContainer["pady"] = 50
            self.primeiroContainer["padx"] = 100
            self.primeiroContainer.pack()

            self.widget = Frame(master)
            self.msg = Label(self.primeiroContainer, text="Qual o nome do arquivo?")
            self.msg["font"] = ("Calibri", "14", "bold")
            self.msg.pack(side=TOP)

            self.nome = Entry(self.primeiroContainer)
            self.nome["width"] = 30
            self.nome["font"] = ("Calibri", "10")
            self.nome.pack(side=TOP)

            #Função para receber o arduino e imprimir informações na listbox
            '''def imprime():
                    x=(arduino.readline().strip())
                    self.listbox.insert(END, x)
                    root.after(100, imprime)'''

            #Função para enviar dados para o Arduino
            def enviar(info):
                    arduino.write(info.encode())
                    
            def parametros():
                    if self.nome.get()=="":	#Teste para conferir que há algo escrito na primeira caixa de texto
                            msgb.showerror("ERRO!", "Insira o nome do arquivo!")
                    else:
                            self.paginanova=Toplevel() #cria nova pagina
                            self.paginanova.wm_geometry("300x130")
                            file=open(self.nome.get()+".txt", "w+") #Cria um arquivo com o nome escolhido pelo usuário

                            def intervalo_tempo():	#Função utilizada para saber qual botão o usuário apertou (tempo ou força)
                                    tempo=1
                                    intervalo(tempo)

                            def intervalo_forca():
                                    tempo=0
                                    intervalo(tempo)

                            def intervalo(tempo):

                                    def pagina_dados():
                                            '''
                                            Após definido o intervalo, a 2a página é fechada, a primeira é limpa e os dados gerados
                                            pela prensa são printados na tela da interface
                                            '''
                                            if self.intervaloesc.get()=="" or self.funesca.get()=="":
                                                    msgb.showerror("ERRO!", "Insira um valor!")

                                            elif float(self.intervaloesc.get())>float(self.funesca.get()):
                                                    print (self.intervaloesc.get()+"\n")
                                                    print (self.funesca.get()+"\n")
                                                    msgb.showerror("ERRO!", "Insira um intervalo menor do que o fundo de escala!")

                                            else:
                                                    def reiniciar():    #função que reinicia o programa
                                                        file.close()
                                                        python = sys.executable
                                                        os.execl(python, python, *sys.argv)

                                                    def fechar():       #função que fecha o programa
                                                        file.close()
                                                        root.destroy()
                                                        sys.exit()

                                                        end = '0'
                                                        enviar(end)
                                                        
                                                    if tempo == 1:
                                                        modo = 't'
                                                    else: 
                                                        modo = 'f'

                                                    interv=self.intervaloesc.get()
                                                    fundo_escala=self.funesca.get()
                                                    
                                                    info = modo + "," +str(interv) + "," + str(fundo_escala)+"\n"
                                                    enviar(info)
                                                    
                                                    self.containerlist = Frame(master)
                                                    self.containerlist["pady"] = 1
                                                    self.containerlist["padx"] = 1
                                                    self.containerlist.pack(fill=BOTH, expand=1)
                                                    
                                                    self.containerbotao = Frame(master)
                                                    self.containerbotao["pady"] = 1
                                                    self.containerbotao["padx"] = 1
                                                    self.containerbotao.pack()
                                                        
                                                    self.botaoreiniciar = Button(self.containerbotao, text="Reiniciar",)
                                                    self.botaoreiniciar.pack(side=RIGHT)
                                                    self.botaoreiniciar["command"]=reiniciar

                                                    self.botaofechar = Button(self.containerbotao, text="Fechar",)
                                                    self.botaofechar.pack(side=LEFT)
                                                    self.botaofechar["command"]=fechar
                                                    
                                                    interv=self.intervaloesc.get()
                                                    fundo_escala=self.funesca.get()
                                                    self.paginanova.destroy()
                                                    self.primeiroContainer.destroy()
                                                    self.listbox=Listbox(self.containerlist, width=50, height=20)

                                                    

                                                    self.listbox.insert(END, 'Projeto Correli')
                                                    self.listbox.insert(END, 'Horário de início do ensaio: '+str(tempoinicio))

                                                    file.write("Projeto Correli\n")
                                                    file.write("Horário de início do ensaio: "+str(tempoinicio)+"\n")

                                                    if tempo==0:
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
                                                    #root.after(100, imprime)

                                                    self.scrollbar = Scrollbar(self.containerlist)
                                                    self.scrollbar.pack(side=RIGHT, fill=Y)
                                                    self.listbox.config(yscrollcommand=self.scrollbar.set)
                                                    self.scrollbar.config(command=self.listbox.yview)
                                                    self.listbox.pack(fill=BOTH, expand=1)

                                    #Mensagens e botões presentes na 2a página da interface
                                    self.botaofinal = Button(self.paginanova, text="ENTER")
                                    self.botaofinal.pack(side=BOTTOM)
                                    self.botaofinal["command"]=pagina_dados

                                    self.configuracao.destroy()
                                    self.botaotempo.destroy()
                                    self.botaoforca.destroy()

                                    self.intervaloesc = Entry(self.paginanova)
                                    self.intervaloesc.pack(side=BOTTOM)

                                    self.mensagem = Label(self.paginanova, text="Insira o intervalo")
                                    self.mensagem["font"] = ("Calibri", "10")
                                    self.mensagem.pack(side=BOTTOM)


                                    self.funesca = Entry(self.paginanova)
                                    self.funesca.pack(side=BOTTOM)

                                    self.mensagem2 = Label(self.paginanova, text="Insira o fundo de escala")
                                    self.mensagem2["font"] = ("Calibri", "10")
                                    self.mensagem2.pack(side=BOTTOM)

                                    self.mensagem_lembrete = Label(self.paginanova, text="SOMENTE NÚMEROS!")
                                    self.mensagem_lembrete["font"] = ("Calibri", "10")
                                    self.mensagem_lembrete.pack(side=BOTTOM)
                                    
                                    


                            #Mensagens e botões presentes na 2a página da interface
                            self.configuracao = Label(self.paginanova, text="Descreva o modo de operação")
                            self.configuracao["font"] = ("Calibri", "12", "bold")
                            self.configuracao.pack(side=TOP)

                            self.botaotempo = Button(self.paginanova, text="Por tempo")
                            self.botaotempo.pack(side=LEFT)
                            self.botaotempo["command"]=intervalo_tempo

                            self.botaoforca = Button(self.paginanova, text="Por Força")
                            self.botaoforca.pack(side=RIGHT)
                            
                            self.botaoforca["command"]=intervalo_forca
                            
                            start = 'oi'
                            enviar(start)
            
            self.botaoConfirm=Button(self.primeiroContainer, text="Criar arquivo")
            self.botaoConfirm["width"]=10
            self.botaoConfirm.pack(side=BOTTOM)
            
            self.botaoConfirm["command"]=parametros #Quando é apertado o botão, o código vai para parâmetros, que cria outra página
            self.botaoConfirm.pack()


root = Tk()
root.title("Correli")
Application(root)
root.mainloop()
