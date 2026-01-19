
#include "NewPing.h"

#define TRIGGER_PIN 9

#define ECHO_PIN 8

#define MAX_DISTANCE 900

const int numReadings = 7;

int readings[numReadings];      // the readings from the analog input

int readIndex = 0;              // the index of the current reading

int total = 0;                  // the running total

int average = 0;                // the average

int n = 0;

int nybil = 1;

int nuller = 0;

int teller = 0;

int valid_distance = 0;

const int chipSelect = 10; 

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); 



void setup() {

  Serial.begin(9600);
 

  for (int thisReading = 0; thisReading < numReadings; thisReading++) {

      readings[thisReading] = 0;

   }

}



  

void loop() {
    
     delay(300);
     //Serial.println ("----------------");

     n = n+1;

     unsigned int distance = sonar.ping_cm();
     //Serial.println(distance);
     
     if (distance > 130){
        valid_distance = distance;
        
     }
     if (distance < 130){
        distance = valid_distance;
     }       
     /*
     Serial.print ("dist = ");
     Serial.println(distance);
     Serial.print ("Valid_dist = ");
     Serial.println(valid_distance);
     */

         //****Telling - Snitt****

    // subtract the last reading:

    total = total - readings[readIndex];

    // read from the sensor:

    readings[readIndex] = valid_distance;

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

    //Serial.print ("Snitt = ");

    //Serial.println(average);

    delay(20);        // delay in between reads for stability
         
      //******Telling***********
    if (average < 180  && nybil == 0){

     teller = teller +1;

     nybil = 1;
     //Serial.print ("—");
     //Serial.print (average);
     //Serial.print ("—");
     //Serial.print("Teller***********************");
     Serial.println (teller);

    }

    
    if (average < 180){
      nuller = 0;
    }
    if (average > 250){
      nuller = nuller + 1;
      //Serial.println(nuller);
     if (nuller > 4){
        nybil = 0;
        
        //Serial.println("NYbil^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");         
     }
     //Serial.println ("Nybil = 0");

    }
    //Serial.print ("Totalt antall biler = ");

    //Serial.println (teller);
    if (teller > 10000){
      teller = 0;
    }
}
