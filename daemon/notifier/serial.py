import serial 

from notifier import Notifier

class SerialNotifier(Notifier):
    """Sends notification to serial port"""

    def __init__(self, port, baudrate=9600):
        """Establishing connection with arduino.
        should use for notifications
        
        FUTURE:
        Establishing connection between raspi and arduino?
        """
        
        ser = serial.Serial()
        ser.baudrate = baudrate
        ser.port = port
        ser.open()

    def notify(message):
        raise NotImplementedError()

    def message_to_bytes(message): # dictionary
        """Protocol realization"""
        
        bytes = bytearray(6)

        beg = int('10101010', 2)
        sender = message['sender']
        type = message['type']
        value = message['value']
        end = int('11111111', 2)
        checksum = (beg + sender + type + value + end) & 255
        
        bytes[0] = beg
        bytes[1] = sender
        bytes[2] = (type << 4) | (value >> 4)
        bytes[3] = (value << 4) & 255
        bytes[4] = checksum
        bytes[5] = end
        return bytes
