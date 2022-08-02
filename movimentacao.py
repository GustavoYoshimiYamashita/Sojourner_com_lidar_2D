

def set_steering_angle(wheel_angle, motores_angulo):
    back_left_angle = wheel_angle[0]
    back_right_angle = wheel_angle[1]
    front_left_angle = wheel_angle[2]
    front_right_angle = wheel_angle[3]

    motores_angulo[0].setPosition(back_left_angle)
    motores_angulo[1].setPosition(back_right_angle)
    motores_angulo[2].setPosition(front_left_angle)
    motores_angulo[3].setPosition(front_right_angle)

def set_speed(velocity, motores_velocidade):
    motores_velocidade[0].setVelocity(velocity[0])
    motores_velocidade[1].setVelocity(velocity[1])
    motores_velocidade[2].setVelocity(velocity[2])
    motores_velocidade[3].setVelocity(velocity[3])
    motores_velocidade[4].setVelocity(velocity[4])
    motores_velocidade[5].setVelocity(velocity[5])

def iniciando_motores(robot):
    # Definindo as partes de movimentação do robô
    back_left_arm = robot.getDevice('BackLeftArm')
    back_left_wheel = robot.getDevice('BackLeftWheel')
    back_right_arm = robot.getDevice('BackRightArm')
    back_right_wheel = robot.getDevice('BackRightWheel')
    front_left_arm = robot.getDevice('FrontLeftArm')
    front_left_wheel = robot.getDevice('FrontLeftWheel')
    front_right_arm = robot.getDevice('FrontRightArm')
    front_right_wheel = robot.getDevice('FrontRightWheel')
    middle_left_wheel = robot.getDevice('MiddleLeftWheel')
    middle_right_wheel = robot.getDevice('MiddleRightWheel')

    # Definindo o giro da roda como infinito
    back_left_wheel.setPosition(float('inf'))
    back_right_wheel.setPosition(float('inf'))
    front_left_wheel.setPosition(float('inf'))
    front_right_wheel.setPosition(float('inf'))
    middle_left_wheel.setPosition(float('inf'))
    middle_right_wheel.setPosition(float('inf'))

    # Motores Velocidade
    motores_velocidade = [back_left_wheel, back_right_wheel, front_left_wheel, front_right_wheel, middle_left_wheel,
                          middle_right_wheel]
    # Motores angulo
    motores_angulo = [back_left_arm, back_right_arm, front_left_arm, front_right_arm]

    return motores_velocidade, motores_angulo
