import pygame, math
from GameObject import GameObject
from random import randint

class Camera(GameObject):

    def __init__(self, pos, size, level, cat, kitties, drawing, screen, level_size_p):
        self.about_state = False
        self.drawing = []
        self.rain = []
        self.rain_n = 3
        self.rain_range = []
        self.rain_state = 0
        self.light_next = 100
        self.light_state = 0
        self.sound_channel = pygame.mixer.Channel(0)
        self.light_sound = pygame.mixer.Sound("data\\sounds\\light.wav")
        for i in range(self.rain_n):
            self.rain.append(pygame.image.load("data\\sprites\\rain_" + str(i) + ".png"))
        self.rain_size = self.rain[0].get_size()
        super().__init__(pos, size, level_size_p)
        self.screen = screen
        self.drawing += drawing
        self.level = level
        self.cat = cat
        self.w3 = size[0] / 3
        self.w23 = 2 * size[0] / 3
        self.h3 = size[1] / 3
        self.h23 = 2 * size[1] / 3
        self.rain_range.append(self.width // self.rain_size[0] + 1)
        self.rain_range.append(self.height // self.rain_size[1] + 1)
        self.heart = pygame.image.load("data\\sprites\\heart.png")
        self.heart_size = self.heart.get_size()
        self.heart_small = pygame.image.load("data\\sprites\\heart_small.png")
        self.heart_small_size = self.heart_small.get_size()
        self.follow_dog = pygame.image.load("data\\sprites\\follow_dog.png")
        self.follow_dog_size = self.follow_dog.get_size()
        self.heart_dist = 64
        self.heart_time = 30
        self.heart_time2 = self.heart_time / 2
        self.kitties = kitties
        self.kitties_all = len(kitties)
        self.hit = []
        for i in range(self.cat.hit_n):
            self.hit.append(pygame.image.load("data\\sprites\\hit\\hit_" + str(i) + ".png"))
        self.hit_size = self.hit[0].get_size()
    
    def get_local(self, obj):
        return (obj.left - self.left, obj.top - self.top)

    def draw(self):
        #kinetic scroll
        speed_x = 0
        speed_y = 0
        if self.cat_local[0] + self.cat.width > self.w23:
            speed_x = self.cat.speed * (6 * (self.cat_local[0] + self.cat.width) - 4 * self.width) / self.width
        elif self.cat_local[0] < self.w3:
            speed_x = self.cat.speed * (6 * self.cat_local[0] - 2 * self.width) / self.width
        if self.cat_local[1] + self.cat.height > self.h23:
            speed_y = self.cat.speed * (6 * (self.cat_local[1] + self.cat.height) - 4 * self.height) / self.height
        elif self.cat_local[1] < self.h3:
            speed_y = self.cat.speed * (6 * self.cat_local[1] - 2 * self.height) / self.height
        if speed_x or speed_y:
            self.move(speed_x, speed_y)

        self.draw_level()

        for i in self.drawing:
            if (i.right >= self.left and i.bottom >= self.top) and (i.left <= self.right and i.top <= self.bottom):
                i.draw(self.screen, self.get_local(i))

        self.cat.draw(self.screen, self.get_local(self.cat))
        
        if self.cat.hit_state != 5:
            self.screen.blit(self.hit[self.cat.hit_state], (self.cat_local_center[0] - self.hit_size[0] / 2, self.cat_local_center[1] - self.hit_size[1] / 2))
            self.cat.hit_state += 1

        self.draw_bushes()

        for kitty in self.kitties:
            if kitty.is_follow:
                if kitty.master == self.cat:
                    self.screen.blit(self.heart_small, (kitty.centerx - self.left - self.heart_small_size[0] / 2, kitty.top - self.top - self.heart_small_size[1]))
                else:
                    self.screen.blit(self.follow_dog, (kitty.centerx - self.left - self.follow_dog_size[0] / 2, kitty.top - self.top - self.follow_dog_size[1]))               

        for kitty in self.cat.kitties_near:
            dist = self.cat.distance(kitty[0].center)
            if dist[2] < self.heart_dist:
                pos = (self.cat_local_center[0] + dist[0] - self.heart_size[0] / 2, self.cat_local_center[1] + dist[1] - self.heart_size[1] / 2)
            else:
                pos = (self.cat_local_center[0] + dist[0] * self.heart_dist / dist[2] - self.heart_size[0] / 2, self.cat_local_center[1] + dist[1] * self.heart_dist / dist[2] - self.heart_size[1] / 2)
            
            temp = pygame.Surface((self.width, self.height)).convert()
            temp.blit(self.screen, (0, 0))
            temp.blit(self.heart, pos)
            if dist[2] < self.cat.kitties_detectable:
                k = 256 * (1 - dist[2] / self.cat.kitties_detectable)
            else:
                k = 0
            if kitty[1] < self.heart_time2:
                k = k * kitty[1] / self.heart_time2
                kitty[1] += 1
            elif kitty[1] < self.heart_time:
                k = k *  (self.heart_time - kitty[1]) / self.heart_time2
                kitty[1] += 1
            else:
                self.cat.kitties_near.remove(kitty)
                k = 0
            temp.set_alpha(k)
            self.screen.blit(temp, (0, 0))

        self.draw_dark()
        self.draw_rain()
        self.draw_lightning()
        if self.about_state:
            self.about()
        self.draw_gui()
        
    def draw_rain(self):
        if not self.rain_state < self.rain_n:
            self.rain_state = 0
        for i in range(self.rain_range[0]):
            for j in range(self.rain_range[1]):
                self.screen.blit(self.rain[self.rain_state], (self.rain_size[0] * i, self.rain_size[1] * j))
        self.rain_state += 1

    def draw_lightning(self):
        if self.light_state == self.light_next:
            self.sound_channel.play(self.light_sound)
            l = pygame.Surface((self.width, self.height))
            l.set_alpha(128)
            l.fill((255,255,255))
            self.screen.blit(l, (0,0))
            self.light_state = 0
            self.light_next = randint(10, 500)
        self.light_state += 1
    
    def draw_dark(self):
        l = pygame.Surface((self.width, self.height))
        l.set_alpha(64)
        l.fill((0,0,0))
        self.screen.blit(l, (0,0))

    def draw_level(self):
        left = self.left // self.level.textures_size[0]
        top = self.top // self.level.textures_size[1]
        right = self.right // self.level.textures_size[0] + 1
        bottom = self.bottom // self.level.textures_size[1] + 1

        for i in range(left, right):
            for j in range(top, bottom):
                self.screen.blit(self.level.textures[self.level.body[i][j]], (self.level.textures_size[0] * i - self.left, self.level.textures_size[1] * j - self.top))

    def draw_bushes(self):
        for i in self.level.bushes_phys:
            if (i.right >= self.left and i.bottom >= self.top) and (i.left <= self.right and i.top <= self.bottom):
                i.draw(self.screen, self.get_local(i))

    @property
    def cat_local(self):
        return (self.cat.left - self.left, self.cat.top - self.top)
    
    @property
    def cat_local_center(self):
        return (self.cat.centerx - self.left, self.cat.centery - self.top)

    def about_switch(self):
        self.about_state = not self.about_state
    
    text = ["save all kitties! accompany them to the house!", "but be aware of dogs - they take away kitties!", "arrows - move", "c - call kitties", "x - switch following", "z - hit", "all textures and sounds are stolen for educational purposes", "ihbg@bk.ru", "goulash", "2019"]

    def about(self):
        for i in range(len(self.text)):
            self.screen.blit(pygame.font.SysFont("comicsansms", 20).render(self.text[i], False, (255,255,255)), (self.width / 10, self.height / 4 + i * 25))

    def draw_gui(self):
        text = ["Kitties saved:", str(self.kitties_all - len(self.kitties)) + " / " + str(self.kitties_all)]
        for i in range(len(text)):
            self.screen.blit(pygame.font.SysFont("comicsansms", 20).render(text[i], False, (255,255,255)), (self.width / 10, self.height / 10 + i * 25))
