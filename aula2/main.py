# Requisitos
# pip install glfw PyOpenGL

import glfw
from OpenGL.GL import *

def main():
    if not glfw.init():
        return
    janela = glfw.create_window(800, 600, "Hello World", None, None)
    glfw.make_context_current(janela)

    while not glfw.window_should_close(janela):
        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)
        glClearColor(0, 0.7, 0.4, 1) # r, g, b, transparencia
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glfw.swap_buffers(janela)
        glfw.poll_events()

if __name__ == "__main__":
    main()