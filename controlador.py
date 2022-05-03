import glfw
import sys
from modelos import Pajaro, EggCreator
from typing import Optional

#Estas funciones tienen de nombre Egg debido a que usé como base el código entregado en clases para el juego del Chansey recoge huevos!

class Controller(object):
    model: Optional['Pajaro'] 
    eggs: Optional['EggCreator']

    def __init__(self):
        self.model = None
        self.eggs = None

    def set_model(self, m):
        self.model = m

    def set_eggs(self, e):
        self.eggs = e

    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            glfw.terminate()
            sys.exit()

        elif key == glfw.KEY_UP and action == glfw.PRESS:
            self.model.move_up()


