import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es

from OpenGL.GL import *
import random
from typing import List

def create_gpu(shape, pipeline):
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpu


class Pajaro(object):

    def __init__(self, pipeline):
        # Modelación jerárquica con grafo
        gpu_body_quad = create_gpu(bs.createColorQuad(0.8, 0.7, 0.4), pipeline)  # cafe claro
        gpu_pico_quad = create_gpu(bs.createColorQuad(0.2, 0.1, 0), pipeline)  # cafe
        gpu_eye_quad = create_gpu(bs.createColorQuad(1, 1, 1), pipeline)  # blanco
        gpu_ala_quad = create_gpu(bs.createColorQuad(0.6, 0.5, 0.3), pipeline) #blanco

        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(1)
        body.childs += [gpu_body_quad]

        # Creamos el pico
        pico = sg.SceneGraphNode('Pico') 
        pico.transform = tr.scale(0.6, 0.3, 1)
        pico.childs += [gpu_pico_quad]

        # Rotacion del pico del pájaro
        rot_pico = sg.SceneGraphNode('rotar pico')
        rot_pico.transform = tr.translate(0.55, -0.05, 0)  # tr.matmul([])..
        rot_pico.childs += [pico]

        # Ojitos
        eye = sg.SceneGraphNode('eye')
        eye.transform = tr.scale(0.2, 0.2, 1)
        eye.childs += [gpu_eye_quad]

        eye_der = sg.SceneGraphNode('eyeRight')
        eye_der.transform = tr.translate(0.28, 0.3, 0)
        eye_der.childs += [eye]

        # Ala
        ala = sg.SceneGraphNode('ala')
        ala.transform = tr.scale(0.36, 0.7, 1)
        ala.childs += [gpu_ala_quad]

        # Rot Ala
        rot_ala = sg.SceneGraphNode('rotar ala')
        rot_ala.transform = tr.translate(-0.15, -0.3, 0)
        rot_ala.childs += [ala]

        # Ensamblamos el mono
        mono = sg.SceneGraphNode('pajaro')
        mono.transform = tr.matmul([tr.scale(0.15, 0.15, 0), tr.translate(0, 0, 0)])
        mono.childs += [body, rot_pico, rot_ala, eye_der]

        transform_mono = sg.SceneGraphNode('pajaroTR')
        transform_mono.childs += [mono]

        self.model = transform_mono
        self.pos_y = 0.4 
        self.pos = 0
        self.alive = True

    def move_up(self):
        if not self.alive:
            return
        self.pos_y += 0.3

    def draw(self, pipeline):
            self.model.transform = tr.translate(0, self.pos_y, 0)
            sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def update(self, dt):
        if not self.alive:
            return
        self.pos_y -= 0.7*dt

    def die(self):  
        glClearColor(1, 0, 0, 1)  
        self.on = False
    
    def tope(self):
        if self.pos_y < -0.8:
                self.die()
                self.alive = False
        elif self.pos_y>1:
                self.die()
                self.alive=False
    
    def modifymodel(self):
        self.model.transform = tr.translate(0, self.y, 0)

    def collide_up(self, eggs: 'EggCreator'):
        if not eggs.on: 
            return
        deleted_eggs = []

        for e in eggs.eggs:
            if self.alive==False:
                return
            else:
                if e.pos_y==0.7:
                    if -0.4<e.pos_x<-0.1 and self.pos_y+1>(e.pos_y+0.7):
                        print('GAME OVER')  
                        eggs.die()  
                        self.alive = False
                if e.pos_y==0.8:
                    if -0.4<e.pos_x<-0.1 and self.pos_y+1>(e.pos_y+0.8):
                        print('GAME OVER')  
                        eggs.die()  
                        self.alive = False
                if e.pos_y==0.9:
                    if -0.4<e.pos_x<-0.1 and self.pos_y+1>(e.pos_y+0.9):
                        print('GAME OVER') 
                        eggs.die()  
                        self.alive = False


    def collide_down(self, eggs: 'EggCreator'):
        if not eggs.on:  
            return
        deleted_eggs = []
        for e in eggs.eggs:
            if self.alive==False:
                return
            else:    
                if e.pos_y==0.7:
                    if -0.4<e.pos_x<-0.1 and (e.pos_y-0.28)>(self.pos_y+1):
                        print('GAME OVER') 
                        eggs.die()  
                        self.alive = False
                if e.pos_y==0.8:
                    if -0.4<e.pos_x<-0.1 and (e.pos_y-0.35)>(self.pos_y+1):
                        print('GAME OVER') 
                        eggs.die()  
                        self.alive = False
                if e.pos_y==0.9:
                    if -0.4<e.pos_x<-0.1 and (e.pos_y-0.40)>(self.pos_y+1):
                        print('GAME OVER') 
                        eggs.die()  
                        self.alive = False

#Estas funciones tienen de nombre Egg debido a que usé como base el código entregado en clases para el juego del Chansey recoge huevos!
class Egg(object):

    def __init__(self, pipeline):
        gpu_egg = create_gpu(bs.createColorQuad(0.15, 0.7, 0.36), pipeline)
        
        egg = sg.SceneGraphNode('leg')
        egg.transform = tr.scale(0.33,0.7, 1)
        egg.childs += [gpu_egg]

        egg_izq = sg.SceneGraphNode('legLeft')
        egg_izq.transform = tr.translate(0.7, 1, 0)  # tr.matmul([])..
        egg_izq.childs += [egg]

        egg_der = sg.SceneGraphNode('legRight')
        egg_der.transform = tr.translate(0.7, -1, 0)
        egg_der.childs += [egg]
        
        mono = sg.SceneGraphNode('pajaro')
        mono.transform = tr.matmul([tr.scale(0.6, 1, 0), tr.translate(0,-0.55, 0)])
        mono.childs += [egg_izq, egg_der]
        transform_mono = sg.SceneGraphNode('pajaroTR')
        transform_mono.childs += [mono]
        self.pos_y = random.choice([0.7,0.8,0.9,])
        self.pos_x = 1  
        self.model = transform_mono

    def draw(self, pipeline):
        self.model.transform = tr.translate(self.pos_x, 0.7*self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def update(self, dt):
        self.pos_x -= dt


class EggCreator(object):
    eggs: List['Egg']

    def __init__(self):
        self.eggs = []
        self.on = True

    def die(self):
        glClearColor(1, 0, 0, 1) 
        self.on = False

    def create_egg(self, pipeline):
        self.eggs.append(Egg(pipeline))

    def draw(self, pipeline):
        for k in self.eggs:
            k.draw(pipeline)

    def update(self, dt):
        for k in self.eggs:
            k.update(dt)

    def delete(self, d):
        if len(d) == 0:
            return
        remain_eggs = []
        for k in self.eggs:  
            if k not in d:  
                remain_eggs.append(k)
        self.eggs = remain_eggs  
