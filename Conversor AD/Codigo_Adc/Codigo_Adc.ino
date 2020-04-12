/*Novo código para a leitura da tensão utilizando o ADS1115
 *Bibliotecas necessárias:
 **i2cdevlib e ADS1115 disponíveis em "https://github.com/jrowberg/i2cdevlib/tree/master/Arduino"
 *Pinagem 
  ADS1115 -->  NANO
    VDD        5V
    GND        GND
    SCL        A5 (or SCL)
    SDA        A4 (or SDA)
    ALRT       2
 

*/
#include "ADS1115.h"

float tensao_millivolts;

ADS1115 adc(ADS1115_DEFAULT_ADDRESS);

//Pino do arduino que será responsavel pela alerta de leitura
const int pinoAlertReady = 2;

//Pino ligado ao relay
const int pinoRelay = 10;
int acionado;

void iniciar_ADC(){

  //inicializa o ADC
  adc.initialize();

  //seta a leitura na porta A1 com o GND como referência
  adc.setMultiplexer(ADS1115_MUX_P1_NG);

  //seta o modo single shot (um medicao por vez)
  adc.setMode(ADS1115_MODE_SINGLESHOT);

  //seta uma frequência de aquisição de 8HZ -> 125 ms
  adc.setRate(ADS1115_RATE_8);

  //Seta o ganho (PGA) +/- 6.144v (Fundo de escala)
  adc.setGain(ADS1115_PGA_6P144);

  //Habilita o pino ALERT/RDY 
  pinMode(pinoAlertReady, INPUT_PULLUP);
  adc.setConversionReadyPinMode();
  
  }

void setup() {
  //Permite a comunicação com o protocolo I2C
  Wire.begin();
  //Inicia a comunicação serial
  Serial.begin(9600);
  //Seta as configurações do ADS1115
  iniciar_ADC();
  //inicia o valor da tensão
  tensao_millivolts = 0;

  pinMode(pinoRelay,OUTPUT);
  digitalWrite(pinoRelay,LOW);
  acionado = 0;
}

void ler_ADC(){
  
  //Trigger para uma nova conversão
  adc.triggerConversion();
  
  //Espera a conversão estar feita -> pinoAlertRead = 0
  while(digitalRead(pinoAlertReady)){
    //Serial.println("=======================");
    }

  tensao_millivolts = adc.getMilliVolts(false);
 
  
  }

void loop() {
  ler_ADC();

  Serial.print("A1: "); Serial.print(tensao_millivolts,3); Serial.print("mV\n");

  if(tensao_millivolts >4000){
      if(!acionado){
        digitalWrite(pinoRelay, LOW); //aciona
        Serial.println("Acionado");
        acionado = 1;
        }
    }else{
      if(acionado){
        Serial.println("Desacionado");
        digitalWrite(pinoRelay, HIGH);
        acionado = 0;
      }
      
      }

  delay(10);
}
