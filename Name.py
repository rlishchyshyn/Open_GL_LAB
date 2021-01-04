import pygame
import random
import hashlib
import win32api
import numpy as np

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


def load_model(file, scale=1.0):
    vert_coords = []
    faces = []

    for line in open(file, 'r'):
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue

        if values[0] == 'v':
            vert_coords.append([float(values[1]) / scale, float(values[2]) / scale, float(values[3]) / scale])

        if values[0] == 'f':
            face_i = []
            for v in values[1:4]:
                w = v.split('/')
                face_i.append(int(w[0]) - 1)

            faces.append(face_i)
    return vert_coords, faces


color = [0.95, 0.04, 0.04, 1.0]


def getVertex():
    verticies1, surfaces1 = load_model("Objects/name.obj", 20)
    verticies2, surfaces2 = load_model("Objects/Deer.obj", 300)
    v = []
    for surface in surfaces1:
        for vertex in surface:
            for i in verticies1[vertex]:
                v.append(i)
    for surface in surfaces2:
        for vertex in surface:
            for i in verticies2[vertex]:
                v.append(i)
    return v


verticies = getVertex()
data = (GLfloat * len(verticies))(*verticies)


def Mesh():
    glEnableClientState(GL_VERTEX_ARRAY)
    glColor4fv(color)
    glVertexPointer(3, GL_FLOAT, 0, np.array(data, dtype='float32'))
    glDrawArrays(GL_TRIANGLES, 0, len(data)//3)
    glDisableClientState(GL_VERTEX_ARRAY)


def init_screen_and_clock():
    global screen, display, clock
    pygame.init()
    WINDOW_SIZE = (800, 600)
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL, vsync=1)
    clock = pygame.time.Clock()
    gluPerspective(45, (WINDOW_SIZE[0] / WINDOW_SIZE[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)


init_screen_and_clock()


def start():
    rotator = [1, 0, 1, 0]
    sampleRate = 44100
    freq = 440
    # sampling frequency, size, channels, buffer
    pygame.mixer.init(44100, -16, 2, 512)
    arr = np.array([4096 * np.sin(2.0 * np.pi * freq * x / sampleRate) for x in range(0, sampleRate)]).astype(
        np.int16)
    arr2 = np.c_[arr, arr]
    global color
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    sound = pygame.sndarray.make_sound(arr2)
                    sound.play()
                elif event.button == 3:
                    color = [random.random(), random.random(), random.random(), 1.0]
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
            return 0
        if pressed[pygame.K_w]:
            rotator = [1, -1, 0, 0]
        if pressed[pygame.K_s]:
            rotator = [1, 1, 0, 0]
        if pressed[pygame.K_a]:
            rotator = [1, 0, -1, 0]
        if pressed[pygame.K_d]:
            rotator = [1, 0, 1, 0]

        glRotatef(rotator[0], rotator[1], rotator[2], rotator[3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Mesh()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    s = str(win32api.GetVolumeInformation("C:\\")[1])
    hash_object = hashlib.sha256(s.encode())
    hex_dig = hash_object.hexdigest()
    key = "56c0873f04ab380f6c92da3c530538fdf71479c3fb2075a80f7adb82138f8eeb"
    if hex_dig != key:
        win32api.MessageBeep(0)
        win32api.MessageBox(0, "Wrong key!", "3D Name", 0x00001000)
        exit(0)
    start()
