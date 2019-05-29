#include <Adafruit_ADS1015.h>
#define value 1

float aux = value;
int sensorValue;
float tensaoADS;
float tensaoReal;
float forca;
int porta = 11;

Adafruit_ADS1115 ads(0x48);//conectado no GND

void setup() {

  Serial.begin(9600);
  pinMode(porta, OUTPUT);
  ads.begin();
 
}

void loop() {
  calculoForca();
  acionamentoRele();
  printSerial();
  
}

void calculoForca(){
  
  sensorValue = ads.readADC_SingleEnded(0);
  tensaoADS = sensorValue * (0.1875 /1000);//ler o que vem do ADS; 0<=tensaoADS<=5V
  tensaoReal = 2 * tensaoADS;
  forca = tensaoReal*25; //em toneladas  
  }

void acionamentoRele(){
  if((aux-tensaoADS)<=0 ){
    digitalWrite(porta, HIGH);
    aux = tensaoADS+value;
    //delay(1000);
    Serial.println("LIGOU");
  }else{
    digitalWrite(porta, LOW);
  }
}

void printSerial(){

  Serial.print(tensaoReal ,4);
  Serial.print(" V");
  Serial.print("\t\t"); 
  Serial.print("\t\t");
  
  Serial.print(tensaoADS ,4);
  Serial.print(" V");
  Serial.print("\t\t"); 
  Serial.print("\t\t");
  
  Serial.print(forca ,4);
  Serial.print(" toneladas");
  Serial.print("\t\t");
  Serial.println(aux-tensaoADS, 4);
  delay(100);
  }
