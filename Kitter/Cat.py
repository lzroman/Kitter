import pygame, math, PhysObject
from Actor import Actor

class Cat(Actor):
    def __init__(self, pos, level_size_p, kitties, kitties_del, dogs):
        self.is_with_kitty = False
        self.sound_channel = pygame.mixer.Channel(1)
        self.meow_sound = pygame.mixer.Sound("data\\sounds\\cat.wav")
        self.ask_sound = pygame.mixer.Sound("data\\sounds\\ask.wav")
        self.hit_sound = pygame.mixer.Sound("data\\sounds\\hit.wav")
        self.kitties = kitties
        self.states = []
        self.kitties_near = []
        self.kitties_del = kitties_del
        self.dogs = dogs
        self.hit_n = 5
        self.hit_state = 5
        super().__init__(pos, self.states, "cat", 5, level_size_p)
        self.kitties_detectable = 0.25 * self.mapdiag
        self.hit_dist = 75
    
    def attack():
        pass
    
    def act(self):#keys: 
        keys = pygame.key.get_pressed()
        vx = 0
        vy = 0
        if keys[pygame.K_UP]:
            vy -= 1
        if keys[pygame.K_RIGHT]:
            vx += 1
        if keys[pygame.K_DOWN]:
            vy += 1
        if keys[pygame.K_LEFT]:
            vx -= 1
        super().move_to(vx, vy)
    
    def speedy(self):
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.speed = 25
        else:
            self.speed = 5
    
    def meow(self):
        if not self.sound_channel.get_busy():
            self.sound_channel.play(self.meow_sound)
            self.kitties_near.clear()
            for kitty in self.kitties:
                dist = self.distance(kitty.center)
                if dist[2] < self.kitties_detectable:
                    k = 1 - dist[2] / self.kitties_detectable
                    self.kitties_near.append([kitty, 0])
                    kitty.meow(k)
    
    def ask(self):
        for kitty in self.kitties:
            dist = self.distance(kitty.center)
            if dist[2] < kitty.ask_dist:
                if kitty.is_follow and kitty.master == self:
                    if kitty.is_in_safe():
                        self.kitties_del += [kitty]
                        kitty.go_home()
                    else:
                        kitty.stay()
                else:
                    kitty.follow_sound.set_volume(1 - dist[2] / self.kitties_detectable)
                    kitty.follow(self)

    def ask_meow(self):
        if not self.sound_channel.get_busy():
            self.sound_channel.play(self.ask_sound)
            self.ask()

    def hit(self):
        if not self.sound_channel.get_busy():
            self.hit_state = 0
            self.sound_channel.play(self.hit_sound)
            for dog in self.dogs:
                dist = self.distance(dog.center)
                if dist[2] < self.hit_dist:
                    dog.on_hit()
