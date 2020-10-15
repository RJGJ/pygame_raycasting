from pygame.locals import *
from random import randint
from scipy.spatial import distance

import pygame as pg
import numpy as np 
import vectormath as vmath
import math

pg.init()
surface = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
font = pg.font.Font(None, 30)
# DISPLAY SIZE
W, H = pg.display.get_surface().get_size()


class Boundary():
    
    def __init__(self, x1, y1, x2, y2):
        self.a = vmath.Vector2(x1, y1)
        self.b = vmath.Vector2(x2, y2)
        
    def draw(self):
        pg.draw.line(surface, 
            pg.Color('white'), self.a, self.b, 5)


class Ray():
    
    def __init__(self, pos, angle):
        self.pos = pos
        self.dir = vmath.Vector2(math.cos(angle),
            math.sin(angle))
        
    def look_at(self, x, y):
        self.dir.x = x - self.pos.x
        self.dir.y = y - self.pos.y
        self.dir.normalize()
        
    def draw(self):
        pg.draw.line(surface, 
            pg.Color('white'), self.pos, 
            self.dir * 1 + self.pos)
            
    def cast(self, wall):
        x1 = wall.a.x
        y1 = wall.a.y
        x2 = wall.b.x
        y2 = wall.b.y
        
        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y
        
        den = (x1 - x2) * (y3 - y4) - \
            (y1 - y2) * (x3 - x4)
        
        if den == 0:
            return vmath.Vector2(None)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * \
            (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * \
            (x1 - x3)) / den
        
        if t > 0 and t < 1 and u > 0:
            pt = vmath.Vector2(x1 + t * (x2 - x1),
                y1 + t * (y2 - y1))
            return pt
        else:
            return vmath.Vector2(None)


class Particle():
    
    def __init__(self):
        self.pos = vmath.Vector2(W // 2, H // 2)
        self.rays = []
        
        for i in range(0, 360, 5):
            self.rays.append(Ray(self.pos, 
                math.radians(i)))
                
    def look(self, walls):
        for ray in self.rays:
            
            closest = None
            record = 999_999
            for wall in walls:
                
                pt = ray.cast(wall)
                if not (pt.x == 0 and pt.y == 0):
                    
                    d = distance.euclidean(self.pos, pt)
                    if d < record:
                        record = d
                        closest = pt
            if not closest is None:
                pg.draw.line(surface, 
                    pg.Color('white'), self.pos, closest)
    
    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y
    
    def draw(self):
        pg.draw.circle(surface, pg.Color('white'),
            self.pos, 20)
        for ray in self.rays:
            ray.draw()
    

# SETUP
walls = []
walls.append(Boundary(0, 0, W, 0))
walls.append(Boundary(W, 0, W, H))
walls.append(Boundary(W, H, 0, H))
walls.append(Boundary(0, H, 0, 0))
for _ in range(5):
    walls.append(Boundary(randint(0, W), randint(0, H), 
        randint(0, W), randint(0, H)))

ray = Ray(100, 1000)
particle = Particle()


while True:
    for ev in pg.event.get():
        if ev.type == QUIT:
            pg.quit()
    clock.tick(60)
    surface.fill(pg.Color('black'))
    
    # LOGIC HERE
    mouse_pos = pg.mouse.get_pos()
    
    # DRAW HERE
    #pg.draw.circle(
    #   surface, pg.Color('blue'), mouse_pos, 50)
    
    # draw walls ;)
#   pg.draw.line(surface, pg.Color('white'), 
#       (0, 0), (W, 0), 5)
#   pg.draw.line(surface, pg.Color('white'), 
#       (W, 0), (W, H), 5)
#   pg.draw.line(surface, pg.Color('white'), 
#       (W, H), (0, H), 5)
#   pg.draw.line(surface, pg.Color('white'), 
#       (0, H), (0, 0), 5)
    
    for wall in walls:
        wall.draw()
    
    particle.update(mouse_pos[0], mouse_pos[1])
    particle.draw()
    particle.look(walls)
    
    
    fps = font.render(str(int(clock.get_fps())), 
        True, pg.Color('red'))
    surface.blit(fps, (50, 50))
    pg.display.update()