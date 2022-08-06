import math

import funcoes_lidar
from controller import *
import movimentacao
import pygame
import mapa
import funcoes_gps
import funcoes_bussola
import inteligencia

'''

    Inicializando variáveis e funções para a simulação
s
'''

# Definindo taxSa de atualização do simulador
TIME_STEP = 10

# Instanciando funções do robô
robot = Robot()

'''

    Iniciando componentes do robô

'''

# Iniciando os controles dos motores
motores_velocidade, motores_angulo= movimentacao.iniciando_motores(robot)
lidar = funcoes_lidar.iniciando_lidar(robot, TIME_STEP, Lidar)
GPS = funcoes_gps.iniciando_GPS(robot, TIME_STEP)
compass = funcoes_bussola.iniciando_compass(robot, TIME_STEP)

'''

    Funções

'''

def movimentar(speed):
    movimentacao.set_speed(speed, motores_velocidade)
    angulos = [0, 0, 0, 0]
    movimentacao.set_steering_angle(angulos, motores_angulo)

def girar_direita_proprio_eixo():
    velocidades = [-1, 1, -1, 1, -1, 1]
    movimentar(velocidades)
    angulos = [1, -1, -1, 1]
    movimentacao.set_steering_angle(angulos, motores_angulo)

def girar_esquerda_proprio_eixo():
    velocidades = [1, -1, 1, -1, 1, -1]
    movimentar(velocidades)
    angulos = [1, -1, -1, 1]
    movimentacao.set_steering_angle(angulos, motores_angulo)

# Prominent Arduino map function :)
def _map(x, in_min, in_max, out_min, out_max):
    return float((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

'''
    Iniciando Mapa

'''

surface = mapa.iniciando_mapa(pygame)

'''

    Lógica principal da simulação

'''

def desenhando_mapa_lidar(xGPS, yGPS, angulo_compass, loop_limpeza):
    if loop_limpeza:
        # Essa função atualiza o mapa
        mapa.atualiza_mapa_preto(surface)

    # Coletando os dados do Sensor Lidar no robô
    imagem = funcoes_lidar.coletando_dados_lidar(lidar)
    # Criando uma lista com o valor da distância e do grau
    imagem_radianos, imagem_graus = funcoes_lidar.relacionando_imagem_com_graus(imagem)

    imagem_cartesiana = mapa.transformando_polar_em_cartesiano(imagem_radianos, xGPS, yGPS, angulo_compass)
    mapa.desenhando_mapa_2D(pygame, surface, imagem_cartesiana, imagem_graus, xGPS, yGPS, angulo_compass)

    pygame.display.update()
    pygame.display.flip()
    mapa.encerra_mapa(pygame)

movimentar([0] * 6)

loop = True
posicaoX = 0
posicaoY = 0
correcao = False
rad_objetivo = 0

teste = True
rad_teste = 0

# Loop da simulação
while robot.step(TIME_STEP) != -1 and loop:

    # Definindo a velociade de movimento do robô para linha reta
    #movimentar(1)

    # Retornando a posição X e Y do robô
    xGPS, yGPS = funcoes_gps.retornando_posicao(GPS, _map)

    # Leitura do ângulo em radianos
    rad = funcoes_bussola.leitura_compass(compass)

    ang = rad * 180 / math.pi

    print(f"Ângulo robô: {ang}")
    print(f"Radianos: {rad}")

    # Desenhando um mapa em 2D com as leituras do Lidar e a posição do robô
    desenhando_mapa_lidar(xGPS, yGPS, rad, loop_limpeza= False)

    # Criando um controle do robô via teclados
    inteligencia.controle_robo_teclado(pygame, movimentar, girar_direita_proprio_eixo, girar_esquerda_proprio_eixo)

    if pygame.key.get_pressed()[pygame.K_s] == True:
        matriz = mapa.criando_matriz_cores_salva(pygame, surface)
        mapa.criando_mapa_com_matriz_salva(pygame, surface, matriz)
        mapa_compacto = mapa.criando_mapa_compacto(pygame, surface)
        mapa.desenhando_mapa_compacto(pygame, surface, mapa_compacto)

        posicaoX, posicaoY = inteligencia.coletando_posicao_mouse(mapa, pygame)
        posicao_roboX, posicao_roboY, posicao_objetivoX, posicao_objetivoY, x, y, rad_diferenca, beta = inteligencia.verificar_diferenca_angulo_objetivo(rad, (xGPS, yGPS), (posicaoX, posicaoY))
        correcao = True



