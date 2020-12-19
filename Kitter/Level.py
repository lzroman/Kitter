import pygame, PhysObject, GameObject
from random import randint

class Level:
    def __init__(self, size):
        self.textures_n = 4
        self.textures = []
        self.body = []
        self.size = size

        temp = []
        for i in range(self.size[0]):
            temp.clear()
            for j in range(self.size[1]):
                temp.append(randint(0, self.textures_n - 1))
            self.body.append(temp[:])
        for i in range(self.textures_n):
            self.textures.append(pygame.image.load("data\\sprites\\back_" + str(i) + ".png"))      
        self.textures_size = self.textures[0].get_size()
        self.level_size_p = (self.textures_size[0] * (self.size[0] - 1), self.textures_size[1] * (self.size[1] - 1))

        self.bushes_n = 4
        self.bushes = []
        self.bushes_phys = []
        for i in range(self.bushes_n):
            self.bushes.append(pygame.image.load("data\\sprites\\bush_" + str(i) + ".png"))
        self.bushes_size = self.bushes[0].get_size()
        for i in range(self.size[0] * self.size[1] // 10):
            self.bushes_phys.append(PhysObject.PhysObject((randint(0, self.level_size_p[0] - self.bushes_size[0] - 1), randint(0, self.level_size_p[1] - self.bushes_size[1] - 1)), self.bushes_size, self.level_size_p))
            self.bushes_phys[i].set_states([PhysObject.State([self.bushes[randint(0, self.bushes_n - 1)]], lambda: None)])

        self.safespace_texture = pygame.image.load("data\\sprites\\safespace.png")
        self.safespace_size = self.safespace_texture.get_size()
        self.safespace_pos = ((self.level_size_p[0] - self.safespace_size[0]) / 2 - 1, self.level_size_p[1] - self.safespace_size[1] - 1)
        self.safespace = PhysObject.PhysObject(self.safespace_pos, self.safespace_size, self.level_size_p)
        self.safespace.set_states([PhysObject.State([self.safespace_texture], lambda: None)])
