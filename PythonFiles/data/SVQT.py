import random

import pygame
from data import vector
from data import settings
from data import block

from data import Particles
from data import functions
from data import SFX
MAXDEPTH = settings.DEPTH
print("Here", MAXDEPTH)
TILESIZE = settings.TILESIZE
Vec2 = vector.Vec2

particles = Particles.particleContainer



numOfNodes = 0
class Node:
    def __init__(self, pos, depth, parent, globalPos, subdivide):
        self.localPos = pos
        self.globalPos = globalPos
        self.depth = depth
        self.size = 0.5**self.depth*settings.EldestNodeSize
        self.item = None

        if subdivide:
            self.isleaf = depth>=MAXDEPTH

        else:
            self.isleaf = True
            # self.item = self.getBlockGroup()

        if self.depth < settings.LOADCHUNKSPEED:
            self.loaded = False

        self.parent = parent
        self.updated = True
        self.type = -1
        self.children = self.get_children()

        if self.depth<settings.HAVESURFACEDEPTH:
            self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            # self.updateSurface()
        # else:
        #     self.surface = None

    def getChildrenNumber(self):
        global numOfNodes
        numOfNodes = 0
        self.BFS(Vec2((0,0)))

        return numOfNodes

    def findNode(self, prevPos, findpos):
        if self.isleaf:
            return self
        else: # recursively finds next block to binary search
            if findpos.x > prevPos.x+self.size / 2 *0.5:
                if findpos.y > prevPos.y+self.size / 2*0.5:
                    return self.children[3].findNode(prevPos + (Vec2((1,1)) * self.size / 2*0.5), findpos)

                else:
                    return self.children[2].findNode(prevPos + (Vec2((1, 0)) * self.size / 2*0.5), findpos)

            else:
                if findpos.y > prevPos.y+self.size / 2*0.5:
                    return self.children[1].findNode(prevPos + (Vec2((0, 1)) * self.size / 2*0.5), findpos)
                else:
                    return self.children[0].findNode(prevPos + (Vec2((0, 0)) * self.size / 2*0.5), findpos)


    def findNode2(self, prevPos, findpos):
        if self.isleaf:
            return self, prevPos+self.globalPos, self.size

        else:
            if findpos.x > prevPos.x+self.size / 2 *0.5:
                if findpos.y > prevPos.y+self.size / 2*0.5:

                    return self.children[3].findNode2(prevPos + (Vec2((1,1)) * self.size / 2*0.5), findpos)

                else:
                    return self.children[2].findNode2(prevPos + (Vec2((1, 0)) * self.size / 2*0.5), findpos)

            else:
                if findpos.y > prevPos.y+self.size / 2*0.5:
                    return self.children[1].findNode2(prevPos + (Vec2((0, 1)) * self.size / 2*0.5), findpos)
                else:
                    return self.children[0].findNode2(prevPos + (Vec2((0, 0)) * self.size / 2*0.5), findpos)

    def findEncompassingNode(self, prevPos, findPos, Dist):
        if self.isleaf or Dist*8>=self.size*0.5:
            return self

        else:
            if findPos.x > prevPos.x + self.size / 4:
                if findPos.y > prevPos.y + self.size / 4:
                    return self.children[3].findEncompassingNode(prevPos + (Vec2((1, 1)) * self.size / 4), findPos, Dist)
                else:
                    return self.children[2].findEncompassingNode(prevPos + (Vec2((1, 0)) * self.size / 4), findPos, Dist)

            else:
                if findPos.y > prevPos.y + self.size / 4:
                    return self.children[1].findEncompassingNode(prevPos + (Vec2((0, 1)) * self.size / 4), findPos, Dist)
                else:
                    return self.children[0].findEncompassingNode(prevPos + (Vec2((0, 0)) * self.size / 4), findPos, Dist)
    def BFS(self, parentPos):
        global numOfNodes
        if not self.isleaf:
            for child in self.children:
                child.BFS(parentPos+(self.localPos*self.size/2))


        else:
            numOfNodes += 1

    def update_items(self, parentPos):
        if not self.isleaf and self.updated:
            tempcounter = 0
            for child in self.children:
                tempcounter += 1
                child.update_items(parentPos + (self.localPos * self.size / 2))

            prevItem = -1
            counter = 0
            for child in self.children:
                if child.type != -1:  # if the chlid item is a valid block type
                    if child.type == prevItem:
                        counter += 1

                    else:
                        counter = 0
                        prevItem = child.type

                else:  # the child item is not a valid block type
                    self.type = -1
                    return 0

            if counter >= 3:
                self.type = self.children[0].item.type
                self.children = None
                self.isleaf = True
                self.size = self.size*2
                # self.item = block.Block(Vec2((0,0)), self.type)
                self.item = block.BlockGroup(self.type, self.size/4)



            else:
                self.type = -1  # the items are all different

    def update_isUpdated(self):
        if self.depth < settings.HAVESURFACEDEPTH:
            if self.updated==True:
                return 0

            self.updated = True

        if self.parent != None:
            self.parent.update_isUpdated()

    def updateSurfaces(self):
        if self.depth >= settings.HAVESURFACEDEPTH:
            surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.draw(surface, Vec2((0,0)))
            return surface

        if self.isleaf:
            if self.updated:
                self.surface.fill((0,0,0,0))
                self.item.drawRel(Vec2((0,0)),self.surface)
                self.updated = False

            return self.surface

        if self.updated:
            self.surface.fill((0,0,0,0))
            for child in self.children:


                if child.isleaf and child.depth < settings.HAVESURFACEDEPTH:
                    surf = child.updateSurfaces()
                    self.surface.blit(surf, (self.localPos * self.size/2+child.localPos*self.size/4).position)

                else:
                    self.surface.blit(child.updateSurfaces(), (self.localPos * self.size/2).position)



            self.updated = False

        return self.surface

    def updateSurface(self):
        self.surface.fill((0,0,0,0))
        self.draw(self.surface, Vec2((0,0)))

    def init_items(self, parentPos):
        if not self.isleaf:
            for child in self.children:
                child.init_items(parentPos+(self.localPos*self.size/2))




            prevItem = -1
            counter = 0
            for child in self.children:
                if child.type != -1: #if the chlid item is a valid block type
                    if child.type == prevItem:
                        counter += 1

                    else:
                        prevItem = child.type

                else: #the child item is not a valid block type
                    self.type = -1
                    return 0

            if counter >= 3:
                self.type = self.children[0].item.type
                self.children = None
                self.isleaf = True
                self.size = self.size * 2
                # self.item = block.Block(Vec2((0,0)), self.type)
                self.item = block.BlockGroup(self.type, self.size/4)



            else:
                self.type = -1  # the items are all different



        else:
            self.item = self.getItem(parentPos+(self.localPos*self.size/2))



    def draw(self, screen, parentPos):

        if not self.isleaf:
            for child in self.children:
                child.draw(screen, parentPos+(self.localPos*self.size/2))

        else:
            # self.item.draw(screen)


            if self.size/2 > settings.TILESIZE:
                # self.item.draw(screen)
                self.item.drawRel(parentPos+(self.localPos*self.size/4), screen)


            else:
                self.item.drawRel(parentPos + (self.localPos * self.size / 2), screen)
            # print(self.depth, self.size, (parentPos+(self.localPos*self.size/2)).position)

    def testDraw(self, screen, parentPos, mousePos):
        if not self.isleaf:
            trueSize = self.size*0.5
            offsetPos = Vec2(((mousePos.x>(parentPos.x+trueSize))*trueSize, (mousePos.y>(parentPos.y+trueSize))*trueSize))

            for child in self.children:
                if (parentPos+offsetPos + (self.localPos * self.size / 2)-mousePos).mag < 200 or self.depth < 3:
                    child.testDraw(screen, parentPos+(self.localPos*self.size/2), mousePos)
        else:
            self.item.draw(screen)

            # print(self.depth, self.size, (parentPos+(self.localPos*self.size/2)).position)

    def paint(self, parentPos, mousePos, radius, type, blocksAvailable):


        if not self.isleaf:
            squarePos = parentPos + (self.localPos * self.size / 2)
            dist = functions.distance_point_to_square(mousePos, squarePos, self.size)

            for child in self.children:
                if dist < radius:
                    child.paint(squarePos, mousePos, radius, type, blocksAvailable)

        else:
            if self.size/4>=settings.TILESIZE:
                self.divideNode()
                self.paint(parentPos, mousePos, radius, type, blocksAvailable)

            else: #its a single node
                if self.type != type and (type==0 or blocksAvailable.numOfItems > 0):
                    # self.item.health -= 1
                    #
                    # if self.item.health <= 0:
                    if self.type != 0:
                        particles.add_particle(Particles.BlockDestroyParticle(self.globalPos + parentPos, self.type))
                        if self.type <= 2:
                            SFX.dirtBreakSFX.playSimple(-1)
                        elif self.type == 3:
                            SFX.stoneBreakSFX.playSimple(-1)
                        elif self.type == 4:
                            SFX.ironBreakSFX.playSimple(-1)
                        elif self.type == 5:
                            SFX.diamondBreakSFX.playSimple(-1)


                    if type != 0:
                        blocksAvailable.numOfItems -= 0.25
                        if type <= 2:
                            SFX.dirtBreakSFX.playSimple(-1)
                        elif type == 3:
                            SFX.stoneBreakSFX.playSimple(-1)
                        elif type == 4:
                            SFX.ironBreakSFX.playSimple(-1)
                        elif type == 5:
                            SFX.diamondBreakSFX.playSimple(-1)


                    self.type = type
                    # print(self.type)
                    self.item.updateType(type)
                    self.update_isUpdated()




    def get_children(self):
        if not self.isleaf:
            childdepth = self.depth+1
            return (Node(Vec2((False,False)),childdepth, self, self.globalPos, True),Node(Vec2((False,True)),childdepth, self, self.globalPos, True),Node(Vec2((True,False)),childdepth, self, self.globalPos, True),Node(Vec2((True,True)),childdepth, self, self.globalPos, True))
        else:
            return None

    def divideNode(self):

        self.item = None
        self.isleaf = False
        self.size /= 2
        # self.update_isUpdated()

        childdepth = self.depth+1
        self.children = (Node(Vec2((False, False)), childdepth, self, self.globalPos, False),
                         Node(Vec2((False, True)), childdepth, self, self.globalPos, False),
                         Node(Vec2((True, False)), childdepth, self, self.globalPos, False),
                         Node(Vec2((True, True)), childdepth, self, self.globalPos, False))

        for child in self.children:
            # child.size*=2
            child.size = self.size
            child.type = self.type


        if self.size/8 <= settings.TILESIZE:
            for child in self.children:
                child.item = block.Block(self.type)

        else:
            for child in self.children:
                child.item = child.getBlockGroup(self.type)

        self.update_isUpdated()




    def getItem(self,pos):
        position = pos + self.globalPos

        # print(position.y, math.sin(position.x/1000)*100-300)
        # math.sin(position.x / 100) * 100 + 300
        if position.y < functions.terrain[int(position.x)] * 100 + 300+500:
            self.type = 0
        else:



            if position.y < functions.terrain[int(position.x)] * 100 + 500 +500+ random.randint(-3,3):
                if position.y < functions.terrain[int(position.x)] * 100 + 350 +500+ random.randint(-3,3):
                    self.type = 1
                else:
                    self.type = 2

            else:
                caveNoise = functions.caveNoiseArray[int((self.globalPos.x// settings.EldestNodeSize) % settings.NUMOFNOISEMAPS)]
                if int(functions.clamp(0,10,(caveNoise[int((position.x)%(settings.NOISESIZE))][int((position.y)%(settings.NOISESIZE))]+1.2))) > 0: #cave generation
                    ironNoise = functions.ironNoiseArray[int(((self.globalPos.x * 23 + 11 * self.globalPos.y + 1231) // settings.EldestNodeSize) % (settings.NUMOFNOISEMAPS * 2))]
                    ironNoiseSize = settings.NOISESIZE / 4
                    if int(functions.clamp(0, 10, (ironNoise[int(position.x % ironNoiseSize)][ int(position.y % ironNoiseSize)] + 1.4))) > 0:  # cave generation
                        diamondNoise = functions.diamondNoiseArray[int(((self.globalPos.x * 33 + 28 * self.globalPos.y + 1231) // settings.EldestNodeSize) % (settings.NUMOFNOISEMAPS * 2))]
                        if int(functions.clamp(0, 10, (diamondNoise[int(position.x % ironNoiseSize)][int(position.y % ironNoiseSize)] + 1.7))) > 0 or position.y < 1000+500:  # cave generation
                            self.type = 3
                        else:
                            self.type = 5



                    else:
                        self.type = 4
                else:

                    self.type = 0
            # self.type = random.randint(10,10)
        # self.type = position.y%10
        return block.Block(self.type)

    def getBlockGroup(self, type):
        return block.BlockGroup(type, self.size/2)






