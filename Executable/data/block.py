import pygame
import random
from data import vector
from data import settings
from data import functions

blockImages = functions.getImages(functions.scale(pygame.image.load("data/assets/christmasGameTiles_lowRes.png"),settings.TILESIZE/4),4*settings.TILESIZE/4)
blockRepeatedTiles = [functions.getRepeatedTiles(blockImage, settings.DEPTH, []) for blockImage in blockImages]



class Block():
    def __init__(self, type):
        # self.pos = pos
        self.type = type
        # self.health = 2**self.type
        # self.color = (self.type/settings.NUMOFTYPES*255, 130, self.type/settings.NUMOFTYPES*255)
        # self.rect = pygame.Rect(self.pos.x, self.pos.y, settings.TILESIZE, settings.TILESIZE)

    def updateType(self, type):
        self.type = type
        # self.health = 2**self.type

    def drawRel(self, pos, screen):
        if self.type != 0:
            screen.blit(blockImages[self.type-1], pos.position)
            # pygame.draw.rect(screen, self.color, pygame.Rect(pos.x, pos.y, settings.TILESIZE, settings.TILESIZE))


    # def draw(self, screen):
    #     if self.type != 0:
    #         pygame.draw.rect(screen, self.color, self.rect)
        # pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.pos.x+settings.TILESIZE/4, self.pos.y+settings.TILESIZE/4, settings.TILESIZE*3/5, settings.TILESIZE*3/5))

class BlockGroup():
    def __init__(self, type, size):
        # self.pos = pos
        self.type = type
        self.size = size
        self.depth = functions.fastLog2(size/settings.TILESIZE)
        # self.color = (self.type/settings.NUMOFTYPES*255, 130, self.type/settings.NUMOFTYPES*255)
        # self.texture = None
        # self.rect = pygame.Rect(self.pos.x, self.pos.y, size, size)

    def updateType(self, type):
        self.type = type
        self.color = (self.type / settings.NUMOFTYPES * 255, 130, self.type / settings.NUMOFTYPES * 255)

    def drawRel(self, pos, screen):
        if self.type != 0:
            # pygame.draw.rect(screen, self.color, pygame.Rect(pos.x, pos.y, self.size, self.size))
            screen.blit(blockRepeatedTiles[self.type-1][self.depth], pos.position)

        # pygame.draw.rect(screen, (255,0,0), pygame.Rect(pos.x+self.size/5, pos.y+self.size/5, self.size*3/5, self.size*3/5))

    def draw(self, screen):
        if self.type != 0:
            pygame.draw.rect(screen, self.color, self.rect)
        # pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.pos.x+self.size/5, self.pos.y+self.size/5, self.size*3/5, self.size*3/5))