import serial 

from abstract_notifier import Notifier

class SerialNotifier(Notifier):
    """Sends notification to serial port"""

    def __init__(self, port, baudrate=9600):
        """
        Establishing connection with arduino.
        should use for notifications
        
        FUTURE:
        Establishing connection between raspi and arduino?
        """
        
        ser = serial.Serial()
        ser.baudrate = baudrate
        ser.port = port
        # try me
        ser.open()
        # except me

    def notify(self, message):
        bytes = self.message_to_bytes(message)
        # ... write them
        raise NotImplementedError()

    @staticmethod
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
        bytes[2] = (type << 4) | (value >> 8)
        bytes[3] = value & 255
        bytes[4] = checksum
        bytes[5] = end
        return bytes

if __name__ == '__main__':
    import binascii
    b = SerialNotifier.message_to_bytes({
        'sender': 14,
        'type': 1,
        'value': 144
        })
    print( 'beg(8)', 'sender=14(8)', 'type=1(4)', 'value=144(12)', 'checksum(8)', 'end(8)', sep=' ')
    lensize = 8
    binstr = bin(int(binascii.hexlify(b), 16)).__str__().split('b')[1]
    words = [binstr[x:x+lensize] for x in range(0, len(binstr), lensize)]
    print(' '.join(words))
