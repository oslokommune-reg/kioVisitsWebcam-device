#define trigPin 8
#define echoPin 9

long duration;
int distance;

const int numReadings = 30;
int readings[numReadings];
int readIndex = 0;
int total = 0;
int average = 0;

int nybil = 1;
int teller = 0;

bool debugModeSerial = true;  // Sett til true for Serial Monitor (Tallverdier) debugging
bool debugModePlotter = false;  // Sett til true for Serial Plotter (Grafer) debugging

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  Serial.println("Starting...");
  
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }
}

void loop() {
  unsigned long start = micros();
 
  digitalWrite(trigPin, LOW);
  delayMicroseconds(20);
  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(50);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  delay(50);
  // Calculates a floating average to filter readings
  total = total - readings[readIndex];
  readings[readIndex] = distance;
  total = total + readings[readIndex];
  readIndex = readIndex + 1;

  if (readIndex >= numReadings) {
    readIndex = 0;
  }

  average = total / numReadings;

  if (debugModeSerial) {
    // Skriv ut verdier for debugging til Serial Monitor (Tallverdier)
    Serial.print("Average:");
    Serial.println(average);
    Serial.print("Distance:");
    Serial.println(distance);
    Serial.print("Teller:");
    Serial.println(teller);
    Serial.print("Nybil:");
    Serial.println(nybil);
  }

  if (debugModePlotter) {
    // Send dataene til Serial Plotter (Graf)
    Serial.print(average);
    Serial.print(",");
    Serial.print(distance);
    Serial.print(",");
    Serial.print(teller);
    Serial.print(",");
    Serial.println(nybil);
  }

  if (average < 135 && nybil == 0) {
    teller = teller + 1;
    nybil = 1;
    //Printer alltid for at python på pi skal lese signal om bil
    Serial.print (teller * 10);
  }

  if (average > 150) {
    nybil = 0;
  }
}
