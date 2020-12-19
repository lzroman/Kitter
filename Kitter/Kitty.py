import pygame
import Actor
from random import choice, randint

class Kitty(Actor.Actor):
    def __init__(self, level_size_p, safespace, cat):
        self.meow_sound = pygame.mixer.Sound("data\\sounds\\kitty.wav")
        self.follow_sound = pygame.mixer.Sound("data\\sounds\\follow.wav")
        self.lost_sound = pygame.mixer.Sound("data\\sounds\\lost.wav")
        self.meow_home = pygame.mixer.Sound("data\\sounds\\home.wav")
        self.cat = cat
        self.ask_dist = 50
        self.can_follow = True
        self.states = []
        self.type = choice(["black", "gray", "red", "white"])
        self.safespace = safespace
        self.master = None
        self.staytime = 0
        self.staytime_max = randint(500, 1000)
        super().__init__((0, 0), self.states, "kitty_" + self.type, 3, level_size_p)
        self.setpos((randint(0, level_size_p[0] - self.width - 1), randint(0, level_size_p[1] - self.height - 1)))
        self.set_on_stop_follow(self.stop_follow)
        self.set_on_staying(self.staying_act)
    
    def stop_follow(self):
        if self.master == self.cat:
            self.lost_sound.play()
        self.is_follow = False
        self.staytime = 0
        self.staytime_max = randint(500, 1000)

    def staying_act(self):
        self.staytime += 1
        if self.staytime >= self.staytime_max:
            self.move_random()
            self.staytime = 0
            self.staytime_max = randint(500, 1000)
    
    def meow(self, vol):
        self.meow_sound.set_volume(vol)
        self.meow_sound.play()
    
    def follow(self, master):
        if self.can_follow:
            if not self.is_follow:
                if master == self.cat:
                    self.master = master
                    self.move_in_pos((lambda: (self.master.centerx, self.master.centery)), True)
                    self.follow_sound.play()
                else:
                    self.master = master
                    self.move_in_pos((lambda: (self.master.centerx, self.master.centery)), True)
            elif self.master != master:
                if master == self.cat:
                    self.master = master
                    self.move_in_pos((lambda: (self.master.centerx, self.master.centery)), True)
                    self.follow_sound.play()
                else:
                    self.master = master
                    self.move_in_pos((lambda: (self.master.centerx, self.master.centery)), True)
            else:
                self.is_in_safe()
                self.is_follow = not self.is_follow

    def is_in_safe(self):
        if (self.left <= self.safespace.right and self.right >= self.safespace.left) and (self.bottom >= self.safespace.top and self.top <= self.safespace.bottom):
            return True
        else:
            return False

    def go_home(self):
        self.ignore_bounds = True
        self.meow_home.play()
        self.move_in_pos(lambda: (self.safespace.centerx, self.level_size_p[1] + 2 * self.height), False)
        self.can_follow = False
