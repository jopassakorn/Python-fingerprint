import serial                                                              #Serial imported for Serial communication
import time                                                                #Required to use delay functions
import array

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=.1)       #Create Serial port object called ArduinoUnoSerialData time.sleep(2)                                                             #wait for 2 secounds for the communication to get established
time.sleep(2) #give the connection a second to settle
loop = True
finger = array.array('i', (0 for i in range(0, 512)))
while(loop):
    arduino.write("1")
    data = arduino.readline()
    data = str(data)
    if (data != 'f'):
        input = arduino.readline()
        while (len(str(input)) < 3):
            input = arduino.readline()
        print(input)
    if (data == 'f'):
        print("Failed")