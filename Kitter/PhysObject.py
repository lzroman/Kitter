import pygame, math
from GameObject import GameObject

class State:
    def __init__(self, texture, action):
        self.texture = texture
        self.action = action

class PhysObject(GameObject):

    def __init__(self, pos, size, level_size_p):
        super().__init__(pos, size, level_size_p)
        self.states = []
        self.state = 0
        self.anim_state = 0
    
    def set_states(self, states):
        for i in states:
            self.states.append(i)
    
    def draw(self, screen, pos):
        if not self.anim_state < len(self.states[self.state].texture):
            self.anim_state = 0
        screen.blit(self.states[self.state].texture[self.anim_state], (pos[0], pos[1]))
        self.anim_state += 1
    
    def update(self):
        self.states[self.state].action()
