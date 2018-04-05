#include "SerialCommunicator.h"

SerialCommunicator::SerialCommunicator() {
    _available = false;
    Serial.begin(9600);
}

bool SerialCommunicator::available() {
    return _available;
}

void SerialCommunicator::next() {
    _available = false;
}

int SerialCommunicator::get_sender() {
    if (_available) return (int)_message[0];
    else return -1;
}

int SerialCommunicator::get_type() {
    if (_available) {
        int tmp = _message[1];
        return tmp >> 4;
    }
    else return -1;
}

int SerialCommunicator::get_value() {
    if (_available) {
        byte tmp = _message[1];
        bitClear(tmp, 0);
        bitClear(tmp, 1);
        bitClear(tmp, 2);
        bitClear(tmp, 3);
        return (int)_message[2] + (tmp << 4);
    }
    else return -1;
}

/*
    SerialEvent occurs whenever a new data comes in the hardware serial RX. This
    routine is run between each time loop() runs, so using delay inside loop can
    delay response. Multiple bytes of data may be available.
*/
void SerialCommunicator::serialEvent() {
    while (!_available && Serial.available()) {
        // get new byte
        byte tmp = Serial.read();
        // if first byte = 10101010 and available >= 5 bites
        while (tmp == 170 && Serial.available() >= 5) {
            // get all new message
            for (byte i = 0; i < 4; i++) {
                _message[i] = Serial.read();
            }
            // analize massage
            if (Serial.read() == 255 && check_sum()) {
                _available = true;
            }
        }
    }
}

/*
    Считает контрольную сумму сообщения и сравнивает ее с эталонной.
    Возвращает TRUE в случае успеха.
*/
bool SerialCommunicator::check_sum() {
    // TODO: реализовать подсчет контрольной суммы
    return true;
}