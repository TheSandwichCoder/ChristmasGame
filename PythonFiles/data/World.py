from data import settings
from data import SVQT
from data import vector
import pygame
Vec2 = vector.Vec2

class Chunk:
    def __init__(self, pos):
        self.pos = pos
        # self.blocks = SVQT.Node(Vec2((0,0)),0, None, self.pos, True)
        self.blocks = None
        self.loaded = False
        # self.blocks.init_items(Vec2((0,0)))

    def init_Blocks(self):
        self.blocks = SVQT.Node(Vec2((0,0)),0, None, self.pos, True)
        self.blocks.init_items(Vec2((0,0)))

    def getBlockNum(self):
        return self.blocks.getChildrenNumber()

    def findBlock(self, pos):
        return self.blocks.findNode(Vec2((0,0)), pos-self.pos)

    def findNode2(self, pos):
        return self.blocks.findNode2(Vec2((0, 0)), pos - self.pos)

    def updateAllBlocks(self):
        self.blocks.update_items(Vec2((0,0)))

    def updateSurfaces(self):
        self.blocks.updateSurfaces()

    def paint(self, offset, pos, radius, type, blocksAvailable):
        self.blocks.paint(Vec2((0,0)), pos-self.pos-offset, radius, type, blocksAvailable)

    def drawBlock(self, offset, pos):
        block = self.blocks.findNode(Vec2((0,0)), pos-self.pos-offset)

        if block.size/2 > settings.TILESIZE:
            block.divideNode()
            # block.update_isUpdated()
            # block.paint(parentPos, mousePos)

        # else:  # its a single node
        #     block.type = 3
        #     block.item.updateType(3)
        #     block.update_isUpdated()



    def draw(self,offset, screen):
        # print((self.pos+offset).position)
        screen.blit(self.blocks.surface, (self.pos+offset).position)

