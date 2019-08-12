from tkinter import *
import tkinter as tk
from tkinter import messagebox as msgb
import datetime	#Biblioteca utilizada para pegar o horário e data de início do teste


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

						elif self.intervaloesc.get()>self.funesca.get():
							msgb.showerror("ERRO!", "Insira um intervalo menor do que o fundo de escala!")

						else:
							interv=self.intervaloesc.get()
							fundo_escala=self.funesca.get()
							self.paginanova.destroy()
							self.primeiroContainer.destroy()
							self.listbox=Listbox(root, width=70, height=50)

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

							file.write("Intervalo escolhido: "+str(interv)+"\n\n")


							oi="batata"
							for i in range(1000):
								self.listbox.insert(END, oi)
								file.write(oi+"\n")

							
							#Todos os dados obtidos são colocados no arquivo criado com o nome escolhido pelo usuário
							file.close()

							self.scrollbar = Scrollbar(root)
							self.scrollbar.pack(side=RIGHT, fill=Y)
							self.listbox.config(yscrollcommand=self.scrollbar.set)
							self.scrollbar.config(command=self.listbox.yview)
							self.listbox.pack()

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
				self.botaotempo.place(x=0, y=25)
				self.botaotempo["command"]=intervalo_tempo

				self.botaoforca = Button(self.paginanova, text="Por Força")
				self.botaoforca.place(x=200, y=25)
				self.botaoforca["command"]=intervalo_forca

				
		
		self.botaoConfirm=Button(self.primeiroContainer, text="Criar arquivo")
		self.botaoConfirm["width"]=10
		self.botaoConfirm.pack(side=BOTTOM)
		
		self.botaoConfirm["command"]=parametros #Quando é apertado o botão, o código vai para parâmetros, que cria outra página
		self.botaoConfirm.pack()


root = Tk()
root.title("Correli")
Application(root)
root.mainloop()