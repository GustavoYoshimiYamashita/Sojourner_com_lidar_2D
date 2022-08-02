import math

def iniciando_compass(robot, TIME_STEP):
    # Iniciando o sensor Lidar
    compass = robot.getDevice("compass")
    compass.enable(TIME_STEP)

    return compass

def leitura_compass(compass):

    direction = 0
    initial_value = True

    # Recebendo os valores da bússola
    valuesCompass = compass.getValues()
    # Transformando os valores em ângulos
    rad = math.atan2(valuesCompass[0], valuesCompass[2])
    bearing = (rad - 1.5708) / math.pi * 180

    # Iniciando o valor inicial do ângulo como o primeiro ângulo calculado
    if initial_value:
        initial_angle = bearing
        initial_value = False
    # Caso o valor zere, retornar para 360
    if bearing < 0.0:
        bearing = bearing + 360

    rad = (bearing * math.pi) / 180

    return rad

