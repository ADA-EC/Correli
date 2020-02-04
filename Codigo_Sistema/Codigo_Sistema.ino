/*
 *         ****************  CONSIDERAÇÕES GERAIS  ****************
 * 
 * Para o funcionamento do código, é necessário instalar e importar
 * a biblioteca "Adafruit_ADS1X15.h". Ela tem o propósito de permitir a
 * comunicação entre arduino e o conversor analógico-digital (ADS1115).
 * 
 * Um detalhe importante sobre a estrutura do programa é a não utilização
 * da rotina void loop() como mantenedora dos loops do código. Optamos por
 * controlar nós mesmos os loops por meio de funções específicas, como 
 * modo_forca() e modo_tempo().
 */
  
#include <Adafruit_ADS1015.h>
#define valueModoTensao 1
#define OK 1
#define ERRO 0

float intervalo_tempo; 
float intervalo_forca;

int16_t sensorValue;
float tensaoADS;
float tensaoReal;
float tensaoAnt = 0.0;
float forca;
float forcaAnt = 0.0;

int cont = 1;
int porta_rele = 10;

unsigned long tempo;
unsigned long tempoAnt = 0;
float fundo_escala; 

/*
 * Variáveis utilizadas para auxiliar no recebimento das configurações 
 * de funcionamento do programa - dados enviados pela interface gráfica.
 */
char modo = '0';
String intervaloS = "";
String fundoS = "";
float intervalo;

/*
 * Configuração do endereço (Address) do ADS1115 como sendo o GND,
 * indicado por "0x48".
 */ 
Adafruit_ADS1115 ads(0x48);

void setup() {

  Serial.begin(9600);
  
  pinMode(porta_rele, OUTPUT);
  digitalWrite(porta_rele, HIGH);
  
  ads.begin();

  //Receber as configurações de funcionamento do programa 
  recebe_dados();
  converte_dados();

  //O programa funcionará conforme o modo acionado - força (f) ou tempo (t)
  if(modo == 'f')
  {
    Serial.println("IMAGEM       TENSAO         FORCA         FORCA_P            TENSAO_P            INTERVALO");

    intervalo_forca = intervalo;
    modo_forca();
  }
  else if(modo == 't')
  {
    Serial.println("IMAGEM       TENSAO         FORCA         FORCA_P            TENSAO_P            INTERVALO");
    intervalo_tempo = intervalo;
    modo_tempo();      
  }
}

int verificar_comecar()
{
  char verifica = '0';
  
  while(verifica == '0') //A interface deve mandar um char qualquer para comecar.
  {
    if(Serial.available()>0)
      verifica = Serial.read();       
  }

  Serial.println(verifica);
  return OK;
}

/* 
 *  Os dados enviados pela interface gráfica estão organizados em uma estrutura 
 *  fixa e muito bem definida: "modo,intervalo,fundo_de_escala", em uma única string. 
 *  Para facilitar a coleta desses dados, decidimos analisar char por char enviado
 *  pela interface e, em seguida, armazena-los em strings. 
 *  No caso do modo de operacao, havia somente duas opcoes: tempo ou forca, que foram
 *  representadas, respectivamente, por 't' e 'f'. Essa informacao foi armazenada em
 *  um unico char chamado "modo".
 *  O intervalo de operacao e o fundo de escala foram armazenados, respectivamente, nas
 *  strings "intervaloS" e "fundoS".      
 */
void recebe_dados()
{
  char caractere = '0';
  int aux_modo = OK;
  int aux_intervalo = ERRO;
  int aux_fundo = ERRO;
  int conta_virgula = 0;
  
  while(caractere != '\n')
  {
    if(Serial.available())
    {
      caractere = Serial.read();

      if(caractere == ',')
        conta_virgula++;

      if(conta_virgula == 2)
      {
        aux_intervalo = ERRO;
        aux_fundo = OK; 
      }
        
      if(caractere != ',' && aux_modo == OK && aux_intervalo == ERRO && aux_fundo == ERRO)
      {
        modo = caractere; 
        aux_modo = ERRO;
        aux_intervalo = OK;   
      }

      if(caractere != ',' && aux_modo == ERRO && aux_intervalo == OK && aux_fundo == ERRO && conta_virgula != 0)
      {
        intervaloS.concat(caractere);
      }

      if(caractere != ',' && aux_modo == ERRO && aux_intervalo == ERRO && aux_fundo == OK)
      {
        fundoS.concat(caractere);
      }
    }
  }
}

 /* 
 *  A funcao converte_dados() converte o intervalo de operacao e o fundo escala 
 * de uma string - intervaloS e fundoS - para um numero flutuante (float). 
 */
 
