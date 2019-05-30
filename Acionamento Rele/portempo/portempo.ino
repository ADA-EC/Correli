unsigned long value = 1000;
unsigned long tempo;
unsigned long temp_ant = 0;
int porta = 11;

void setup() {
  pinMode(porta, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  tempo = millis();
  
  Serial.print(tempo);
  Serial.print("\t");
  Serial.println(tempo - temp_ant);
  
  if((tempo - temp_ant) >= value){
    digitalWrite(porta, HIGH);
    temp_ant = tempo;
  }else{
    digitalWrite(porta, LOW);
  }
}
