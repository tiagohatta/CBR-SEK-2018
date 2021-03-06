#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

# definicao de motores
motorDireita = LargeMotor('outC')
motorEsquerda = LargeMotor('outB')
motorGarra = MediumMotor('outA')

# definicao de sensores
ultrassonico = UltrasonicSensor()
assert ultrassonico.connected, "Sensor ultrassonico nao conectado"
ultrassonico.mode = 'US-DIST-CM'

gyro = GyroSensor()
assert gyro.connected, "Giroscopio nao conectado"

SensorCorDir = ColorSensor('in1')
assert SensorCorDir.connected, "Sensor de cor nao conectado"
SensorCorDir.mode='COL-COLOR'
colors=('none','black','blue','green','yellow','red','white','brown')

SensorCorEsq = ColorSensor('in4')
assert SensorCorEsq.connected, "Sensor de cor nao conectado"
SensorCorEsq.mode='COL-COLOR'

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
			motorDireita.run_forever(speed_sp=-200)
			motorEsquerda.run_forever(speed_sp=200)
			anguloSensor = gyro.value()
	else:
		while(anguloSensor > anguloDesejado + 4): # 4 eh para compensar o lag de leitura do gyro
			motorDireita.run_forever(speed_sp=200)
			motorEsquerda.run_forever(speed_sp=-200)
			anguloSensor = gyro.value()

	motorDireita.stop(stop_action="hold")
	motorEsquerda.stop(stop_action="hold")
	calibraGyro()

def plaza_entrega_boneco ():
	#Entrega do boneco
	print("PLAZA AI VAMOS NOS")
	while(colors[SensorCorDir.value()] != "black") or (colors[SensorCorEsq.value()] != "black"):
		motorDireita.run_forever(speed_sp=200)
		motorEsquerda.run_forever(speed_sp=200)
	print("ACHEI PRETO, VOU IR PRO CENTRO DA BOLA")
	sleep(1) #Esse sleep serve para não ficar na borda do centro preto
	motorDireita.run_forever(speed_sp=0)
	motorEsquerda.run_forever(speed_sp=0)
	motorGarra.run_to_rel_pos(position_sp=290, speed_sp=100, stop_action="hold") #abre H ra
	print("AGORA VOU ANDAR PRA TRAS")
	sleep(2)
	motorDireita.run_timed(time_sp=1400, speed_sp=-200)
	motorEsquerda.run_timed(time_sp=1400, speed_sp=-200)
	sleep(3)
	motorGarra.run_to_rel_pos(position_sp=-300, speed_sp=100, stop_action="hold") #fecha H ra
	sleep(0.4)
	plaza_modo1()

def plaza_modo1():
	print("SAINDO DO PLAZA")
	motorDireita.run_forever(speed_sp=-200)
	motorEsquerda.run_forever(speed_sp=-200)
	sleep(3)
	motorDireita.run_forever(speed_sp=0)
	motorEsquerda.run_forever(speed_sp=0)
	#Verifica distancia das paredes:
	dist_dir = ultrassonico.value()/10
	print("Distancia da direita: ", dist_dir)
	sleep(0.4)
	girarRobo(90)
	girarRobo(90)
	dist_esq = ultrassonico.value()/10
	print("Distancia da esquerda: ", dist_esq)
	sleep(0.4)
	while(abs(dist_esq-dist_dir)>3):
		if(dist_esq > dist_dir):
			#Anda para a esquerda
			girarRobo(90)
			motorDireita.run_forever(speed_sp=200)
			motorEsquerda.run_forever(speed_sp=200)
			sleep(0.5)
			motorDireita.run_forever(speed_sp=0)
			motorEsquerda.run_forever(speed_sp=0)
			girarRobo(90)
		elif(dist_esq < dist_dir):
			#Anda para a direita
			girarRobo(-90)
			motorDireita.run_forever(speed_sp=200)
			motorEsquerda.run_forever(speed_sp=200)
			sleep(0.5)
			motorDireita.run_forever(speed_sp=0)
			motorEsquerda.run_forever(speed_sp=0)
			girarRobo(-90)
		dist_dir = ultrassonico.value()/10
		girarRobo(90)
		girarRobo(90)
		dist_esq = ultrassonico.value()/10
	motorDireita.run_timed(time_sp=2000, speed_sp=200)
	motorEsquerda.run_timed(time_sp=2000, speed_sp=200)



def main():
	motorDireita.run_forever(speed_sp=200)
	motorEsquerda.run_forever(speed_sp=200)
	if (colors[SensorCorDir.value()] == "red") or (colors[SensorCorEsq.value()] == "red"): #Condição para entrar no plaza (que pode ser outra condição. Coloquei essa por não saber exatamente qual seria)
		plaza_entrega_boneco()

while(True):
	main()
