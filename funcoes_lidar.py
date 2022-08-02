import math

def iniciando_lidar(robot, TIME_STEP, Lidar):
    # Iniciando o sensor Lidar
    lidar = robot.getDevice("lidar")
    Lidar.enable(lidar, TIME_STEP)
    Lidar.enablePointCloud(lidar)

    return lidar

def coletando_dados_lidar(lidar):
    # Coletando dado polar
    imagem = lidar.getRangeImage()

    return imagem

def imprimindo_imagem(imagem):
    print(imagem)

def relacionando_imagem_com_graus(imagem):
    quantidade_de_dados = len(imagem)

    # Cada leitura está com um ângulo em relação a outra leitura do sensor,
    # esse ângulo é o "angulo_divido", basicamente então, o ângulo interno de cada leitura.
    angulo_divido = 360 / quantidade_de_dados
    angulo = 360
    rad = 0
    distancia_com_angulo = []
    distancia_com_radianos = []

    # Para cada item dentro da imagem do Lidar
    for x in range(len(imagem)):
        # Se o objeto estiver muito perto do robô desconsiderar, pois pode ser alguma parte do próprio robô
        if imagem[x] < 0.4:
            # Transforma o valor muito perto em infinito, é uma coisa do próprio Lidar que estou usando, quando ele não lê nada, ele retorna -inf
            imagem[x] = -(math.inf)
        distancia_com_radianos.append([imagem[x], rad])
        distancia_com_angulo.append([imagem[x], angulo])
        angulo = angulo - angulo_divido
        # Transformando ângulo em radioanos para posteriormente aplicar a função math.sin() e math.cos()
        rad = (angulo * math.pi) / 180

    return distancia_com_radianos, distancia_com_angulo

