
#include "NewPing.h"

#define TRIGGER_PIN 9

#define ECHO_PIN 8

#define MAX_DISTANCE 800

const int numReadings = 5;

int readings[numReadings];      // the readings from the analog input

int readIndex = 0;              // the index of the current reading

int nuller = 0;

int total = 0;                  // the running total

int average = 0;                // the average

int n = 0;

int nybil = 1;

int timeout = 0;

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
    
     delay(250);
     //Serial.println ("----------------");
     timeout = timeout + 1; 
     n = n+1;
     //Serial.println(timeout);
     
     unsigned int distance = sonar.ping_cm();
     //Serial.println(distance);
     
     if (distance > 180){
        valid_distance = 0;
       //Serial.println(distance);  
     }
     if (distance < 180){
        valid_distance = distance;
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

    //delay(20);        // delay in between reads for stability
         
      //******Telling***********
    if (average > 27  && nybil == 0){

     teller = teller +1;

     nybil = 1;
     //Serial.print ("—");
     //Serial.print (average);
     //Serial.print ("—");
     timeout = 0;
     //Serial.print ("Teller****************");
     Serial.println (teller);

    }
    if (average != 0){
      nuller = 0;
    }
    if (average == 0){
      nuller = nuller + 1;
      //Serial.println(nuller);
     if (nuller > 2){
        nybil = 0;
        //Serial.println ("Nybil^^^^^^^^^^^^^^^^^^^^^^^^^^^");
         
     }
     //Serial.println ("Nybil = 0");

    }
    
  
    //Serial.print ("Totalt antall biler = ");

    //Serial.println (teller);
    if (timeout > 30600){
      teller = 0;
    }  
    if (teller > 10000){
      teller = 0;
    }
}
