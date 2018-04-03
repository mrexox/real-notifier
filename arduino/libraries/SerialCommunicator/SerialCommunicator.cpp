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
        byte tmp =_message[1];
        bitClear(tmp, 4);
        bitClear(tmp, 5);
        bitClear(tmp, 6);
        bitClear(tmp, 7);
        return (int)tmp;
    }
    else return -1;
}

int SerialCommunicator::get_value() {
    if (_available) {
        int tmp = (int)_message[2];
        if (bitRead(_message[1], 4)) tmp += 256;
        if (bitRead(_message[1], 5)) tmp += 512;
        if (bitRead(_message[1], 6)) tmp += 1024;
        if (bitRead(_message[1], 7)) tmp += 2048;
        return tmp;
    }
    else return -1;
}

/*
    SerialEvent occurs whenever a new data comes in the hardware serial RX. This
    routine is run between each time loop() runs, so using delay inside loop can
    delay response. Multiple bytes of data may be available.
*/
void SerialCommunicator::serialEvent() {
    while (Serial.available() >= 5 && !_available) {
        // get all new bytes
        for (byte i = 0; i < 4; i++) {
            _message[i] = Serial.read();
        }
        // analize massage
        if (Serial.read() == 255 && check_sum()) {
            _available = true;
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