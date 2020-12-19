import sys, pygame, time, Cat, Level, Camera, Kitty, Dog
from collections import defaultdict

class Kitter:
    def __init__(self, level_size, kitties, dogs):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mixer.music.load("data\\sounds\\rain.wav")
        pygame.mixer.music.play(-1)
        self.level_size = level_size
        self.kitties_n = kitties
        self.dogs_n = dogs
        self.fps = 20
        self.size = (640, 480)
        self.screen = pygame.display.set_mode(self.size)
        self.loading_screen = pygame.Surface(self.size)
        self.loading_screen.fill((0,0,0))
        self.screen.blit(self.loading_screen, (0,0))
        self.screen.blit(pygame.font.SysFont("comicsansms", 20).render("Loading", False, (255,255,255)), (self.size[0] / 2, self.size[1] / 2))
        pygame.display.flip()
        self.level = Level.Level(self.level_size)
        self.level_size_p = self.level.level_size_p

        self.kitties = []
        self.kitties_del = []
        self.dogs = []

        self.cat = Cat.Cat(self.level.safespace.center, self.level_size_p, self.kitties, self.kitties_del, self.dogs)

        for i in range(self.dogs_n):
            self.dogs.append(Dog.Dog(self.level_size_p, self.kitties, self.cat))

        for i in range(self.kitties_n):
            self.kitties.append(Kitty.Kitty(self.level_size_p, self.level.safespace, self.cat))

        self.pause = False

        self.draws = [self.level.safespace] + self.dogs + self.kitties
        self.updates = [self.cat] + self.kitties + self.dogs

        self.camera = Camera.Camera(((self.level.level_size_p[0] - self.size[0]) / 2 - 1, self.level.level_size_p[1] - self.size[1] - 1), self.size, self.level, self.cat, self.kitties, self.draws, self.screen, self.level_size_p)

        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)

        self.keydown_handlers[pygame.K_UP].append(self.cat.act)
        self.keydown_handlers[pygame.K_RIGHT].append(self.cat.act)
        self.keydown_handlers[pygame.K_DOWN].append(self.cat.act)
        self.keydown_handlers[pygame.K_LEFT].append(self.cat.act)
        self.keydown_handlers[pygame.K_F1].append(self.camera.about_switch)
        self.keydown_handlers[pygame.K_c].append(self.cat.meow)
        self.keydown_handlers[pygame.K_x].append(self.cat.ask_meow)
        self.keydown_handlers[pygame.K_z].append(self.cat.hit)
        self.keydown_handlers[pygame.K_LSHIFT].append(self.cat.speedy)
        self.keyup_handlers[pygame.K_UP].append(self.cat.act)
        self.keyup_handlers[pygame.K_RIGHT].append(self.cat.act)
        self.keyup_handlers[pygame.K_DOWN].append(self.cat.act)
        self.keyup_handlers[pygame.K_LEFT].append(self.cat.act)
        self.keyup_handlers[pygame.K_LSHIFT].append(self.cat.act)
        self.keyup_handlers[pygame.K_F1].append(self.camera.about_switch)
        self.keyup_handlers[pygame.K_LSHIFT].append(self.cat.speedy)

        while len(self.kitties):
            self.start = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == pygame.KEYDOWN:
                    for handler in self.keydown_handlers[event.key]:
                        handler()
                elif event.type == pygame.KEYUP:
                    for handler in self.keyup_handlers[event.key]:
                        handler()
            for i in self.updates:
                i.update()
            if len(self.kitties_del):
                for i in self.kitties_del:
                    if not i.state:
                        self.kitties_del.remove(i)
                        self.kitties.remove(i)
                        self.draws.remove(i)
                        self.updates.remove(i)
            self.camera.draw()
            pygame.display.flip()
            self.end = time.time()
            self.diff = self.end - self.start
            self.delay = 1.0 / self.fps - self.diff
            if self.delay > 0:
                    time.sleep(self.delay)
        self.screen.blit(pygame.font.SysFont("comicsansms", 20).render("You win! Restarting…", False, (255,255,255)), (self.size[0] / 3, self.size[1] / 3))
        pygame.display.flip()
        time.sleep(5)

if __name__ == '__main__':
    while True:
        game = Kitter((25, 15), 5, 3)
