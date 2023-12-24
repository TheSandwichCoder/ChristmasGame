# import pygame
from data import vector
from data import functions
Vec2 = vector.Vec2

class Background:
    def __init__(self, background):
        self.background = background
        self.backgroundSize = Vec2(background.get_size())
        self.segmentSize = Vec2((1280/2,720/2))
        self.segmentShape = Vec2((int(self.backgroundSize.x//self.segmentSize.x), int(self.backgroundSize.y//self.segmentSize.y)))
        self.segments = self.getSegments()
        self.length = len(self.segments)

    def getSegments(self):
        array = []

        for y in range(self.segmentShape.y):
            for x in range(self.segmentShape.x):
                array.append(functions.clip(self.background, x*self.segmentSize.x, y*self.segmentSize.y, self.segmentSize.x, self.segmentSize.y))

        return array

    def get1dPos(self, pos):
        return int(pos.y * self.segmentShape.x + pos.x)

    def draw(self, screen, pos):
        screenPos = -pos
        topLeftItem = Vec2((screenPos.x//self.segmentSize.x, screenPos.y//self.segmentSize.y))
        AnotherTopLeftVector = -(self.segmentSize-Vec2((pos.x%self.segmentSize.x, pos.y%self.segmentSize.y)))
        for y in range(3):
            for x in range(3):
                location = self.get1dPos(topLeftItem+Vec2((x,y)))
                if location < self.length:
                    drawPos = AnotherTopLeftVector+Vec2((x*self.segmentSize.x,y*self.segmentSize.y))
                    screen.blit(self.segments[location], drawPos.position)

