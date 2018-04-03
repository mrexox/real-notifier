/*
  SerialCommunicator.h - Library for communicating
  through the serial port using its own protocol.
*/
#ifndef SerialCommunicator_h
#define SerialCommunicator_h


#include <Arduino.h>
 
class SerialCommunicator
{
  public:
    SerialCommunicator();
    bool available();
    int get_sender();
    int get_type();
    int get_value();
    void next();
  private:
    bool _available;
    byte _message[4];
    void serialEvent();
    bool check_sum();
};


#endif