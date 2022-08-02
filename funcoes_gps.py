def iniciando_GPS(robot, TIME_STEP):
    # Iniciando o sensor Lidar
    GPS = robot.getDevice("gps")
    GPS.enable(TIME_STEP)

    return GPS

def retornando_posicao(GPS, _map):

    valores = GPS.getValues()
    x = valores[0]
    y = valores[2]

    '''
    
    Regra de três que representa o seguinte: Por meio de testes, percebi que o -6 até 6 no gps é o limite do meu mapa,
    isso significa que você precisa pegar esses valores testando manualmente ou definindo um valor alto.
    O 60 até 540 é o limite do tamanho da tela do pygame, apesar do meu pygame estar definido de 600 a 600, eu quis 
    fazer de 60 até 540 pra ter uma borda.
    
    O sinal do 6 pode deixar o mapa espelhado, cuidado.
    
    '''

    x = _map(x, 6, -6, 60, 540)
    y = _map(y, -6, 6, 540, 60)

    return x, y