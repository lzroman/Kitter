import PhysObject, pygame
import Actor
from random import choice, randint

class Dog(Actor.Actor):
    def __init__(self, level_size_p, kitties, cat):
        self.is_searching = True
        self.is_escaping = False
        self.is_followed = False
        self.is_moving_to_kitty = False
        self.search_distance = 500
        self.escaping_distance = 500
        self.states = []
        self.kitties = kitties
        self.cat = cat
        self.ignoring_state = 0
        self.ignoring_max = 0
        self.staying_state = 0
        self.staying_max = 50
        self.escape_sound = pygame.mixer.Sound("data\\sounds\\dog_escape.wav")
        self.kitty_to_follow = None
        self.nearest_kitty = None
        self.dist_min = 0
        self.found = False

        super().__init__((0, 0), self.states, "dog", 5, level_size_p)
        super().setpos((randint(0, level_size_p[0] - self.width), randint(0, level_size_p[1] - self.height)))

        self.set_on_moving(self.on_moving_act)
        self.set_on_stop_moving(self.on_stop_moving_act)
        self.set_on_staying(self.on_staying_act)

    def on_moving_act(self):
        if self.is_escaping:
            if self.distance(self.cat.center)[2] > self.escaping_distance:
                self.stay()
        else:
            if self.is_searching:
                if self.ignoring_state < self.ignoring_max:
                    self.ignoring_state += 1
                else:
                    if not self.is_followed:
                        self.dist_min = self.distance(self.kitties[0].center)[2]
                        self.found = False
                        self.nearest_kitty = self.kitties[0]
                        for kitty in self.kitties:
                            dist = self.distance(kitty.center)[2]
                            if dist < self.search_distance:
                                self.found = True
                                if dist < self.dist_min:
                                    self.dist_min = dist
                                    self.nearest_kitty = kitty
                        if self.found:
                            self.is_searching = False
                            self.is_followed = True
                            self.is_moving_to_kitty = True
                            self.kitty_to_follow = self.nearest_kitty
                            self.move_in_pos(lambda: self.kitty_to_follow.center, False)
            else:
                if self.kitty_to_follow == None:
                    self.is_followed = False
                    self.is_searching = True
                    self.is_moving_to_kitty = False
                    self.speed = 5
                    self.generate_staying()
                    self.generate_ignoring()
                    self.move_random()
                if not self.kitty_to_follow.can_follow:           
                    self.is_moving_to_kitty = False
                    self.is_followed = False
                    self.is_searching = True
                    self.speed = 5
                    self.generate_staying()
                    self.generate_ignoring()
                    self.move_random()
        
    def on_staying_act(self):
        if self.is_escaping:
                self.move_random()
        else:
            if self.staying_state < self.staying_max:
                self.staying_state += 1
                self.ignoring_state += 1
            else:
                self.move_random()

    def on_stop_moving_act(self):
        if self.is_escaping:
            if self.distance(self.cat.center)[2] < self.escaping_distance:
                self.move_random()
            else:
                self.is_followed = False
                self.is_escaping = False
                self.is_searching = True
                self.speed = 5
                self.generate_staying()
                self.generate_ignoring()
        else:
            if self.is_moving_to_kitty:
                self.speed = self.kitties[0].speed
                self.kitty_to_follow.follow(self)
                self.is_moving_to_kitty = False
                self.move_random()
            elif self.is_followed:
                if self.kitty_to_follow != None:
                    if self.kitty_to_follow.master == self and self.kitty_to_follow.is_follow:
                        self.kitty_to_follow.stay()
                        self.is_followed = False
                        self.is_searching = True
                        self.speed = 5
                        self.generate_staying()
                        self.generate_ignoring()
                    else:
                        self.is_followed = False
                        self.is_searching = True
                        self.speed = 5
                        self.generate_staying()
                        self.generate_ignoring()
                else:
                        self.is_followed = False
                        self.is_searching = True
                        self.speed = 5
                        self.generate_staying()
                        self.generate_ignoring()
            else:
                self.generate_staying()

    def on_hit(self):
        self.speed = 10
        self.escape_sound.play()
        self.is_escaping = True
        self.is_searching = False
        self.is_moving_to_kitty = False
        self.move_random()
        if self.kitty_to_follow.master == self and self.kitty_to_follow.is_follow:
            self.kitty_to_follow.stay()

    def generate_staying(self):
        self.staying_state = 0
        self.staying_max = randint(10, 150)

    def generate_ignoring(self):
        self.ignoring_state = 0
        self.ignoring_max = randint(10, 300)
