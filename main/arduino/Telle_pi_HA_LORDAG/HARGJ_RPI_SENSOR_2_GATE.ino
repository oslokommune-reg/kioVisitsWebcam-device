//Sensor 2 pointing west, USB0
//NOT IN USE
#include "NewPing.h"

#define TRIGGER_PIN 9
#define ECHO_PIN 8
#define MAX_DISTANCE 900

const int numReadings = 7;
int nuller = 0;
int readings[numReadings];
int readIndex = 0;
int total = 0;
int average = 0;
int nybil = 1;
int teller = 0;
int valid_distance = 0;

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

bool debugModeSerial = true;   // Sett til true for Serial Monitor (seriell) debugging
bool debugModePlotter = false; // Sett til true for Serial Plotter (plotter) debugging

void setup() {
  Serial.begin(9600);

  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }
}

void loop() {
    delay(320);

    unsigned int distance = sonar.ping_cm();
    // Filter out wrong readings
     if (distance > 130){
        valid_distance = distance;
     }

     if (distance < 130){
        distance = valid_distance;
     }       

    total -= readings[readIndex];
    readings[readIndex] = valid_distance;
    total += readings[readIndex];
    readIndex = (readIndex + 1) % numReadings;

    if (readIndex >= numReadings) {
        readIndex = 0;
    }

    average = total / numReadings;

    if (debugModeSerial) {
        Serial.print("Average: ");
        Serial.println(average);
        Serial.print("Distance: ");
        Serial.println(distance);
        Serial.print("Teller: ");
        Serial.println(teller);
        Serial.print("Nybil: ");
        Serial.println(nybil);
    }

    if (debugModePlotter) {
        Serial.print(average);
        Serial.print(",");
        Serial.print(distance);
        Serial.print(",");
        Serial.print(teller);
        Serial.print(",");
        Serial.println(nybil);
    }
    //******Telling***********
    if (average < 180 && nybil == 0) {
        teller++;
        nybil = 1;
        Serial.println(teller);
    }

    if (average < 180){
        nuller = 0;
    }
    //Bilen har passert ved tre målinger på null
    if (average > 250){
        nuller++;
        if (nuller > 4){
            nybil = 0;   
        }
    }
}
