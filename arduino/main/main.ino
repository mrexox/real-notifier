#include <SerialCommunicator.h>

SerialCommunicator communicator;

void setup() {
  for (int i = 2; i <= 13; i++) {
    pinMode(i, OUTPUT);
  }
  Serial.begin(9600);
}

int const NEW_MESSAGE_BLINK_PIN = 13;
int const NEW_MESSAGE_BLINK_DELAY = 300;
unsigned long new_message_blink_start_time = 0;

int pre_value = 0;

void loop() {
  unsigned long cur_time = millis();

  // if available new message
  if (communicator.available()) {
    // make blink
    digitalWrite(NEW_MESSAGE_BLINK_PIN, HIGH);
    new_message_blink_start_time = cur_time;
    // read and display new value
    int cur_value = communicator.get_value();
    if (cur_value != pre_value) {
      display_value(cur_value);
      pre_value = cur_value;
    }
    // wait for next message
    communicator.next();
  }
  // finish blink after NEW_MESSAGE_BLINK_DELAY milliseconds
  if (new_message_blink_start_time && cur_time - new_message_blink_start_time > NEW_MESSAGE_BLINK_DELAY) {
    digitalWrite(NEW_MESSAGE_BLINK_PIN, LOW);
    new_message_blink_start_time = 0;
  }

  delay(50);
}

void serialEvent() {
  communicator.serialEvent();
}

void display_value(int val) {
  for (int i = 2; i <= 7; i++) {
    if (val > i -2) {
      digitalWrite(i, HIGH);
    }
    else { 
      digitalWrite(i, LOW);
    }
  }
}

