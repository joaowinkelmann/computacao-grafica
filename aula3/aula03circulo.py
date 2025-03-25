
import glfw
from math import cos, sin, pi
from OpenGL.GL import *

def main():
    if not glfw.init():
        return
    janela = glfw.create_window(800, 800, "Pacmano", None, None)
    glfw.make_context_current(janela)

    glfw.swap_interval(1) # ativa o vsync

    while not glfw.window_should_close(janela):
        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        eixos() # sempre desenha na ordem que foi definido aqui
        circulo(0.5, 100)
        # triangulo_pacman()

        # fazer o pacman abrir e fechar a boca com seno
        t = glfw.get_time()
        altura = 0.5 * sin(2 * t)
        triangulo_pacman_altura(altura)

        glfw.swap_buffers(janela)
        glfw.poll_events()


#eixos no x, y no centro da tela
def eixos():
    glBegin(GL_LINES)
    glColor3f(0.3, 0.4, 0.6)
    glVertex2f(-1, 0)
    glVertex2f(1, 0)
    glVertex2f(0, -1)
    glVertex2f(0, 1)
    glEnd()

def circulo(raio, segmentos):
    # glColor3f(1, 1, 1)
    glColor(1, 1, 0) # amarelo, pacman
    glBegin(GL_POLYGON)
    for i in range(segmentos):
        theta = 2.0 * pi * i / segmentos
        x = raio * cos(theta)
        y = raio * sin(theta)
        glVertex2f(x, y)
    glEnd()
# 
# def triangulo_pacman():
#     glBegin(GL_TRIANGLES)
#     glColor3f(0, 0, 0) # preto para ser a boca
#     glVertex2f(0, 0)
#     glVertex2f(0.5, 0.5)
#     glVertex2f(0.5, -0.5)
#     glEnd()

# recebe a altura como parametro da funcao do seno para abrir e fechar a boca
def triangulo_pacman_altura(altura):
    glBegin(GL_TRIANGLES)
    glColor3f(0, 0, 0) # preto para ser a boca
    glVertex2f(0, 0)
    glVertex2f(0.5, altura)
    glVertex2f(0.5, -altura)
    glEnd()


if __name__ == "__main__":
    main()