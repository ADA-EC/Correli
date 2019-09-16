#include <Adafruit_ADS1015.h>
#define valueModoTensao 1
#define OK 1
#define ERRO 0

float intervalo_tempo; 
float intervalo_tensao;

int sensorValue;
float tensaoADS;
float tensaoReal;
float tensaoAnt = 0.0;
float forca;

int porta_rele = 10;

unsigned long tempo;
unsigned long temp_ant = 0;
float fundo_escala; 

//Variaveis para receber as configuracoes
String texto = "";
char modo = '0';
String intervaloS = "";
String fundoS = "";
float intervalo;

Adafruit_ADS1115 ads(0x48);//conectado no GND

void setup() {

  Serial.begin(9600);
  pinMode(porta_rele, OUTPUT);
  digitalWrite(porta_rele, LOW);
  ads.begin();

  if(1)
  {   
    recebe_dados();
    converte_dados();
    //Serial.println("Entrou");
    if(modo == 'f')
    {
      //Serial.println("Forçaa !!");
      intervalo_tensao = intervalo;
      modo_forca();
    }
    else if(modo == 't')
    {
      Serial.println("\t        FORÇA(KT)\t\t\t\t\t      TEMPO(mS)");
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
    if(Serial.available())
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
  char parada = '0';
  
  while(parada == '0')
  {
    calculoForca();
    AcionamentoPorTempo();
    //Precisa implementar receber parada
  }
}

void modo_forca()
{
  char parada = '0';
  
  while(parada == '0')
  {
    calculoForca();
    acionamentoRele();
    printSerialForca();
    //Precisa implementar receber parada
  }
}

void calculoForca(){
  
  sensorValue = ads.readADC_SingleEnded(0);
  tensaoADS = sensorValue * (0.1875 /1000);//ler o que vem do ADS; 0<=tensaoADS<=5V
  tensaoReal = 2 * tensaoADS;
  forca = tensaoReal*(fundo_escala); //em toneladas
}

void acionamentoRele(){
  if((tensaoReal- tensaoAnt)>= intervalo_tensao){
    digitalWrite(porta_rele, HIGH);
    tensaoAnt = tensaoReal;
  }else{
    digitalWrite(porta_rele, LOW);
  }
}

void printSerialForca(){

  delay(100); 
  
  Serial.println(tensaoReal ,4); //Manda informacoes para a interface
  
  Serial.println(tensaoADS ,4);
  
  Serial.println(forca ,4);
 
//  Serial.println(aux-tensaoADS, 4);
}

void AcionamentoPorTempo(){
  
  tempo = millis();
    
  //Serial.println(tempo);
  //Serial.println(tempo - temp_ant);
  
  if((tempo - temp_ant) >= intervalo_tempo){
    
    Serial.print("\t\t");//Manda informacoes para a interface
    Serial.print(forca);
    Serial.print("\t\t\t\t\t\t\t");
    Serial.println(tempo);
    
    digitalWrite(porta_rele, HIGH);
    delay(10);
    temp_ant = tempo;
  }else{
    digitalWrite(porta_rele, LOW);
  }
}

void loop(){}
