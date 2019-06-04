#include <Adafruit_ADS1015.h> //biblioteca utilizada por conta do conversor AD
#define valueModoTensao 1

unsigned long valueModoTempo = 1000;
float aux = valueModoTensao;
int sensorValue;
float tensaoADS;
float tensaoReal;
float forca;
int porta = 11;
unsigned long tempo;
unsigned long temp_ant = 0;
int modo=0;
int entrou=0;

Adafruit_ADS1115 ads(0x48);//conectado no GND

void setup() {

  Serial.begin(9600);
  pinMode(porta, OUTPUT);
  ads.begin();
  menu();
  while(Serial.available()==0);
  modo = Serial.read(); //Verifica modo de operacao da camera.
  
}

void loop() {  
  if(modo == 49){ //Valores da tabela ASCII: "49" equivale ao numero "1"  
    calculoForca();
    acionamentoRele();
    printSerial();
  }

  if(modo == 50){//Valores da tabela ASCII: "50" equivale ao numero "2"
    AcionamentoPorTempo();
  }
}

void calculoForca(){  //Função utilizada caso  usuário escolha o acionamento da câmera por intervalo de tensão
  sensorValue = ads.readADC_SingleEnded(0);
  tensaoADS = sensorValue * (0.1875 /1000);//ler o que vem do ADS; 0<=tensaoADS<=5V
  tensaoReal = 2 * tensaoADS;
  forca = tensaoReal*25; //em toneladas  
  }

void acionamentoRele(){
  if((aux-tensaoADS)<=0 ){
    digitalWrite(porta, HIGH);
    aux = tensaoADS+valueModoTensao;
    //delay(1000);
    Serial.println("LIGOU");
  }else{
    digitalWrite(porta, LOW);
  }
}

void printSerial(){ //Função que mostra na serial os valores da tensão real, da tensão sobre o ADS e da força

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

void AcionamentoPorTempo(){ //Função utilizada caso o usuário escolha o acionamento da câmera por intervalo de tempo
  tempo = millis();
  
  Serial.print(tempo);
  Serial.print("\t");
  Serial.println(tempo - temp_ant);
  
  if((tempo - temp_ant) >= valueModoTempo){
    digitalWrite(porta, HIGH);
    temp_ant = tempo;
  }else{
    digitalWrite(porta, LOW);
  }
}

void menu(){
  Serial.print("Escolha o modo de operacao:\n\n");
  Serial.print("1-Tirar fotos com base na forca aplicada\n");
  Serial.print("2-Tirar fotos ao longo de intervalos de tempo\n"); 
}
