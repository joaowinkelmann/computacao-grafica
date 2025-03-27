# 1) Criar uma primitiva de triângulo e centralizar no meio da tela.
# 2) Adicionar cores aos vértices.
# 3) Desenhar os eixos para visualizar a centralização.
# 4) Após pressionar a tecla ESPAÇO, desenhar este mesmo triângulo sem
# cor de fundo, somente com cor nas linhas.
# Opcional: Desenhar outras formas geométricas para praticar
# Desafio: Utilizar VBOs

import glfw
from OpenGL.GL import *
import numpy as np
import ctypes
import math
import random

# variaveis globais
desenhar_linhas = False
shape_atual = "triangulo"
vbo = None
shader = None

def getVerticesTriangulo():
    vertices = np.array([
        # x, y, r, g, b
        0.0, 0.5, 1.0, 0.0, 0.0,  # vertice superior (vermelho)
        0.5, -0.5, 0.0, 1.0, 0.0,  # vertice inferior direito (verde)
        -0.5, -0.5, 0.0, 0.0, 1.0  # vertice inferior esquerdo (azul)
    ], dtype=np.float32)
    return vertices

def getVerticesQuadrado():
    vertices = np.array([
        # x, y, r, g, b
        -0.5, 0.5, 1.0, 0.0, 0.0,  # vertice superior esquerdo (vermelho)
        0.5, 0.5, 0.0, 1.0, 0.0,  # vertice superior direito (verde)
        0.5, -0.5, 0.0, 0.0, 1.0,  # vertice inferior direito (azul)
        -0.5, -0.5, 1.0, 1.0, 0.0  # vertice inferior esquerdo (amarelo)
    ], dtype=np.float32)
    return vertices

# numero de lados do poligono
# rotacao em graus
def getVerticesCircular(num_lados, rotacao_graus = 0):
    raio = 0.5
    vertices = []
    rotacao_radianos = math.radians(rotacao_graus)
    for i in range(num_lados):
        angulo = 2 * math.pi * i / num_lados + rotacao_radianos
        x = raio * math.cos(angulo)
        y = raio * math.sin(angulo)
        # cor aleatoria para cada vertice
        r = random.random()
        g = random.random()
        b = random.random()
        vertices.extend([x, y, r, g, b])
    return np.array(vertices, dtype=np.float32)

def main():
    global desenhar_linhas, shape_atual, vbo, shader
    if not glfw.init():
        return

    janela = glfw.create_window(800, 800, "Shapes com VBO", None, None)
    glfw.make_context_current(janela)

    glfw.swap_interval(1) # ativa o vsync

    # eventos de teclado
    def key_callback(window, key, scancode, action, mods):
        global desenhar_linhas, shape_atual, vbo
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            desenhar_linhas = not desenhar_linhas
        if key == glfw.KEY_1 and action == glfw.PRESS:
            shape_atual = "triangulo"
            setVBOVertices(getVerticesTriangulo())
        if key == glfw.KEY_2 and action == glfw.PRESS:
            shape_atual = "hexagono"
            setVBOVertices(getVerticesCircular(6))
        if key == glfw.KEY_3 and action == glfw.PRESS:
            shape_atual = "circulo"
            setVBOVertices(getVerticesCircular(100))
        if key == glfw.KEY_4 and action == glfw.PRESS:
            shape_atual = "quadrado"
            # setVBOVertices(getVerticesCircular(4, 45))
            setVBOVertices(getVerticesQuadrado())

    glfw.set_key_callback(janela, key_callback)

    # instancia o programa shader
    shader_program = initShader()
    glUseProgram(shader_program)

    # Inicializa o VBO com os dados do triângulo
    vbo = bindVBO(getVerticesTriangulo())

    while not glfw.window_should_close(janela):
        glClearColor(0, 0, 0, 1) # preto
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        eixos() # sempre desenha na ordem que foi definido aqui
        if shape_atual == "triangulo":
            drawShape(vbo, shader_program, 3)
        elif shape_atual == "hexagono":
            drawShape(vbo, shader_program, 6)
        elif shape_atual == "circulo":
            drawShape(vbo, shader_program, 100)
        elif shape_atual == "quadrado":
            drawShape(vbo, shader_program, 4)
        

        glfw.swap_buffers(janela)
        glfw.poll_events()

    glDeleteBuffers(1, [vbo]) # quando terminar, deleta o VBO
    glfw.terminate()

def initShader():
    # Vertex Shader
    vertex_shader = """
    #version 330 core
    layout (location = 0) in vec2 aPos;
    layout (location = 1) in vec3 aColor;
    out vec3 vertexColor;

    void main() {
        gl_Position = vec4(aPos.x, aPos.y, 0.0, 1.0);
        vertexColor = aColor;
    }
    """

    # Fragment Shader
    fragment_shader = """
    #version 330 core
    in vec3 vertexColor;
    out vec4 FragColor;

    void main() {
        FragColor = vec4(vertexColor, 1.0);
    }
    """

    # compila shaders
    vertexShaderObj = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertexShaderObj, vertex_shader)
    glCompileShader(vertexShaderObj)

    fragmentShaderObj = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragmentShaderObj, fragment_shader)
    glCompileShader(fragmentShaderObj)

    # cria o programa para ser retornado
    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertexShaderObj)
    glAttachShader(shaderProgram, fragmentShaderObj)
    glLinkProgram(shaderProgram)

    # Limpar
    glDeleteShader(vertexShaderObj)
    glDeleteShader(fragmentShaderObj)

    return shaderProgram

def bindVBO(vertices):
    global vbo
    # cria um VBO, passando o id
    vbo = glGenBuffers(1)

    # faz o vinculo do VBO ao buffer
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    # manda os dados pro VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # define os atributos de posição e cor
    # posição (x, y)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # cor (r, g, b)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(2 * 4))
    glEnableVertexAttribArray(1)

    return vbo

def setVBOVertices(vertices):
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

def drawShape(vbo, shader, num_vertices):
    glUseProgram(shader) # ativa o shader
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # habilita os atributos do VBO para serem acessados no shader
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    if desenhar_linhas:
        glDrawArrays(GL_LINE_LOOP, 0, num_vertices)
    else:
        glDrawArrays(GL_TRIANGLES, 0, num_vertices)

    # Desabilita os atributos do VBO após desenhar
    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)

def eixos():
    glUseProgram(0) # desliga o shader que a gente tava usando
    glBegin(GL_LINES)
    glColor3f(1, 1, 1) # branco
    glVertex2f(-1, 0)
    glVertex2f(1, 0)
    glVertex2f(0, -1)
    glVertex2f(0, 1)
    glEnd()

if __name__ == "__main__":
    main()