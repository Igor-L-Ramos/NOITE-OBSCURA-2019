import cv2
import numpy as np
import time
import math
import serial

a = 0
ser = serial.Serial('COM3', 9600)
inicial = cv2.VideoCapture(0)

while a < 2:
    ser.write("1".encode())
    print("1")
    time.sleep(2)
    ser.write("0".encode())
    a += 1

while True:
    i,img = inicial.read()
    if i:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        baixo = np.array([0,0,90]) 
        superior = np.array([50,255,255])

        mascara = cv2.inRange(hsv, baixo, superior)
        mas = cv2.medianBlur(mascara,35)
        res = cv2.bitwise_and(img,img, mask= mas)
        
        contours, hierarchy = cv2.findContours(mas, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cv2.drawContours(img, contours,0, (0,255,0), 3)
            
            cimg = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
            cir = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,0.000000001,2000,
                           param1=28,param2=75,minRadius=20,maxRadius=0)

            if cir is not None:
                circles = np.uint16(np.around(cir))
                
                for i in circles[0,:]:
                    cv2.circle(img,(i[0],i[1]),i[2],(255,0,255),2)
                    area = (i[2] ** 2) * 3.14
                    if i[0] < 250:
                        ser.write("1".encode())
                        print(1)
                        time.sleep(2)
                    if i[0] > 250:
                        ser.write("0".encode())
                        time.sleep(2)
    
            
    cv2.imshow("img",img)
    cv2.imshow("img3",res)

    k = cv2.waitKey(30) & 0xFF

    if k == 27:
        break
        
    
inicial.release()
cv2.destroyAllWindows
    