class ChunksHandler():
    def __init__(self, size):
        self.size = size
        self.offset = Vec2((0,0))
        self.chunks = self.initiateChunks()

    def initiateChunks(self):
        chunks = []
        for y in range(self.size.y):
            for x in range(self.size.x):
                chunks.append(Chunk(Vec2((x*settings.EldestNodeSize/2,y*settings.EldestNodeSize/2))))
                print(f"CHUNK {y*self.size.x+x} ")

        return chunks

    def get1dposition(self, pos):
        if pos.x < 0 or pos.y < 0:
            return -1

        return int(pos.y*self.size.x+pos.x)

    def get2dposition(self, num):
        return Vec2((num%self.size.x, num//self.size.x))

    def is_ChunkExists(self, pos):
        if pos.x < 0 or pos.y < 0:
            return False
        elif pos.x >= self.size.x or pos.y >= self.size.y:
            return False
        return True

    def getSurroundingChunks(self, pos1):
        pos = pos1-self.offset

        ENS = settings.EldestNodeSize/2
        mainChunk = Vec2(((pos.x // ENS), (pos.y // ENS)))
        array = []
        for x in range(-1,2):
            for y in range(-1,2):
                chunk = mainChunk+Vec2((x,y))
                if self.is_ChunkExists(chunk):
                    array.append(self.get1dposition(chunk))
        return array



    def getNearbyChunks(self, pos1):
        pos = pos1-self.offset

        ENS = settings.EldestNodeSize/2
        mainChunk = Vec2(((pos.x//ENS),(pos.y//ENS)))
        mainChunkMiddle = (mainChunk*ENS)+Vec2((ENS/2,ENS/2))
        mainArray = []

        # if self.is_ChunkExists(mainChunk):
        mainArray.append(self.get1dposition(mainChunk))

        if pos.x > mainChunkMiddle.x:
            if pos.y > mainChunkMiddle.y:
                evalPos = mainChunk+Vec2((1, 1))
                evalPos2 = mainChunk+Vec2((0,1))
                evalPos3 = mainChunk+Vec2((1,0))

                if self.is_ChunkExists(evalPos):
                    mainArray.append(self.get1dposition(evalPos))
                if self.is_ChunkExists(evalPos2):
                    mainArray.append(self.get1dposition(evalPos2))
                if self.is_ChunkExists(evalPos3):
                    mainArray.append(self.get1dposition(evalPos3))

            elif pos.y < mainChunkMiddle.y:
                evalPos = mainChunk + Vec2((1, -1))
                evalPos2 = mainChunk + Vec2((0, -1))
                evalPos3 = mainChunk + Vec2((1, 0))
                if self.is_ChunkExists(evalPos):
                    mainArray.append(self.get1dposition(evalPos))
                if self.is_ChunkExists(evalPos2):
                    mainArray.append(self.get1dposition(evalPos2))
                if self.is_ChunkExists(evalPos3):
                    mainArray.append(self.get1dposition(evalPos3))

        elif pos.x < mainChunkMiddle.x:
            if pos.y > mainChunkMiddle.y:
                evalPos = mainChunk + Vec2((-1, 1))
                evalPos2 = mainChunk + Vec2((-1, 0))
                evalPos3 = mainChunk + Vec2((0, 1))
                if self.is_ChunkExists(evalPos):
                    mainArray.append(self.get1dposition(evalPos))
                if self.is_ChunkExists(evalPos2):
                    mainArray.append(self.get1dposition(evalPos2))
                if self.is_ChunkExists(evalPos3):
                    mainArray.append(self.get1dposition(evalPos3))


            elif pos.y < mainChunkMiddle.y:
                evalPos = mainChunk + Vec2((-1, -1))
                evalPos2 = mainChunk + Vec2((-1, 0))
                evalPos3 = mainChunk + Vec2((0, -1))
                if self.is_ChunkExists(evalPos):
                    mainArray.append(self.get1dposition(evalPos))
                if self.is_ChunkExists(evalPos2):
                    mainArray.append(self.get1dposition(evalPos2))
                if self.is_ChunkExists(evalPos3):
                    mainArray.append(self.get1dposition(evalPos3))

        return mainArray

    def draw(self,pos,screen):
        array = self.getSurroundingChunks(pos+self.offset)

        for location in array:
            if location < len(self.chunks):
                chunk = self.chunks[location]
                if chunk.loaded:
                    chunk.draw(self.offset, screen)

        # for chunk in self.chunks:
        #     # print(chunk.pos.position)
        #     if chunk.loaded:
        #         chunk.draw(self.offset, screen)



    def updateAllBlocks(self):
        for chunk in self.chunks:
            if chunk.loaded:
                chunk.updateAllBlocks()

    def updateSurfaces(self):
        for chunk in self.chunks:
            if chunk.loaded:
                chunk.updateSurfaces()

    def paint(self, pos, radius, type, blocksAvailable):
        # for chunk in self.chunks:
        #     chunk.paint(self.offset, pos)
        array = self.getNearbyChunks(pos)



        for location in array:
            if location < len(self.chunks) and location>=0:
                self.chunks[location].paint(self.offset, pos, radius, type, blocksAvailable)

        # self.chunks[1].paint(self.offset, pos)

    def findBlock(self, pos):
        ENS = settings.EldestNodeSize/2
        loc = self.get1dposition(Vec2(((pos.x // ENS), (pos.y // ENS))))
        chunk = self.chunks[loc]

        return chunk.findBlock(pos-self.offset)

    def findNode2(self, pos):
        ENS = settings.EldestNodeSize / 2
        loc = self.get1dposition(Vec2((((pos.x) // ENS), ((pos.y) // ENS))))
        if loc < len(self.chunks) and loc > -1:
            chunk = self.chunks[loc]
            return chunk.findNode2(pos)
        return None



    def drawBlock(self, pos):
        for chunk in self.chunks:
            chunk.drawBlock(self.offset, pos)

    def getBlockNum(self):
        num = 0
        numLoaded = 0
        for chunk in self.chunks:
            if chunk.loaded:
                numLoaded += 1
                num+=chunk.getBlockNum()
        return num, numLoaded

    def loadChunks(self, player):
        chunks = self.getSurroundingChunks(player.pos+self.offset)

        for chunk in chunks:
            chunkObj = self.chunks[chunk]

            if chunkObj.loaded:
                continue
            else:
                chunkObj.init_Blocks()

                chunkObj.loaded = True

    def PC_y(self, player):



        pack1 = self.findNode2(player.pos+Vec2((player.size.x/2,player.size.y-1)))
        if pack1 != None:
            block_under = pack1[0]
            block_under_pos = pack1[1]
            if not block_under.type == 0:
                if player.pos.y+player.size.y > block_under_pos.y:
                    player.pos.update_y(block_under_pos.y-player.size.y)
                    player.grounded = True
                    player.vec.update_y(0)
                else:
                    player.grounded = False
                return 0

        pack2 = self.findNode2(player.pos+Vec2((player.size.x/2,-1)))

        if pack2 != None:
            block_above = pack2[0]
            block_above_pos = pack2[1]
            block_above_size = pack2[2]

            # block_above, block_above_pos, block_above_size = self.findBlock(player.pos+Vec2((player.size.x/2,-2)))


            if not block_above.type == 0:
                if player.pos.y < block_above_pos.y+block_above_size:
                    player.pos.update_y(block_above_pos.y + block_above_size)
                    player.vec.update_y(0)


    def PC_x(self, player):
        pack1 = self.findNode2(player.pos + Vec2((-1, self.size.y/2)))

        if pack1 != None:
            block_left = pack1[0]
            block_left_pos = pack1[1]
            block_left_size = pack1[2]
            if not block_left.type == 0:
                if player.pos.x < block_left_pos.x + block_left_size:
                    player.pos.update_x(block_left_pos.x + block_left_size / 4)
                    # player.grounded = True
                    player.vec.update_x(0)

        pack2 = self.findNode2(player.pos + Vec2((player.size.x+1, self.size.y/2)))
        if pack2 != None:
            block_right = pack2[0]
            block_right_pos = pack2[1]



            if not block_right.type == 0:
                if player.pos.x+player.size.x > block_right_pos.x:
                    player.pos.x = block_right_pos.x-player.size.x
                    # player.grounded = True
                    player.vec.update_x(0)









    def playerCollision(self, player):
        player.pos += player.vec

        if player.pos.y+player.size.y > settings.EldestNodeSize/2*settings.WorldSize[1]:
            player.pos.update_y(settings.EldestNodeSize/2*settings.WorldSize[1]-player.size.y)
            player.vec.update_y(0)
            player.grounded = True
        if player.pos.y < 0:
            player.pos.update_y(0)
            player.vec.update_y(0)

        if player.pos.x < 3:
            player.pos.update_x(3)
            player.vec.update_x(0)

        elif player.pos.x+player.size.x > settings.EldestNodeSize/2*settings.WorldSize[0]-3:
            player.pos.update_x(settings.EldestNodeSize * settings.WorldSize[0] - player.size.x-3)
            player.vec.update_x(0)

        # player.pos.y_increment(player.vec.y)
        self.PC_y(player)

        # player.pos.x_increment(player.vec.x)
        self.PC_x(player)

