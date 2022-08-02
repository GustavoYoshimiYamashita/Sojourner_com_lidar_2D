import math
import numpy as np

''' Variáveis para o Pygame'''

# Inicializando cor
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
white = (255, 255, 255)
vertical = 600
horizontal = 600
centroY = int(vertical/2)
centroX = int(horizontal/2)

tamanho = 120

def iniciando_mapa(pygame):
    surface = pygame.display.set_mode((horizontal, vertical))
    return surface

def encerra_mapa(pygame):
    for event in pygame.event.get():
        if event.type == 256:
            pygame.quit()
            exit()

def atualiza_mapa_preto(surface):
    surface.fill(black)

def transformando_polar_em_cartesiano(imagem, xGPS, yGPS, angulo_compass):
    '''
        Fórmula de transformação de coordenada polar para cartesiana
        x = r*cos(grau)
        y = r*sen(grau)
    '''

    imagem_cartesiana = []

    for i in range(len(imagem)):
        x = (imagem[i][0] * math.cos(imagem[i][1] - angulo_compass)) * 40
        #x = x - (imagem[i][0] * math.cos(angulo_compass)) * 40
        y = (imagem[i][0] * math.sin(imagem[i][1] - angulo_compass)) * 40
        #y = y - (imagem[i][0] * math.cos(angulo_compass)) * 40

        #print(f"x: {x:,.2f}, y: {y:,.2f}")
        #print(f"xGPS: {xGPS:,.2f}, yGPS: {yGPS:,.2f}")
        imagem_cartesiana.append([x + xGPS, -y + yGPS])

    return imagem_cartesiana

def desenhando_mapa_2D(pygame,surface, imagem_cartesiana, imagem_graus, xGPS, yGPS, angulo_compass):

    x = 100 * math.cos(angulo_compass - 3.1415)
    y = 100 * math.sin(angulo_compass - 3.1415)

    #print(f"ang: {angulo_compass}")

    x2 = x
    y2 = y
    xGPS2 = xGPS
    yGPS2 = yGPS

    pygame.draw.line(surface, black, (xGPS, yGPS), (xGPS + x, yGPS + y), 5)



    # Desenhando cada pontinho detectado pelo Lidar
    for i in range(len(imagem_cartesiana)):
        grau = imagem_graus[i][1]

        # Caso o valor retornado seja infinito, isso significa que nada foi detectado dentro dos 8 metros de leitura do sensor Lidar,
        # então, deve se pintar de preto.
        if imagem_cartesiana[i][0] == math.inf:
            imagem_cartesiana[i][0] = 7.6
            imagem_cartesiana[i][1] = 7.6
            x = (imagem_cartesiana[i][0] * math.cos(grau - angulo_compass)) * 40
            # x = x - (imagem[i][0] * math.cos(angulo_compass)) * 40
            y = (imagem_cartesiana[i][0] * math.sin(grau- angulo_compass)) * 40

            pygame.draw.line(surface, black, (xGPS, yGPS), (x + xGPS, y + yGPS), 1)

        pygame.draw.line(surface, black, (xGPS, yGPS), (imagem_cartesiana[i][0], imagem_cartesiana[i][1]), 1)
        pygame.draw.circle(surface, white, (imagem_cartesiana[i][0], imagem_cartesiana[i][1]), 1)

        #print(f"X: {imagem_cartesiana[i][0]}, Y: {imagem_cartesiana[i][1]}")

        # Desenhando um círculp no meio para identificar o robô
        pygame.draw.circle(surface, red, (xGPS, yGPS), 4)

        pygame.draw.line(surface, red, (xGPS2, yGPS2), (xGPS2 + x2, yGPS2 + y2), 1)



def salva_cor_pixels(pygame, surface, coordenadas):
    cor = surface.get_at(coordenadas)
    return cor

def criando_matriz_cores_salva(pygame, surface):
    matriz = []
    for vertical in range(600):
        for horizontal in range(600):
            cor = salva_cor_pixels(pygame, surface, coordenadas=(vertical, horizontal))
            matriz.append([vertical, horizontal, cor[:3]])
    return matriz

def criando_mapa_com_matriz_salva(pygame, surface, matriz):
    for vertical in range(600):
        for horizontal in range(600):
            cor = matriz[vertical*600+horizontal][2]
            surface.set_at((vertical, horizontal), cor)

def criando_mapa_compacto(pygame, surface):
    # Criando uma matriz para representar o ambiente
    mapa_compacto = []

    for ii in range(tamanho):
        mapa_compacto.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    print(mapa_compacto)

    # Detectando se existe parede em cada célula
    for celulasX in range(tamanho): # verificando as 20 células da vertical
        for celulasY in range(tamanho): # verificando as 20 células da horizontal
            parede = False
            #print("---------------------------------")
            #print(f"Analisando a célula: {celulasX, celulasY}")
            for x in range(int(vertical/tamanho)): # Verificando os 30 pixels de cada célula na vertical
                for y in range(int(vertical/tamanho)): # Verificando os 30 pixels de cada célula na Horizontal, totalizando 600 pixels no final
                    # Pegando o valor do pixel pra saber se é um obstáculo
                    cor = surface.get_at((x + celulasX  * int(vertical/tamanho), y + celulasY * int(vertical/tamanho)))
                    # Se a cor for um obstáculo, então marcar aquela célula como uma parede
                    if cor[:3] == (255, 255, 255):
                        parede = True
            if parede == True:
                # O valor -1 representa uma parede
                mapa_compacto[celulasX][celulasY] = -1
                #print("Parede detectada!")
            else:
                # O valor 10 representa a parede
                mapa_compacto[celulasX][celulasY] = 10
                #print("Parede não detectada!")

    # Imprimindo o mapa
    for x in range(tamanho):
        print("[", end='')
        for y in range(tamanho):
            print(f"{mapa_compacto[y][x]},", end='')
        print("],")

    # Desenhando linhas no mapa para motrar a divisão criada
    for i in range(tamanho+1):
        pygame.draw.line(surface, green, (i*int(vertical/tamanho), 0), (i*int(vertical/tamanho), 600), 1)
        pygame.draw.line(surface, green, (0, i*int(vertical/tamanho)), (600, i*int(vertical/tamanho)), 1)

    print("terminei")
    return mapa_compacto

def desenhando_mapa_compacto(pygame, surface, mapa_compacto):

    for celulasX in range(tamanho):  # verificando as 20 células da vertical
        for celulasY in range(tamanho):  # verificando as 20 células da horizontal
            for x in range(int(vertical / tamanho)):  # Verificando os 30 pixels de cada célula na vertical
                for y in range(int(vertical / tamanho)):  # Verificando os 30 pixels de cada célula na Horizontal, totalizando 600 pixels no final
                    if mapa_compacto[celulasX][celulasY] == 10:
                        pygame.draw.circle(surface, black, (x + celulasX * int(vertical/tamanho), y + celulasY * int(vertical/tamanho)), 1)
                    else:
                        pygame.draw.circle(surface, white, (x + celulasX * int(vertical / tamanho), y + celulasY * int(vertical / tamanho)), 1)
    # Desenhando linhas no mapa para motrar a divisão criada
    #for i in range(tamanho+1):
    #    pygame.draw.line(surface, green, (i*int(vertical/tamanho), 0), (i*int(vertical/tamanho), 600), 1)
    #    pygame.draw.line(surface, green, (0, i*int(vertical/tamanho)), (600, i*int(vertical/tamanho)), 1)