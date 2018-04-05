#include <SerialCommunicator.h>

SerialCommunicator communicator;

void setup() {
  pinMode(2, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (communicator.available()) {
    print_communicator_args();
    
    digitalWrite(2, HIGH);
    delay(500);
    digitalWrite(2, LOW);
    
    communicator.next();
  }  
  delay(1000);
}

void serialEvent() {
  communicator.serialEvent();
}

void print_communicator_args() {
  Serial.println("NEW MESSAGE");
  String str = String("sender = ");
  Serial.println(str + communicator.get_sender());
  str = String("type = ");
  Serial.println(str + communicator.get_type());
  str = String("sender = ");
  Serial.println(str + communicator.get_value());
  Serial.println("-------------");
}
