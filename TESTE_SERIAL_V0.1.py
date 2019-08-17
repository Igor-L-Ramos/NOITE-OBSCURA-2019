import serial
from time import sleep as delay


ser = serial.Serial('COM3', 9600)

while True:
    ser.write("0".encode())
    print("0")
    delay(2)
    ser.write("1".encode())
    print("1")
    delay(2)
