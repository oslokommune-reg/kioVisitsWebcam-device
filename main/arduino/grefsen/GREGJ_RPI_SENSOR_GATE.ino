int sensorInput = 13;
int releOutput = 12;    
int sensorState = 0;

void setup() {
  pinMode(sensorInput, INPUT); //Read sensor
  pinMode(releOutput, OUTPUT); //Output to rele
  sensorState = digitalRead(sensorInput);
  Serial.begin(9600);

}

void loop() {
  
  digitalWrite(releOutput, LOW);
  sensorState = digitalRead(sensorInput);
//  Serial.println(sensorState);
  
  if  (sensorState == HIGH){
    while (sensorState == HIGH){
      sensorState = digitalRead(sensorInput); 
      delay(100);
    }
    Serial.println("Bil!");
    digitalWrite(releOutput, HIGH);
    sensorState = LOW;
    delay(100);
    digitalWrite(releOutput, LOW);  
  }
}
  
