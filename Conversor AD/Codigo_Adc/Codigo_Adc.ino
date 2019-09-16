#include <Adafruit_ADS1015.h>

Adafruit_ADS1115 ads(0x48);//conectado no GND

void setup() {

  Serial.begin(9600);
  
  ads.begin();
 
}

void loop() {
  
  int sensorValue = ads.readADC_SingleEnded(0);
  
  float tensaoADS = sensorValue * (0.1875 /1000);//ler o que vem do ADS; 0<=tensaoADS<=5V

  float tensaoReal = 2 * tensaoADS;

  float pressao = 25 * tensaoReal; //em toneladas

  Serial.print(tensaoReal ,4);
  Serial.print(" V");
  Serial.print("\t\t"); 
  Serial.print("\t\t");
  Serial.println(pressao ,4);
  Serial.print(" toneladas");
  
  delay(1000);
}
