from pyfirmata import ArduinoMega, util
from time import sleep as delay
import cv2
import numpy as np
import threading


AP = {}
AS = {}
centrox = 0
centroy = 0
velocidade = 1.3
    
def ViraEsquerda(tempo = 3):                            #FUNÇÃO DE CONTROLE DO MOTOR. PINOS:      4,7|VELOCIDADE      2,3|MOTORD    5,6|MOTORE
    AP['pino4'].write(velocidade)
    AP['pino7'].write(velocidade)
    AP['pino2'].write(0)
    AP['pino3'].write(1)
    AP['pino5'].write(1)
    AP['pino6'].write(0)
    delay(tempo)
    
def ViraDireita(tempo = 3):                             #FUNÇÃO DE CONTROLE DO MOTOR. PINOS:      4,7|VELOCIDADE      2,3|MOTORD    5,6|MOTORE
    AP['pino4'].write(velocidade)
    AP['pino7'].write(velocidade)
    AP['pino2'].write(1)
    AP['pino3'].write(0)
    AP['pino5'].write(0)
    AP['pino6'].write(1)
    delay(tempo)

def SegueReto(tempo):
    AP['pino4'].write(velocidade)
    AP['pino7'].write(velocidade)
    AP['pino2'].write(0)
    AP['pino3'].write(1)
    AP['pino5'].write(0)
    AP['pino6'].write(1)
    delay(tempo)

def SegueTras(tempo):
    AP['pino4'].write(velocidade)
    AP['pino7'].write(velocidade)
    AP['pino2'].write(1)
    AP['pino3'].write(0)
    AP['pino5'].write(1)
    AP['pino6'].write(0)
    delay(tempo)

def Para(tempo):
    AP['pino4'].write(0)
    AP['pino7'].write(0)
    AP['pino2'].write(0)
    AP['pino3'].write(0)
    AP['pino5'].write(0)
    AP['pino6'].write(0)
    delay(tempo)

def PegaBola():
    AS['pino10'].write(170)
    delay(1)
    AS['pino11'].write(170)
    delay(2)
    AS['pino11'].write(0)
    delay(1)

def SoltaBola():
    AS['pino10'].write(180)
    AS['pino11'].write(70)
    delay(2)
    AS['pino10'].write(30)
    delay(3)
    AS['pino10'].write(180)
    delay(1)
    AS['pino11'].write(0)

def CriaPinos(mini = 2, maxi = 9,tipo = 'p', minis = 10, maxis = 12, tipos = 's'):      #TIPO: O:OUTPUT | I:INPUT | P:PWM
    
    arduino = ArduinoMega('COM13')
    
    for p in range(mini,maxi):
        AP["pino" + str(p)] = arduino.get_pin('d:{}:{}'.format(p,tipo))
    for s in range(minis,maxis):
        AS["pino" + str(s)] = arduino.get_pin('d:{}:{}'.format(s,tipos))

def AchaBola():
    inicial = cv2.VideoCapture(0)

    while True:
        i,img = inicial.read()
        median = cv2.medianBlur(img,21)
        cimg = cv2.cvtColor(median,cv2.COLOR_BGR2GRAY)
        cir = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,0.000000001,2000,
                           param1=25,param2=25,minRadius=5,maxRadius=0)
        
        if cir is not None:
            circles = np.uint16(np.around(cir))
            
            for i in circles[0,:]:
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
                global centrox
                global centroy
                centroy = i[1]
                centrox = i[0]
                
        cv2.imshow("img",img)
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break
        
    inicial.release()
    cv2.destroyAllWindows


def main():
    opencv = threading.Thread(target = AchaBola)
    opencv.start()
    CriaPinos()
    print("debug")
    while True:                                               ##ISSO VAI FIRAR FUNÇÃO. UMA PRA CADA EIXO
        errox = centrox - 330
        kpx =0.0001
        controlex = (kpx * errox)
        print(controlex)
        if controlex < 0:
            ViraEsquerda(abs(controlex))
        if controlex > 0:
            ViraDireita(abs(controlex))
        if controlex  == 0:
            Para(0.1)
            break
        
    while True:
        erroy = centroy - 350
        kpy =0.0001
        controley = (kpy * erroy)
        print(controley)
        if controley < 0:
            SegueReto(abs(controley))
        if controley > 0:
            SegueTras(abs(controley))
        if controley  == 0:
            Para(0.1)
            break

    PegaBola() 

    
    
if __name__ == "__main__":
    main()
