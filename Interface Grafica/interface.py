from tkinter import *
import tkinter as tk
from tkinter import messagebox as msgb


class Application:
	def __init__(self, master=None):
		self.primeiroContainer = Frame(master)
		self.primeiroContainer["pady"] = 10

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
			if self.nome.get()=="":
				msgb.showerror("ERRO!", "Insira o nome do arquivo!")
			else:
				self.paginanova=Toplevel() #cria nova pagina
				self.paginanova.wm_geometry("300x150")
				file=open(self.nome.get()+".txt", "w+")

				def intervalo():

					def pagina_dados():
						if self.intervaloesc.get()=="":
							msgb.showerror("ERRO!", "Insira um intervalo!")
						else:
							self.pagina_dados=Toplevel() #cria nova pagina
							self.pagina_dados.wm_geometry("1000x1000")
							self.paginanova.destroy()

							


					self.botaofinal = Button(self.paginanova, text="ENTER")
					self.botaofinal.pack(side=BOTTOM)
					self.botaofinal["command"]=paginadados

					self.intervaloesc = Entry(self.paginanova)
					self.intervaloesc.pack(side=BOTTOM)

					self.mensagem_lembrete = Label(self.paginanova, text="SOMENTE NÚMEROS!")
					self.mensagem_lembrete["font"] = ("Calibri", "10")
					self.mensagem_lembrete.pack(side=BOTTOM)

					self.mensagem = Label(self.paginanova, text="Insira o intervalo")
					self.mensagem["font"] = ("Calibri", "10")
					self.mensagem.pack(side=BOTTOM)



				self.oi = Label(self.paginanova, text="Descreva o modo de operação")
				self.oi["font"] = ("Calibri", "12", "bold")
				self.oi.pack(side=TOP)

				self.botaotempo = Button(self.paginanova, text="Por tempo")
				self.botaotempo.place(x=0, y=25)
				self.botaotempo["command"]=intervalo

				self.botaoforca = Button(self.paginanova, text="Por Força")
				self.botaoforca.place(x=200, y=25)
				self.botaoforca["command"]=intervalo

				
		
		self.botaoConfirm=Button(self.primeiroContainer, text="Criar arquivo")
		self.botaoConfirm["width"]=10
		self.botaoConfirm.pack(side=BOTTOM)
		
		self.botaoConfirm["command"]=parametros
		self.botaoConfirm.pack()



	



root = Tk()
root.title("Correli")
Application(root)
root.mainloop()