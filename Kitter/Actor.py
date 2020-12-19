import pygame
import PhysObject
import GameObject
import math
from random import randint

class Actor(PhysObject.PhysObject):    
    def __init__(self, pos, states, name, speed, level_size_p):
        self.name = ""
        self.vx = 0
        self.vy = 0
        self.moves = []
        self.speed = 0
        self.name = name
        self.is_goal = False
        self.is_follow = False
        self.goal_pos = None
        self.safedist = 50
        self.followdist = 150
        temp = []
        temp.append(pygame.image.load("data\\sprites\\" + name + "\\stay_0.png"))
        #temp.append(pygame.image.load("data\\sprites\\" + name + "\\stay_1.png"))
        self.moves.append(PhysObject.State(temp[:], self.staying))#0, stay
        temp.clear()
        temp.append(pygame.image.load("data\\sprites\\" + name + "\\move_up_0.png"))
        temp.append(pygame.image.load("data\\sprites\\" + name + "\\move_up_1.png"))
        self.moves.append(PhysObject.State(temp[:], self.moving))#1, move up
        temp.clear()
        temp.append(pygame.image.load("data\\sprites\\" + name + "\\move_right_0.png"))
        temp.append(pygame.image.load("data\\sprites\\" + name + "\\move_right_1.png"))
        self.moves.append(PhysObject.State(temp[:], self.moving))#2, move right
        temp.clear()
        temp.append(pygame.image.load("data\\sprites\\" + name + "\\move_down_0.png"))
        temp.append(pygame.image.load("data\\sprites\\" + name + "\\move_down_1.png"))
        self.moves.append(PhysObject.State(temp[:], self.moving))#3, move down
        temp.clear()
        temp.append(pygame.image.load("data\\sprites\\" + name + "\\move_left_0.png"))
        temp.append(pygame.image.load("data\\sprites\\" + name + "\\move_left_1.png"))
        self.moves.append(PhysObject.State(temp[:], self.moving))#4, move left
        super().__init__(pos, self.moves[0].texture[0].get_size(), level_size_p)
        super().set_states(self.moves + states)
        self.speed = speed
        self.on_stop_follow = lambda: None
        self.on_staying = lambda: None
        self.on_moving = lambda: None
        self.on_stop_moving = lambda: None

    def ass(self):
        pass

    def set_on_stop_follow(self, act):
        self.on_stop_follow = act
    
    def set_on_stop_moving(self, act):
        self.on_stop_moving = act

    def set_on_staying(self, act):
        self.on_staying = act

    def set_on_moving(self, act):
        self.on_moving = act
    
    def staying(self):
        if self.is_follow and self.distance(self.goal_pos())[2] > self.safedist:
            self.move_in_pos(self.goal_pos, True)
        else:
            self.on_staying()

    def moving(self):
        if self.is_goal:
            dist = self.distance(self.goal_pos())
            if self.is_follow and dist[2] > self.followdist and self.followdist != 0:
                self.stay()
                self.on_stop_follow()
                self.on_stop_moving()
            else:
                if dist[2] <= self.safedist:
                    self.state = 0
                    self.is_goal = False
                    self.on_stop_moving()
                elif dist[2] < self.speed:
                    self.move_to(dist[0], dist[1])
                    self.vx = dist[0]
                    self.vy = dist[1]
                    self.move(self.vx, self.vy)
                    self.on_moving()
                else:
                    self.move_to(dist[0], dist[1])
                    self.move(self.speed * dist[0] / dist[2], self.speed * dist[1] / dist[2])
                    self.on_moving()
        else:
            self.move(self.vx, self.vy)
            self.on_moving()

    def move_to(self, vx, vy):
        #check rotation
        if vx == 0 and vy == 0:
            self.state = 0
        else:
            if abs(vx) >= abs(vy):
                if vx > 0:
                    self.state = 2
                else:
                    self.state = 4
            elif vy > 0:
                self.state = 3
            else:
               self.state = 1
            speed_in = math.sqrt(vx * vx + vy * vy)
            self.vx = vx * self.speed / speed_in
            self.vy = vy * self.speed / speed_in

    def move_in_pos(self, pos, is_follow):
        self.is_goal = True
        self.is_follow = is_follow
        self.goal_pos = pos
        self.move_to(self.goal_pos()[0] - self.left, self.goal_pos()[1] - self.top)
    
    def stay(self):
        self.state = 0
        self.is_goal = 0
        self.is_follow = 0
        self.vx = 0
        self.vy = 0
        self.on_stop_follow()
        self.on_stop_moving()

    def move_random(self):
        pos = (randint(self.width / 2 + 1, self.level_size_p[0] - self.width / 2 - 2), randint(self.height / 2 + 1, self.level_size_p[1] - self.height / 2 - 2))
        self.move_in_pos(lambda: pos, False)

