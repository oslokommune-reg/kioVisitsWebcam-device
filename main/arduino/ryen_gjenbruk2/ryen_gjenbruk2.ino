//Ryen hage

#include "NewPing.h"

#define TRIGGER_PIN 9

#define ECHO_PIN 8

#define MAX_DISTANCE 500

const int numReadings = 14;
int nuller = 0;

int readings[numReadings];      // the readings from the analog input

int readIndex = 0;              // the index of the current reading

int total = 0;                  // the running total

int average = 0;                // the average

int n = 0;

int nybil = 1;

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
    
     delay(200);
     //Serial.println ("----------------");

     n = n+1;

     unsigned int distance = sonar.ping_cm();
     //Serial.println(distance);
     
     if (distance > 40){
        valid_distance = distance;
        
     }
     if (distance < 40){
        distance = valid_distance;
     }       
     /*
     Serial.print ("dist = ");
     Serial.println(distance);
     Serial.print ("Valid_dist = ");*/
    // Serial.println(valid_distance);
     

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

           // delay in between reads for stability
         
      //******Telling***********
    if (average < 185  && nybil == 0){

     teller = teller +1;

     nybil = 1;
     //Serial.print ("—");
     //Serial.print (average);
     //Serial.print ("—");
     //Serial.print ("Teller******************************: ");
     Serial.println (teller);

    }
    if (average < 185){
      nuller = 0;
    }
    if (average > 300){
      nuller = nuller + 1;
      //Serial.println(nuller);
     if (nuller > 3){
        nybil = 0;
        //Serial.println("Nybil^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
     }
     //Serial.println ("Nybil = 0");

    }

    //Serial.print ("Totalt antall biler = ");
    if (nuller > 10000){
      nuller = 0;
    }
    //Serial.println (teller);
    if (teller > 10000){
      teller = 0;
    }
}
