#include <Adafruit_ADS1015.h>
#define valueModoTensao 1
unsigned long valueModoTempo = 1000;

float aux = valueModoTensao;
int sensorValue;
float tensaoADS;
float tensaoReal;
float tensaoAnt = 0.0;
float forca;
int porta = 11;
unsigned long tempo;
unsigned long temp_ant = 0;
char modo = 'x'; //Para nao iniciar com lixo de memoria
int entrou=0;

Adafruit_ADS1115 ads(0x48);//conectado no GND

void setup() {

  Serial.begin(9600);
  pinMode(porta, OUTPUT);
  ads.begin();

  Serial.print("comecou"); //Indica para o programa em Python que o arduino comecou a funcionar e que o codigo pode comecar a rodar
  delay(1000); 
  
}

void loop() {
  
  while(Serial.available()){
    delay(10);
    modo = Serial.read();
  }
  
  if(modo == '1') //Codigo 1 significa "modo por forca"
  { 
    calculoForca();
    acionamentoRele();
    printSerialForca();
  }

  if(modo == '2') //Codigo 2 significa "modo por tempo"
  {
    AcionamentoPorTempo();
  }
}

void calculoForca(){
  
  sensorValue = ads.readADC_SingleEnded(1);
  tensaoADS = sensorValue * (0.1875 /1000);//ler o que vem do ADS; 0<=tensaoADS<=5V
  tensaoReal = 2 * tensaoADS;
  forca = tensaoReal*25; //em toneladas  
}

void acionamentoRele(){
  if((tensaoReal- tensaoAnt)>= aux){
    digitalWrite(porta, HIGH);
    tensaoAnt = tensaoReal;
  }else{
    digitalWrite(porta, LOW);
  }
}

void printSerialForca(){

  delay(100); //Importante para a comunicacao com Python
  
  Serial.println(tensaoReal ,4);
  
  Serial.println(tensaoADS ,4);
  
  Serial.println(forca ,4);
  
  Serial.println(aux-tensaoADS, 4);
}

void AcionamentoPorTempo(){
  tempo = millis();

  delay(100); //Importante para a comunicacao com Python
  
  Serial.println(tempo);
  Serial.println(tempo - temp_ant);
  
  if((tempo - temp_ant) >= valueModoTempo){
    digitalWrite(porta, HIGH);
    temp_ant = tempo;
  }else{
    digitalWrite(porta, LOW);
  }
}
