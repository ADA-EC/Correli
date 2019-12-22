# Projeto Correli
Projeto desenvolvido pelo Grupo ADA - Projetos em Engenharia de Computação em parceiria com o Departamento de Estruturas da EESC - USP.

## Configuração
É necessário que um Arduino esteja conectado a uma porta USB do computador para que o código seja executado corretamente.

### Ubuntu
Para executar o código no sistesma operacional Ubuntu (os testes foram realizados no Ubuntu 18.04), é necessário possuir a versão 3 do Python, e instalar as seguintes bibliotecas:

- tkinter
- pyserial 
- serial.tools.list_ports

$ python3 interface.py

### Windows
No WIndows, basta rodar o executável previamente criado com Pyinstaller que o programa será executado normalmente. Para executar o código a partir do aquivo Python, é necessário possuir as mesmas bibliotecas e a versão do Python exigida para execução em Linux.

## Descrição do Projeto
Criação de um sistema que integre uma prensa hidráulica e uma câmera que tira fotos do corpo de prova que é submetido ao ensaio na prensa. Por meio de uma interface gráfica, o usuário escolhe o modo de operação da camêra (por tempo ou por intervalo de força realizado pela prensa) para tirar a foto. Os dados do ensaio e as tensões nos momentos em que as fotos s
ão tiradas são registrados em um arquivo que fica salvo no final da execução. 

### Prensa Hidráulica
A prensa possui uma saída de tensão que pode ser relacionada com a força que está sendo aplicada em um corpo de prova. Essa tensão pode variar entre -10 volts e 10 volts, a princípio iremos considerar apenas os valores positivos (0-10 volts), tendo uma precisão de 4 casas decimais na leitura dessa tensão e, por fim, podemos convertê-la para força, uma vez que a cada volt temos 25 toneladas sendo aplicado. 

### Câmera
Já a câmera (Canon EOS 30D), possui um função de acionamento remoto, com isso, podemos tirar uma foto sem necessariamente pressionarmos o botão. A ideia do projeto é integrar as fotos tiradas com a força que está sendo aplicada naquele momento e criar um arquivo “.txt”  contendo essa informações. O acionamento da câmera pode ser regulado tanto pelo tempo, tirando fotos em certos intervalos de tempo, quanto por certo intervalos de forças.

### Interface Gráfica
A interface gráfica foi feita em Python. Ela permite que o usuário crie um arquivo com o nome escolhido por ele, escolha a forma de acionamento da câmera (por tempo ou pressão) e defina o intervalo que seja mais conveniente a ele. Então é iniciado o programa, ele se conecta com o código criado para o Arduino Nano e, então, aparece na tela os valores obtidos da pressão que a prensa hidráulica exerce no exato momento em que a foto é tirada. Para utiliza-lá é preciso que o usuário possua tanto o [Python](https://www.python.org/download/releases/3.0/) quanto a biblioteca [PySerial](https://github.com/pyserial/pyserial) instaladas. 

### Prototipagens
O esquemático apresenta o circuito com Arduino, Relé e conversor AD de maneira que seja possível o acionamento da câmera em intervalos especificados pelo usuário de tempo ou tensão.
Simulou-se a prensa para que fosse possível realizar alguns testes. Para isso, utilizou-se 2 potenciômetros conectados, em que um limita a tensão recebida pela fonte (que é de 12V) em até 10V e o segundo simula as tensões que seriam enviadas pela prensa hidráulica.
A câmera é conectada nos terminais do relé indicados no esquemático. Ela tira fotos quando o circuito é fechado pelo relé, em intervalos de tempo ou tensão definidos pelo código.
![Imagem do primeiro esquemático](https://user-images.githubusercontent.com/40308772/58904498-08340780-86de-11e9-8d0f-73c93ed03429.png)

No segundo modelo feito, utilizou-se um Arduino Nano ao invés do Uno. Também não foi necessário utilizar 2 potenciômetros para simular a prensa, apenas 1. Abaixo está o esquemático do segundo modelo.
![Imagem do segundo esquemático](https://user-images.githubusercontent.com/40308772/65969281-e011a680-e43a-11e9-9a54-cd1cd2966755.jpeg)

