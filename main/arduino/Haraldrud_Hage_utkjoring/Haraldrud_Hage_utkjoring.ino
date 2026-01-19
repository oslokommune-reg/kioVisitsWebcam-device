//Adjusted to be bore sensitive 22.05.24. 
// numReadings = 30 -> 20
// if (average < 135  -> 138
// if (average > 150)(nybil) -> 142


const int numReadings = 20;

// Define Trig and Echo pin:
#define trigPin 8
#define echoPin 9

// Define variables:
long duration;
int distance;

int readings[numReadings];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
int total = 0;                  // the running total
int average = 0;                // the average

int nybil = 1;
int teller = 0;


void setup() {

    // Define inputs and outputs
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  // initialize serial communication with computer:
  Serial.begin(9600);
  //Serial.println("Starting...");
  // initialize all the readings to 0:
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }
}

void loop() {
    unsigned long start = micros();

    // Clear the trigPin by setting it LOW:
    digitalWrite(trigPin, LOW);

    delayMicroseconds(20);

    // Trigger the sensor by setting the trigPin high for 10 microseconds:
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(50);
    digitalWrite(trigPin, LOW);

    // Read the echoPin. pulseIn() returns the duration (length of the pulse) in microseconds:
    duration = pulseIn(echoPin, HIGH);

    // Calculate the distance:
    distance = duration*0.034/2;

    // Print the distance on the Serial Monitor (Ctrl+Shift+M):
    // Serial.print("Distance = ");
    // Serial.println(distance);

    delay(50);

    // subtract the last reading:
    total = total - readings[readIndex];
    // read from the sensor:
    readings[readIndex] = distance;
    // add the reading to the total:
    total = total + readings[readIndex];
    // advance to the next position in the array:
    readIndex = readIndex + 1;

    // if we're at the end of the array...
    if (readIndex >= numReadings) {
    // ...wrap around to the beginning:
    readIndex = 0;
    }

    // calculate the average:
    average = total / numReadings;
    // send it to the computer as ASCII digits
    // Serial.print(" average ");
    // Serial.println(average);

    // Serial.print(" nybil ");
    // Serial.println(nybil * 50 );


    if (average < 138 && nybil == 0){
        teller = teller + 1;
        nybil = 1;
        Serial.print("***Teller***");
        // Serial.println (teller * 10);

    }
    if (average > 142){
        nybil = 0;
        // Serial.print(" nybil ");
        // Serial.println(nybil * 50 );
    }        

}