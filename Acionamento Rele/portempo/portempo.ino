unsigned long value = 1020;
unsigned long tempo;
unsigned long temp_ant = value;
int porta = 11;

void setup() {
  pinMode(porta, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  tempo = millis();
  
  Serial.print(tempo);
  Serial.print("\t");
  Serial.println(temp_ant - tempo);
  
  if((temp_ant - tempo) <= 20){
    digitalWrite(porta, HIGH);
    temp_ant += value;
  }else{
    digitalWrite(porta, LOW);
  }
}
