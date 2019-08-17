from pyfirmata import ArduinoMega, util
from time import sleep as delay
import cv2
import numpy as np

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

        
def main():
    CriaPinos()


    while True:
        ViraEsquerda(3)
        ViraDireita(3)
        SegueReto(3)
    
    
if __name__ == "__main__":
    main()


