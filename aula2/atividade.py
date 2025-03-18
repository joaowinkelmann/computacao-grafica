# Requisitos
# pip install glfw PyOpenGL

import glfw
from OpenGL.GL import *
import random
import time

def main():
    if not glfw.init():
        return
    janela = glfw.create_window(640, 480, "Rave", None, None)
    glfw.make_context_current(janela)

    timestamp = time.time()
    background_color = [random.random(), random.random(), random.random(), 1] # r, g, b, alpha
    tempo_troca = 1 # segundos para cada troca de cor

    while not glfw.window_should_close(janela):

        # se apertar "seta pra cima" ou "seta pra baixo", muda o tempo de troca
        # por algum motivo ele faz esse check a cada frame, entao a troca tem que ser um valor bem pequeno
        if glfw.get_key(janela, glfw.KEY_UP) == glfw.PRESS:
            tempo_troca += 0.001
        if glfw.get_key(janela, glfw.KEY_DOWN) == glfw.PRESS:
            tempo_troca -= 0.001

        # previne epilepsia
        if tempo_troca < 0.1:
            tempo_troca = 0.1

        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)

        # timer pra ficar trocando a cada "tempo_troca" segundos
        tempo_atual = time.time()
        if tempo_atual - timestamp >= tempo_troca: # ta na hora de trocar
            # pega um float pra cada um dos RGB
            background_color = [random.random(), random.random(), random.random(), 1]
            timestamp = tempo_atual

        glClearColor(*background_color) # seta o fundo da janela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # limpa os buffer

        glfw.swap_buffers(janela) # manda o back buffer pro front buffer
        glfw.poll_events() # escuta eventos na janela

    glfw.terminate() # morre

if __name__ == "__main__":
    main()