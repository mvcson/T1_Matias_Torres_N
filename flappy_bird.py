import glfw
import sys
from OpenGL.GL import *

from modelos import *
from controlador import Controller

if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 900
    height = 900

    window = glfw.create_window(width, height, 'FLAPPY BIRD MEGA ÉPICO', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    controlador = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controlador.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 1, 1, 1)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # HACEMOS LOS OBJETOS
    #Estas funciones tienen de nombre Egg debido a que usé como base el código entregado en clases para el juego del Chansey recoge huevos!
    pajaro = Pajaro(pipeline)
    eggs = EggCreator()

    controlador.set_model(pajaro)
    controlador.set_eggs(eggs)

    t0 = 0
    space = 0
    while not glfw.window_should_close(window): 

        # Calculamos el dt
        ti = glfw.get_time()
        dt = ti - t0
        t0 = ti

        # Using GLFW to check for input events
        glfw.poll_events()  # OBTIENE EL INPUT --> CONTROLADOR --> MODELOS

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        space+=1
        if space%400==0:
            eggs.create_egg(pipeline)  # Aleatorio

        eggs.update(1 * dt)  # 0.001
        pajaro.update(dt)

        # Creamos el límite
        pajaro.tope()  
        pajaro.collide_down(eggs)
        pajaro.collide_up(eggs)
        # DIBUJAR LOS MODELOS
        pajaro.draw(pipeline)
        eggs.draw(pipeline)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
