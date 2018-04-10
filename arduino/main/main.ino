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
bool communication_enabled = false;

int pre_value = 0;

void loop() {
  if (communication_enabled || communicator.available()) {
    unsigned long cur_time = millis();
  
    // if available new message
    if (communicator.available()) {
      communication_enabled = true;
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
  }
  else wait();
  
  delay(10);
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


// WAITING FOR FIRST MESSAGE
int wait_pin = 2;
bool wait_pin_flag = true;
int wait_spd = 1000;
bool wait_spd_flag = false;
bool wait_spd_enable = false;

void wait() {
  digitalWrite(wait_pin, HIGH);
  delay(wait_spd);
  digitalWrite(wait_pin, LOW);

  // wait_pin
  if (wait_pin <= 2) {
    wait_pin = 3;
    wait_pin_flag = true;
  }
  else if (wait_pin >= 7) {
    wait_pin = 6;
    wait_pin_flag = false;
  }
  else if (wait_pin_flag) wait_pin += 1;
  else wait_pin -= 1;

  // wait_spd
  if (wait_spd_enable) {
    if (wait_spd <= 10) {
      wait_spd = 11;
      wait_spd_flag = true;
    }
    else if (wait_spd >= 200) {
      wait_spd = 199;
      wait_spd_flag = false;
    }
    else if (wait_spd_flag) wait_spd += 1;
    else wait_spd -= 1;
  }
}


