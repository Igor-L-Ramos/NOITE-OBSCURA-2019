from pyfirmata import ArduinoMega, util
from time import sleep as delay
import cv2
import numpy as np
import threading

AP = {}
    
def ViraEsquerda(tempo = 3):                            #FUNÇÃO DE CONTROLE DO MOTOR. PINOS:      4,7|VELOCIDADE      2,3|MOTORD    5,6|MOTORE
    AP['pino4'].write(0.4)
    AP['pino7'].write(0.4)
    AP['pino2'].write(0)
    AP['pino3'].write(1)
    AP['pino5'].write(1)
    AP['pino6'].write(0)
    delay(tempo)
    
    
def ViraDireita(tempo = 3):                             #FUNÇÃO DE CONTROLE DO MOTOR. PINOS:      4,7|VELOCIDADE      2,3|MOTORD    5,6|MOTORE
    AP['pino4'].write(0.4)
    AP['pino7'].write(0.4)
    AP['pino2'].write(1)
    AP['pino3'].write(0)
    AP['pino5'].write(0)
    AP['pino6'].write(1)
    delay(tempo)

def SegueReto(tempo):
    AP['pino4'].write(0.4)
    AP['pino7'].write(0.4)
    AP['pino2'].write(0)
    AP['pino3'].write(1)
    AP['pino5'].write(0)
    AP['pino6'].write(1)
    delay(tempo)
    
def CriaPinos(mini = 2, maxi = 13,tipo = 'p'):      #TIPO: O:OUTPUT | I:INPUT | P:PWM
    
    arduino = ArduinoMega('COM3')
    for i in range(mini,maxi):
        AP["pino" + str(i)] = arduino.get_pin('d:{}:{}'.format(i,tipo))
        
def AchaBola():
    inicial = cv2.VideoCapture(0)

    while True:
        i,img = inicial.read()
        cv2.imshow("img",img)

        k = cv2.waitKey(30) & 0xFF

        if k == 27:
            break
        
    inicial.release()
    cv2.destroyAllWindows

    
    
def main():
    opencv = threading.Thread(target = AchaBola)
    CriaPinos()
    ViraDireita(3)
    opencv.start()
    SegueReto(3)
    ViraEsquerda(3)

    
    
if __name__ == "__main__":
    main()


