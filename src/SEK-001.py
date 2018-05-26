#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

# definicao de motores
motorDireita = LargeMotor('outB')
motorEsquerda = LargeMotor('outC')
motorGarra = MediumMotor('outA')

# definicao de sensores
ultrassonico = UltrasonicSensor() 
assert ultrassonico.connected, "Sensor ultrassonico nao conectado"
ultrassonico.mode = 'US-DIST-CM'

gyro = GyroSensor()
assert gyro.connected, "Giroscopio nao conectado"

sensorCor = ColorSensor()
assert sensorCor.connected, "Sensor de cor nao conectado"
sensorCor.mode='COL-COLOR'
colors=('unknown','black','blue','green','yellow','red','white','brown')

def calibraGyro():
    gyro.mode = 'GYRO-RATE'
    sleep(1)
    gyro.mode = 'GYRO-ANG'
    sleep(1)

def girarRobo(anguloDesejado):
    calibraGyro()
    anguloSensor = gyro.value()

    if(anguloDesejado > 0):
        while(anguloSensor < anguloDesejado - 4): # 4 eh para compensar o lag de leitura do gyro
            motorDireita.run_forever(speed_sp=-50)
            motorEsquerda.run_forever(speed_sp=50)
            anguloSensor = gyro.value()
    else:
        while(anguloSensor > anguloDesejado + 4): # 4 eh para compensar o lag de leitura do gyro
            motorDireita.run_forever(speed_sp=50)
            motorEsquerda.run_forever(speed_sp=-50)
            anguloSensor = gyro.value()

    motorDireita.stop(stop_action="hold")
    motorEsquerda.stop(stop_action="hold")
    calibraGyro()
    
def agarrarBoneco():
    motorDireita.run_timed(time_sp=600, speed_sp=200)
    motorEsquerda.run_timed(time_sp=600, speed_sp=200)
    sleep(2)
    girarRobo(90)
    sleep(2)
    motorGarra.run_to_rel_pos(position_sp=290, speed_sp=100, stop_action="hold")
    sleep(5)
    motorDireita.run_timed(time_sp=1400, speed_sp=200)
    motorEsquerda.run_timed(time_sp=1400, speed_sp=200)
    sleep(3)
    motorGarra.run_to_rel_pos(position_sp=-300, speed_sp=100, stop_action="hold")
    sleep(5)
    motorDireita.run_timed(time_sp=1400, speed_sp=-200)
    motorEsquerda.run_timed(time_sp=1400, speed_sp=-200)
    sleep(3)
    girarRobo(-90)
    calibraGyro()

def main():	
    btn = Button()
    calibraGyro()	
    Sound.speak('Hello Humans!').wait()
    i = 100
    while i<200:
        motorDireita.run_forever(speed_sp=i)
        motorEsquerda.run_forever(speed_sp=i)
        i = i+25
        sleep(0.3)
    while btn.any()==False:
        distancia = ultrassonico.value()/10  # converte de mm para cm
        if(distancia > 20):
            motorDireita.run_forever(speed_sp=i)
            motorEsquerda.run_forever(speed_sp=i)
        else:
            motorDireita.stop(stop_action="hold")
            motorEsquerda.stop(stop_action="hold")
            agarrarBoneco()
    motorDireita.stop(stop_action="hold") #tentativa de parada
    motorEsquerda.stop(stop_action="hold")

if __name__ == "__main__":
    main()
