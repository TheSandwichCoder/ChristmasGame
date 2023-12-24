import pygame
from data import vector
from data import functions
from data import Interatables
from data import Particles
from data import SFX
Vec2 = vector.Vec2

font = pygame.font.Font("data/assets/font/PixelifySans-VariableFont_wght.ttf",15)

costForType = [0,0.5,0.5,1,50,1000,0,0,0,0,0]

particles = Particles.particleContainer

class SantaShop:
    def __init__(self, pos):
        self.pos = pos

        self.image = functions.scale(pygame.image.load("data/assets/christmasGame_santaShed.png"),2)
        self.SellAllButton = Interatables.ButtonResizeable(self.pos+Vec2((30*2, 36*2)), Vec2((30*2,14*2)), True,False, " ", 0)
        self.SellAllButtonImage = functions.scale(pygame.image.load("data/assets/christmasGame_SellButton.png"),2)
        self.SellAllButtonImageSelected = functions.scale(pygame.image.load("data/assets/christmasGame_SellButtonSelected.png"),2)
        self.SellAllButtonImageUsed = self.SellAllButtonImage

        self.increaseRangeButton = Interatables.ButtonResizeable(self.pos+Vec2((23*2, 16*2)), Vec2((12*2,12*2)), True,True, " ", 1)
        self.increaseRangeButtonImage = functions.scale(pygame.image.load("data/assets/christmasGame_IncreaseRangeButton.png"),2)
        self.increaseRangeButtonImageSelected = functions.scale(pygame.image.load("data/assets/christmasGame_IncreaseRangeButtonSelected.png"),2)
        self.increaseRangeButtonUsed =self.increaseRangeButtonImage

        self.increaseAreaButton = Interatables.ButtonResizeable(self.pos+Vec2((58*2, 17*2)), Vec2((12*2,12*2)), True,True, " ", 2)
        self.increaseAreaButtonImage = functions.scale(pygame.image.load("data/assets/christmasGame_IncreaseAreaButton.png"),2)
        self.increaseAreaButtonImageSelected = functions.scale(pygame.image.load("data/assets/christmasGame_IncreaseAreaButtonSelected.png"),2)
        self.increaseAreaButtonUsed = self.increaseAreaButtonImage

        self.increaseInventoryButton = Interatables.ButtonResizeable(self.pos + Vec2((61 * 2, 7 * 2)), Vec2((16 * 2, 9 * 2)), True, True, " ", 3)
        self.increaseInventoryButtonImage = functions.scale(pygame.image.load("data/assets/christmasGame_IncreaseInventoryButton.png"), 2)
        self.increaseInventoryButtonImageSelected = functions.scale(pygame.image.load("data/assets/christmasGame_IncreaseInventoryButtonSelected.png"), 2)
        self.increaseInventoryButtonUsed = self.increaseInventoryButtonImage


        self.money = 0

    def update(self,player, offset):
        self.SellAllButton.update(offset)
        if self.SellAllButton.hovering:
            self.SellAllButtonImageUsed = self.SellAllButtonImageSelected
        else:
            self.SellAllButtonImageUsed = self.SellAllButtonImage

        self.increaseRangeButton.update(offset)
        if self.increaseRangeButton.hovering:
            self.increaseRangeButtonUsed = self.increaseRangeButtonImageSelected
        else:
            self.increaseRangeButtonUsed = self.increaseRangeButtonImage

        self.increaseAreaButton.update(offset)
        if self.increaseAreaButton.hovering:
            self.increaseAreaButtonUsed = self.increaseAreaButtonImageSelected
        else:
            self.increaseAreaButtonUsed = self.increaseAreaButtonImage

        self.increaseInventoryButton.update(offset)
        if self.increaseInventoryButton.hovering:
            self.increaseInventoryButtonUsed = self.increaseInventoryButtonImageSelected
        else:
            self.increaseInventoryButtonUsed = self.increaseInventoryButtonImage


        keys = pygame.key.get_pressed()
        sellAll = keys[pygame.K_LSHIFT]


        if self.SellAllButton.activated:
            inventory = player.UI.Inventory
            for stack in inventory.stacks:
                if stack.numOfItems > 0:
                    if not sellAll:
                        stack.numOfItems -= 1
                        moneyGained = costForType[stack.type]

                        self.money += moneyGained
                        particles.add_particle(Particles.TextParticle(player.pos-Vec2((player.size.x/2,0)), font.render(f"+${moneyGained}", 1, (131, 191, 52))))
                        break

                    else:
                        moneyGained = costForType[stack.type]*stack.numOfItems
                        self.money += moneyGained
                        stack.clear()
                        particles.add_particle(Particles.TextParticle(player.pos-Vec2((player.size.x/2,0)), font.render(f"+${moneyGained}", 1, (131, 191, 52))))
            SFX.moneySFX.playSimple(-1)




        if self.increaseRangeButton.activated:
            if self.money >= 2000:
                player.range += 10
                particles.add_particle(Particles.TextParticle(player.pos-Vec2((player.size.x/2,0)), font.render(f"+10R", 1, (131, 191, 52))))
                self.money -= 2000
                particles.add_particle(Particles.TextParticle(player.pos-Vec2((player.size.x/2,0)), font.render(f"-2000", 1, (237, 51, 111))))
                SFX.moneySFX.playSimple(-1)

        if self.increaseAreaButton.activated:
            if self.money >= 10000:
                player.radiusMax += 5
                player.radius = player.radiusMax
                particles.add_particle(Particles.TextParticle(player.pos-Vec2((player.size.x/2,0)), font.render(f"+5R", 1, (131, 191, 52))))
                self.money -= 10000
                particles.add_particle(Particles.TextParticle(player.pos-Vec2((player.size.x/2,0)), font.render(f"-10000", 1, (237, 51, 111))))
                SFX.moneySFX.playSimple(-1)

        if self.increaseInventoryButton.activated:
            if self.money >= 1000:
                player.UI.Inventory.addSlot()
                particles.add_particle(Particles.TextParticle(player.pos-Vec2((player.size.x/2,0)), font.render(f"+1 Inventory Slot", 1, (131, 191, 52))))
                self.money -= 1000
                particles.add_particle(Particles.TextParticle(player.pos-Vec2((player.size.x/2,0)), font.render(f"-1000", 1, (237, 51, 111))))
                SFX.moneySFX.playSimple(-1)











    def draw(self, offset, screen):
        screen.blit(self.image, (self.pos+offset).position)
        screen.blit(self.SellAllButtonImageUsed, (self.pos+Vec2((30*2, 36*2))+offset).position)
        screen.blit(self.increaseRangeButtonUsed, (self.pos+Vec2((23*2, 16*2))+offset).position)
        screen.blit(self.increaseAreaButtonUsed, (self.pos+Vec2((58*2, 17*2))+offset).position)
        screen.blit(self.increaseInventoryButtonUsed, (self.pos+Vec2((61*2, 7*2))+offset).position)

        text = font.render("$"+str(self.money),1,(131, 191, 52))
        screen.blit(text, (self.pos+Vec2((75*2, 47*2))-Vec2((text.get_width(),0))+offset).position)