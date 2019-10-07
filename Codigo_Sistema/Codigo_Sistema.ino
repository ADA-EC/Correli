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

//Variaveis para receber as configuracoes
char modo = '0';
String intervaloS = "";
String fundoS = "";
float intervalo;

Adafruit_ADS1115 ads(0x48);//conectado no GND

void setup() {

  Serial.begin(9600);
  
  pinMode(porta_rele, OUTPUT);
  digitalWrite(porta_rele, HIGH);
  
  //ads.setGain(GAIN_ONE);
  ads.begin();

  if(1)
  {   
    recebe_dados();
    converte_dados();
    //Serial.println("Entrou");
    if(modo == 'f')
    {
      Serial.println("IMAGEM         TENSAO         FORCA         FORCA_P            TENSAO_D            TEMPO");

      intervalo_forca = intervalo;
      modo_forca();
    }
    else if(modo == 't')
    {
      Serial.println("IMAGEM         TENSAO         FORCA         FORCA_P            TENSAO_D            TEMPO");
      intervalo_tempo = intervalo;
      modo_tempo();      
    }
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
  //Serial.println(fundoS);
  //Serial.println(intervaloS);
}

void converte_dados()
{
  intervalo = intervaloS.toFloat();
  fundo_escala = fundoS.toFloat();
}

void modo_tempo()
{
  int parada = 0;
  
  while(!parada)
  {
    calculoForca();
    verificarTempo();
    parada = receber_parada();//Precisa implementar receber parada
  }
}

void modo_forca()
{
  char parada = '0';
  
  while(parada == '0')
  {
    calculoForca();
    verificarForca();

    //printSerialForca();
    //Precisa implementar receber parada
  }
}

void calculoForca(){
  
  sensorValue = ads.readADC_SingleEnded(1);
  //sensorValue = analogRead(0);
  //tensaoReal = map_f(sensorValue,0,65535,0,10);
  tensaoADS = sensorValue * (0.1875 /1000);//ler o que vem do ADS; 0<=tensaoADS<=5V
  //tensaoReal = 2 * tensaoADS;
  //forca = tensaoReal*(fundo_escala); //em toneladas
  forca = map_f(sensorValue,0,65536,0,fundo_escala);

  if(forca >= fundo_escala)
      Serial.print("0");
}

void verificarForca(){
  if((forca - forcaAnt)>= intervalo_forca){

    Serial.print(cont);
    
    calculoForca();
    Serial.print("            ");
    Serial.print(tensaoReal,4);
    Serial.print("            ");
    Serial.print(forca); //FORCA ANTERIOR
  
    digitalWrite(porta_rele, LOW);//ACIONAMENTO DO RELE

    calculoForca();
    
    Serial.print("            ");
    Serial.print(forca);//FORCA POSTERIOR
    
    Serial.print("            ");
    Serial.print(tensaoReal,4); //Tensão Real
    
    Serial.print("            ");
    Serial.println(forca-forcaAnt); //Invervalo
    
    forcaAnt = forca;

    cont++;
  }else{
    digitalWrite(porta_rele, HIGH); //desliga o rele
  }
}

void printSerialForca(){

  delay(100); 
  
  Serial.println(tensaoReal ,4); //Manda informacoes para a interface
  
  Serial.println(tensaoADS ,4);
   
//  Serial.println(aux-tensaoADS, 4);
}

void verificarTempo(){
  
  tempo = millis();
    
  //Serial.println(tempo);
  //Serial.println(tempo - temp_ant);
  
  if((tempo - tempoAnt) >= intervalo_tempo){

    Serial.print(cont);

    calculoForca();
    Serial.print("            ");
    Serial.print(tensaoADS,4);
    Serial.print("            ");
    Serial.print(forca,4); //FORCA ANTERIOR
  
    digitalWrite(porta_rele, LOW);//ACIONAMENTO DO RELE
    Serial.print("            ");

    calculoForca();
    
//    Serial.print("            ");
    Serial.print(forca,4);//FORCA POSTERIOR
    
    Serial.print("            ");
    Serial.print(tensaoADS,4);
    
    Serial.print("            ");
    Serial.println(tempo-tempoAnt);

    tempoAnt = tempo;
    
    cont++;
    
  }else{
    digitalWrite(porta_rele, HIGH);
  }
}

int receber_parada()
{
  char parada = '1';
  
  if(Serial.available()>0)
  {
    parada = Serial.read();  
  }

  if(parada == '0') //'0' significa parar o programa
    return 1;
  
  else
    return 0;
}

float map_f(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
void loop(){}
