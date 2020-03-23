'''
Considerações gerais:
1. Arquivos .json e .xml guardam informações em formato de texto.
2. Pesquisando sobre qual usar, optei pelo JSON por ser esteticamente
melhor e, consequentemente mais fácil de ler. Além disso, empresas como Google
e Yahoo! utilizam JSON, logo serve para nossas necessidades.
3. Para mexer com esse tipo de arquivo, trabalhamos com as rotinas padrão 
do Python para arquivos, porém acrescentamos alguns comandos como json.dump()
e json.load().
4. Para usarmos essas funções, precisamos importar a biblioteca "json", que
aparentemente vem padrão com o Python.

OBS: O código abaixo, na realidade, são dois:
O primeiro serve para criar arquivos .json a partir de uma biblioteca criada por nós;
O segundo serve para extrair as informações de um arquivo .json - preexistente.  
'''

import json

#Modo para criação e escrita em arquivos .json

#Criação da biblioteca e preenchimento
data = {}
data['arquivo'] = 'padrao'
data['modo'] = 'f'
data['intervalo'] = 2500
data['fundo_escala'] = 200

arquivo = open('nome.json', 'w')

#Adapta a biblioteca em python para o formato .json e escreve no arquivo
json.dump(data, arquivo)

arquivo.close()

'''

#Modo para leitura de arquivos .json

json_file = open('nome.json', 'r')

#Importa os dados do arquivo .json para uma biblioteca em pyhton
data = json.load(json_file)

json_file.close()

print(data)

'''

