import serial

arduino = serial.Serial('COM3',9600) #Definida a variavel que se comunicara com o arduino

#---------- Funcao que envia para o Arduin o modo de operacao desejado -----------------------#

def send_command(modo): 
    aux = str(modo)
    arduino.write(aux.encode()) #Funcao que envia uma string para o arduino
  

def comando(opcao):
    
    if (opcao == 1):    
        send_command("1")#Envia "1" para o arduino; modo por forca

    elif (opcao == 1 ):
        send_command("2")#Envia "2" para o arduino; modo por tempo
        
#---------- Recebe do arduino que a operacao pode comecar ------------------------------------#
        
aux = "0" 

while(aux == "0"):

    iniciar = (arduino.readline().strip()) #Le se o arduino ja mandou sinal para iniciar

    if(iniciar == "comecou"):
        aux = "vazio"       
    
#---------- Coleta o mode de operacao que o usuario deseja utilizar e manda para o arduino ---#

print("\nDigite 1 para modo por forca, digite 2 para modo por tempo\n\n")

opcao = int(input("Digite um valor: "))

comando(opcao)

#---------- Loop que recebe as informacoes enviadas pelo arduino -----------------------------#

if(opcao == 1): #Por forca
    
    while(1): 
        
        tensaoReal = (arduino.readline().strip())#Funcao para receber informações do arduino
        tensaoADS = (arduino.readline().strip())
        forca = (arduino.readline().strip())
        aux_menos_tensaoADS = (arduino.readline().strip())
        
        print("\nTensao real: ",tensaoReal)
        print("\nTensao ADS",tensaoADS)
        print("\nForca(em toneladas): ",forca)
        print("\nAux-tensaoADS: ",aux_menos_tensaoADS)

        
elif(opcao == 2): #Por tempo

    while(1): 
        tempo = (arduino.readline().strip())#Funcao para receber informações do arduino
        tempo_menos_temp_ant = (arduino.readline().strip())
        
        print("\nTempo: ",tempo)
        print("Tempo - temp_ant: ",tempo_menos_temp_ant)

#OBS: Os nomes das variaveis acima foram escolhidas com base nos nomes
#     presentes no programa enviado ao arduino (arquivo ".ino").
