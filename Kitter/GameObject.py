import pygame
import math

class GameObject:
    def __init__(self, pos, size, level_size_p):
        self.level_size_p = level_size_p
        self.mapdiag = math.sqrt(math.pow(level_size_p[0], 2) + math.pow(level_size_p[1], 2))
        self.bounds = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.ignore_bounds = False

    @property
    def left(self):
        return self.bounds.left
    @property
    def right(self):
        return self.bounds.right
    @property
    def top(self):
        return self.bounds.top
    @property
    def bottom(self):
        return self.bounds.bottom
    @property
    def width(self):
        return self.bounds.width
    @property
    def height(self):
        return self.bounds.height
    @property
    def center(self):
        return self.bounds.center
    @property
    def centerx(self):
        return self.bounds.centerx
    @property
    def centery(self):
        return self.bounds.centery
    
    def move(self, vx, vy):      
        #check for boundaries
        if not self.ignore_bounds:
            if self.left < 0:
                vx = 0
            if self.left < -vx:
                vx = -self.left
            if self.right > self.level_size_p[0] - 1:
                vx = 0
            if (self.level_size_p[0] - 1 - self.right) < vx:
                vx = self.level_size_p[0] - 1 - self.right
            if self.top < 0:
                vy = 0
            if self.top < -vy:
                vy = -self.top
            if self.bottom > self.level_size_p[1] - 1:
                vy = 0
            if (self.level_size_p[1] - 1 - self.bottom) < vy:
                vy = self.level_size_p[1] - 1 - self.bottom
        self.bounds = self.bounds.move((vx, vy))
    
    def setpos(self, pos):
        self.bounds = self.bounds.move((pos[0] - self.left, pos[1] - self.top))

    def distance(self, pos):
        dx = pos[0] - self.centerx
        dy = pos[1] - self.centery
        dist = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
        return (dx, dy, dist)
