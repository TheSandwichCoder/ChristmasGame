import random

import pygame
from data import vector
from data import block
from data import UI
from data import settings
from data import SFX
Vec2 = vector.Vec2

blockImages = block.blockImages
blockImageColors = [block.get_at((0,0)) for block in blockImages]



class ParticleContainer():
    def __init__(self):
        self.blockParticles = pygame.sprite.Group()
        self.textParticles = pygame.sprite.Group()

    def add_particle(self, particle):
        if particle.lifeSpan > 21:
            self.blockParticles.add(particle)
        else:
            self.textParticles.add(particle)

    def update(self, player):
        self.blockParticles.update(player.pos)
        self.textParticles.update()

    def draw(self, offset, screen):
        for particle in self.blockParticles:
            particle.draw(offset, screen)

        for particle in self.textParticles:
            particle.draw(offset, screen)

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, vec, lifespan):
        super().__init__()
        self.pos = pos
        self.vec = vec
        self.lifeSpan = lifespan
        self.lifeTime = 0
        self.image = None
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 10,10)

    def update(self):
        self.pos += self.vec

        if self.lifeTime >= self.lifeSpan:
            self.kill()
        self.lifeTime += 1

    def draw(self, offset, screen):
        screen.blit(self.image, (self.pos+offset).position)

class BlockDestroyParticle(Particle):
    def __init__(self, pos, type):
        super().__init__(pos, Vec2((0,0)), 1000)
        self.type = type
        self.divisionMultiplier = 1
        self.color = blockImageColors[self.type-1]

    def update(self, playerpos):
        if (self.pos-playerpos).mag < 20:
            UI.UI.Inventory.add(self.type)
            SFX.popSFX.playSimple(-1)
            self.kill()
            return 0

        toPlayerDist = (playerpos-self.pos)
        self.vec = toPlayerDist.normalise()*15 * (1+ 5/(toPlayerDist.mag))
        # self.divisionMultiplier += 0.02

        super().update()

    def draw(self, offset, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x+offset.x, self.pos.y+offset.y, settings.TILESIZE, settings.TILESIZE))

class TextParticle(Particle):
    def __init__(self, pos, text):
        super().__init__(pos+Vec2((random.randint(-3,3),random.randint(-3,3))), Vec2((random.randint(-2,2),-5)), 20)
        self.image = text
        self.image.convert_alpha()
    def update(self):
        self.image.set_alpha(255*(self.lifeSpan-self.lifeTime)/self.lifeSpan)
        super().update()

    def draw(self, offset, screen):
        super().draw(offset, screen)


particleContainer = ParticleContainer()





