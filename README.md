# Correli
Projeto desenvolvido pela ADA em parceiria com o departamento de Estruturas da EESC

## Descrição
Criação de um sistema que integre uma prensa hidráulica e uma câmera. 

### Prensa Hidráulica
A prensa possui uma saída de tensão que pode ser relacionada com a força que está sendo aplicada em um corpo de prova. Essa tensão pode variar entre -10 volts e 10 volts, a princípio iremos considerar apenas os valores positivos (0-10 volts), tendo uma precisão de 4 casas decimais na leitura dessa tensão e, por fim, podemos convertê-la para força, uma vez que a cada volt temos 25 toneladas sendo aplicado. 

### Câmera
Já a câmera (Canon EOS 30D), possui um função de acionamento remoto, com isso, podemos tirar uma foto sem necessariamente pressionarmos o botão. A ideia do projeto é integrar as fotos tiradas com a força que está sendo aplicada naquele momento e criar um arquivo “.txt”  contendo essa informações. O acionamento da câmera pode ser regulado tanto pelo tempo, tirando fotos em certos intervalos de tempo, quanto por certo intervalos de forças.
