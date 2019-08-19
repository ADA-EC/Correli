import serial
from tkinter import *

arduino = serial.Serial('COM8', 9600)


def leitura():
    texto = arduino.readline().strip()
    listbox.insert(END, texto)
    janela.after(10,leitura)


janela = Tk()

listbox = Listbox(janela)
listbox.pack()

janela.after(10, leitura)

'''
for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)
    listbox.insert(END,arduino.readline().strip())
'''
janela.mainloop