void converte_dados()
{
  intervalo = intervaloS.toFloat();
  fundo_escala = fundoS.toFloat();
}

/*                  Comtário sobre as funções que vêm a seguir
 * A funções modo_tempo() e modo_forca funcionam de forma análoga,conforme
 * a escolha feita pelo usuário do modo de operação do programa.
 * Essas funções são responsáveis por manter o código funcionando por tempo
 * indeterminado (loop) até que uma condição de parada (int parada) se torne
 * verdadeira, isto é, igual a 1 - isso é modificado pela rotina receber_parada().
 * Enquanto o programa funciona, as rotinas abaixo calculam a força exercida
 * pela prensa no corpo de prova por meio de calculoForca() e, conforme passa o 
 * intervalo de tempo ou de força pré determinado, acionam e desligam o relé - tarefa
 * executada por verificarTempo() ou verificarForca().
 */
 
void modo_tempo()
{
  int parada = 0;
  
  while(!parada)
  {
    calculoForca();
    verificarTempo();
    parada = receber_parada();
  }
}

void modo_forca()
{
  int parada = 0;
  
  while(!parada)
  {
    calculoForca();
    verificarForca();
    parada = receber_parada();
  }
}


void calculoForca(){
  
  sensorValue = ads.readADC_SingleEnded(1);           //Prensa conectada na porta 1
  tensaoADS = sensorValue * (0.1875 /1000);           //Ler o que vem do ADS; 0<=tensaoADS<=5V
  tensaoReal = tensaoADS*2;                           /*A tensão que vem da prensa é duas vezes 
                                                      maior que a que chega no arduino*/
  forca = map_f(sensorValue,0,65536,0,fundo_escala);

  if(forca >= fundo_escala)//Caso ocorra algum erro
      Serial.print("0");
}

void verificarForca(){

  calculoForca();

  //OBS: forcaAnt é inicializada com forcaAnt = 0.0
  //Verificamos se o intervalo de força já foi percorrido para podermos acionar o relé novamente
  if((forca - forcaAnt)>= intervalo_forca){

    Serial.print(cont);
    calculoForca();
    Serial.print("            ");
    Serial.print(tensaoReal,5);
    Serial.print("            ");
    Serial.print(forca,5); //FORCA ANTERIOR
  
    digitalWrite(porta_rele, LOW);//ACIONAMENTO DO RELE

    calculoForca();
    
    Serial.print("            ");
    Serial.print(forca,5);//FORCA POSTERIOR
    
    Serial.print("            ");
    Serial.print(tensaoReal,5); //Tensão Real
    
    Serial.print("            ");
    Serial.println(forca-forcaAnt); //Invervalo
    
    forcaAnt = forca;

    cont++;
  }else{
    digitalWrite(porta_rele, HIGH); //desliga o rele
  }
}

void verificarTempo(){
  
  tempo = millis();

  //Verificamos se o intervalo de tempo já foi percorrido para podermos acionar o relé novamente
  if((tempo - tempoAnt) >= intervalo_tempo){

    Serial.print(cont);

    calculoForca();
    Serial.print("            ");
    Serial.print(tensaoReal,4);
    Serial.print("            ");
    Serial.print(forca,4); //FORCA ANTERIOR
  
    digitalWrite(porta_rele, LOW);//ACIONAMENTO DO RELE
    Serial.print("            ");

    calculoForca();
    
  //Serial.print("            ");
    Serial.print(forca,4);//FORCA POSTERIOR
    
    Serial.print("            ");
    Serial.print(tensaoReal,4);
    
    Serial.print("            ");
    Serial.println(tempo-tempoAnt);

    tempoAnt = tempo;
    
    cont++;
    
  }else{
    digitalWrite(porta_rele, HIGH);
  }
}

/*
 * A função receber_parada() retorna 1 quando o usuário, por meio da interface,
 * indica que o programa deve parar.
 */
int receber_parada()
{
  char parada = '1';
  
  if(Serial.available()>0)
  {
    parada = Serial.read();  
  }

  if(parada == '0') //O recebimento do char '0' significa que o programa deve parar
    return 1;
  
  else
    return 0;
}

/*
 * A função map_f() é uma adapatação da função map(). Sua modificação visa permitir
 * resultados mais precisos no trabalho com números flutuantes, pois a função map() 
 * arredondava valores fracionários para inteiros.
 * Mais informações sobre a função map() no link:
 * https://www.arduino.cc/reference/pt/language/functions/math/map/
 */
float map_f(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
void loop(){}
