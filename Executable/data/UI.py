from data import settings
from data import functions
from data import vector
from data import Interatables
import pygame

blockImages = functions.getImages(functions.scale(pygame.image.load("data/assets/christmasGameTiles.png"),4),4*4)
inventorySlot = pygame.image.load("data/assets/christmasGame_inventorySlotImage.png")
inventorySlotSelected = pygame.image.load("data/assets/christmasGame_inventorySlotImageSelected.png")
Vec2 = vector.Vec2


class itemStack:
    def __init__(self):
        self.type = -1
        self.numOfItems = 0
        self.full = False


    def add(self, type):
        if not self.full:
            if self.type == -1:
                self.type = type

            self.numOfItems += 0.25

            if self.numOfItems == settings.ITEMSTACKMAX:
                self.full = True

    def clear(self):
        self.full = False
        self.numOfItems = 0
        self.type = -1

    def draw(self,screen, pos, selected):
        if selected:
            screen.blit(inventorySlotSelected, (pos - Vec2((4.5, 4.5))).position)
        else:
            screen.blit(inventorySlot, (pos - Vec2((4.5, 4.5))).position)
        if self.type >= 0:

            screen.blit(blockImages[self.type-1], pos.position)
            screen.blit(settings.font.render(str(int(self.numOfItems)), 1, (0,0,0)), pos.position)

        #add the counter

class Inventory:
    def __init__(self):
        self.pos = Vec2((1040,30))
        self.button = Interatables.Button(self.pos+Vec2((200,0)), True, " ", 1)
        self.inventoryImage = pygame.image.load("data/assets/christmasGame_inventoryImage.png")
        self.crossImage = pygame.image.load("data/assets/christmasGame_crossImage.png")

        self.image = self.inventoryImage
        self.numOfSlots = 4
        self.InventorySlotButtonArray = []
        self.init_Buttons()
        self.stacks = [itemStack() for i in range(self.numOfSlots)]
        self.selectedStack = -1
        self.openned = False

    def update(self):
        self.button.update()
        if self.button.activated:
            self.openned = not self.openned

        for button in self.InventorySlotButtonArray:
            button.update()
            if button.activated:
                if button.id == self.selectedStack:
                    self.selectedStack = -1
                else:
                    self.selectedStack = button.id


        for stack in self.stacks:
            if stack.numOfItems <= 0:
                stack.clear()

    def init_Buttons(self):
        self.InventorySlotButtonArray.clear()
        self.InventorySlotButtonArray = [Interatables.Button(Vec2((self.pos.x + (i % 5) * 30, self.pos.y + (i // 5) * 30)),False, " ", i) for i in range(self.numOfSlots)]


    def add(self, type):
        for stack in self.stacks:
            if not stack.full and (stack.type == type or stack.type==-1):
                stack.add(type)
                return

    def addSlot(self):
        self.numOfSlots += 1
        self.stacks.append(itemStack())
        self.init_Buttons()

    def clear(self):
        for stack in self.stacks:
            stack.clear()

    def draw(self, screen):
        # print(self.openned)
        if self.openned:
            counter = 0
            self.image = self.crossImage
            for item in self.stacks:

                item.draw(screen, Vec2((self.pos.x+(counter%5)*30, self.pos.y+(counter//5)*30)), counter == self.selectedStack)
                counter += 1
        else:
            self.image = self.inventoryImage

        screen.blit(self.image, (self.pos+Vec2((200,0))).position)


class playerUI:
    def __init__(self):
        self.Inventory = Inventory()

    def draw(self, screen):
        self.Inventory.draw(screen)

    def update(self, player):
        self.Inventory.update()





UI = playerUI()



