import math

def controle_robo_teclado(pygame, movimentar, girar_direita_proprio_eixo, girar_esquerda_proprio_eixo):
    # Criando um controle do robô via teclados
    if pygame.key.get_pressed()[pygame.K_UP] == True:
        movimentar([1, 1, 1, 1, 1, 1])
    if pygame.key.get_pressed()[pygame.K_DOWN] == True:
        movimentar([-1, -1, -1, -1, -1, -1])
    if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
        girar_direita_proprio_eixo()
    if pygame.key.get_pressed()[pygame.K_LEFT] == True:
        girar_esquerda_proprio_eixo()

def desenhando_mapa_lidar(xGPS, yGPS, angulo_compass, loop_limpeza, mapa, surface, funcoes_lidar, lidar, pygame):

    if loop_limpeza:
        # Essa função atualiza o mapa
        mapa.atualiza_mapa_preto(surface)

    # Coletando os dados do Sensor Lidar no robô
    imagem = funcoes_lidar.coletando_dados_lidar(lidar)
    # Criando uma lista com o valor da distância e do grau
    imagem_radianos, imagem_graus = funcoes_lidar.relacionando_imagem_com_graus(imagem)

    imagem_cartesiana = mapa.transformando_polar_em_cartesiano(imagem_radianos, xGPS, yGPS, angulo_compass)
    mapa.desenhando_mapa_2D(pygame, surface, imagem_cartesiana, imagem_graus, xGPS, yGPS)

    pygame.display.update()
    pygame.display.flip()
    mapa.encerra_mapa(pygame)

def coletando_posicao_mouse(mapa, pygame):
    escolha = True
    while escolha:
        pygame.display.update()
        pygame.display.flip()
        mapa.encerra_mapa(pygame)
        if pygame.mouse.get_pressed()[0] == True:
            print("Coletando a posição X e Y...")
            xy = pygame.mouse.get_pos()
            print(f"(X, Y): {xy}")
            print("Coletando posicao no mapa compacto...")
            posicaoX = int(xy[0] / 5)
            posicaoY = int(xy[1] / 5)
            print(f"(X, Y): {posicaoX, posicaoY}")
            escolha = False

            return posicaoX, posicaoY

def verificar_diferenca_angulo_objetivo(rad, posicao_robo, posicao_objetivo):
    rad = rad - 3.1415
    radRobo = rad
    ang = rad * 180 / math.pi

    print(f"Ângulo robô: {ang}")
    print(f"Radianos: {rad}")

    raio = 2

    x = (raio * math.cos(rad)) * 40
    # x = x - (imagem[i][0] * math.cos(angulo_compass)) * 40
    y = (raio * math.sin(rad)) * 40

    posicao_roboX = posicao_robo[0] #int(posicao_robo[0]/5)
    posicao_roboY = posicao_robo[1] #int(posicao_robo[1]/5)

    posicao_objetivoX = posicao_objetivo[0] * 5# int(posicao_robo[0]/5)
    posicao_objetivoY = posicao_objetivo[1] * 5# int(posicao_robo[1]/5)

    '''
    
        Para facilitar a conta, devemos transportar o vetor para a origem.
        
        novo ponto = (x2 - x1, y2 -y1)
    
    '''

    x1 = x
    y1 = y

    x2 = (posicao_objetivoX - posicao_roboX)
    y2 = (posicao_objetivoY - posicao_roboY)

    print(f"Vetor robô: {(x1, y1)}, vetor objetivo: {(x2, y2)}")

    '''
        
        Para descobrir o ângulo interno dos dois vetores, é necessário aplicar essa fórmula

                cos(a)=          x1 * x2 + y1 * y2
                                -------------------
                        raiz2(x1^2 + y1^2) *  raiz2(x2^2 + y2^2)

                ângulo = arccosseno(cos(a))

    '''

    cosseno = x1 * x2 + y1 * y2
    parte_de_baixo = math.sqrt((x1**2 + y1**2)) * math.sqrt((x2**2 + y2**2))
    cosseno = cosseno / parte_de_baixo
    print(f"Cosseno: {cosseno}, ang: {ang}")

    negativo = False
    if x2 < x1:
        negativo = True

    radDiferenca = math.acos(cosseno)
    radObjetivo = math.acos(cosseno)

    if negativo:
        radObjetivo = radObjetivo * -1

    angulo = rad*180 / math.pi

    #beta = radRobo + radDiferenca

    #if ang < 0:
    #    angulo = angulo * -1

    print(f"O robô está com {radObjetivo} radianos de diferança do objetivo!")

    return posicao_roboX, posicao_roboY, posicao_objetivoX, posicao_objetivoY, x, y, radDiferenca, radObjetivo

def corrigindo_angulo(rad, angulo_objetivo):
    if rad + angulo_objetivo > rad + 0.01 or angulo_objetivo < rad - 0.01:
        return True
