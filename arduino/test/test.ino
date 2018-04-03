#include <SerialCommunicator.h>

SerialCommunicator communicator;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}
 
void loop() {
  if (communicator.available()) {
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    
    communicator.next();
  }
  delay(1000);
  
  
}
