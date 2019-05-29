unsigned long tempo;
int temp_ant=1000;


void setup() {
  pinMode(7, OUTPUT);
}

void loop() {
  tempo=millis();
  temp_ant=tempo-temp_ant;
  if(temp_ant>=0 && temp_ant<1000){
    digitalWrite(7, HIGH);
  }else{
    digitalWrite(7, LOW);
  }
  if(tempo%3000==0){
    temp_ant=tempo;
  }
}
