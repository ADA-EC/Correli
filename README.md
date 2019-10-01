# Correli
Projeto desenvolvido pela ADA em parceiria com o departamento de Estruturas da EESC

## Descrição
Criação de um sistema que integre uma prensa hidráulica e uma câmera. 

### Prensa Hidráulica
A prensa possui uma saída de tensão que pode ser relacionada com a força que está sendo aplicada em um corpo de prova. Essa tensão pode variar entre -10 volts e 10 volts, a princípio iremos considerar apenas os valores positivos (0-10 volts), tendo uma precisão de 4 casas decimais na leitura dessa tensão e, por fim, podemos convertê-la para força, uma vez que a cada volt temos 25 toneladas sendo aplicado. 

### Câmera
Já a câmera (Canon EOS 30D), possui um função de acionamento remoto, com isso, podemos tirar uma foto sem necessariamente pressionarmos o botão. A ideia do projeto é integrar as fotos tiradas com a força que está sendo aplicada naquele momento e criar um arquivo “.txt”  contendo essa informações. O acionamento da câmera pode ser regulado tanto pelo tempo, tirando fotos em certos intervalos de tempo, quanto por certo intervalos de forças.

### Junção dos códigos
A implementação do código foi feita de maneira que o usuário escolhe entre o acionamento da câmera a cada intervalo de tempo (que seria de 1s) e o acionamento da mesma a cada intervalo de tensão. Para isso, o usuário tem que digitar 1 caso queira o acionamento por tempo ou 2 caso queira o acionamento por intervalo de tensão.

### Esquemático
O esquemático apresenta o circuito com Arduino, Relé e conversor AD de maneira que seja possível o acionamento da câmera em intervalos especificados pelo usuário de tempo ou tensão.
Simulou-se a prensa para que fosse possível realizar alguns testes. Para isso, utilizou-se 2 potenciômetros conectados, em que um limita a tensão recebida pela fonte (que é de 12V) em até 10V e o segundo simula as tensões que seriam enviadas pela prensa hidráulica.
A câmera é conectada nos terminais do relé indicados no esquemático. Ela tira fotos quando o circuito é fechado pelo relé, em intervalos de tempo ou tensão definidos pelo código.
![Imagem do primeiro esquemático](https://user-images.githubusercontent.com/40308772/58904498-08340780-86de-11e9-8d0f-73c93ed03429.png)

No segundo modelo feito, utilizou-se um Adruino Nano ao invés do Arduino Uno original. Também não foi necessário utilizar 2 potenciômetros para simular a prensa, apenas 1. Abaixo está o esquemático do segundo modelo.
![Imagem do segundo esquemático](https://user-images.githubusercontent.com/40308772/65969281-e011a680-e43a-11e9-9a54-cd1cd2966755.jpeg)

### Interface Gráfica
A interface gráfica foi feita em Python. Ela permite que o usuário crie um arquivo com o nome escolhido por ele, escolha a forma de acionamento da câmera (por tempo ou pressão) e defina o intervalo que seja mais conveniente a ele. Então é iniciado o programa, ele se conecta com o código criado para o Arduino Nano e, então, aparece na tela os valores obtidos da pressão que a prensa hidráulica exerce no exato momento em que a foto é tirada.