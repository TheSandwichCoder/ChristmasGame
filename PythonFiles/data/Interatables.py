import pygame
from data import vector
Vec2 = vector.Vec2

pygame.font.init()

font = pygame.font.Font("data/assets/font/PixelifySans-VariableFont_wght.ttf",10)

ButtonFont = pygame.font.Font("data/assets/font/PixelifySans-VariableFont_wght.ttf",30)

buttonImage1 = pygame.transform.scale_by(pygame.image.load("data/assets/NNN_gameButtonUnpressed.png"),(15,15))
buttonImage2 = pygame.transform.scale_by(pygame.image.load("data/assets/NNN_gameButtonPressed.png"), (15,15))

class Button():
    def __init__(self, pos, invisible, text, id):
        self.pos = pos
        self.invisible = invisible
        self.size = Vec2((20,20))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.text = text
        self.unPressedImage = buttonImage1
        self.PressedImage = buttonImage2
        self.Image = self.unPressedImage
        self.textRendered = font.render(self.text,1,(0,0,0))
        self.textOffset = (self.size-Vec2(self.textRendered.get_size()))*0.5
        self.id = id
        self.activated = False
        self.gotActivatedTimer = 0

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.activated = False
        if self.rect.collidepoint(mousePos[0], mousePos[1]):
            # self.Image = self.PressedImage

            if pygame.mouse.get_pressed()[0]:

                if self.gotActivatedTimer <= 0:

                    self.activated = True
                self.gotActivatedTimer = 2

            else:
                self.gotActivatedTimer -= 1
        # else:
            # self.Image = self.unPressedImage

    def draw(self, screen):
        if not self.invisible:
            screen.blit(self.Image, self.pos.position)
            screen.blit(self.textRendered, (self.pos+self.textOffset).position)

class ButtonResizeable():
    def __init__(self, pos,size, invisible,clickOnce ,text, id):
        self.pos = pos
        self.invisible = invisible
        self.size = size
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.hovering = False
        self.text = text
        self.clickOnce = clickOnce
        self.unPressedImage = buttonImage1
        self.PressedImage = buttonImage2
        self.Image = self.unPressedImage
        self.textRendered = ButtonFont.render(self.text,1,(0,0,0))
        self.textOffset = (self.size-Vec2(self.textRendered.get_size()))*0.5
        self.id = id
        self.activated = False
        self.gotActivatedTimer = 0

    def update(self, offset):
        mousePos = (Vec2(pygame.mouse.get_pos())-offset).position
        self.activated = False
        self.hovering = False
        if self.rect.collidepoint(mousePos[0], mousePos[1]):
            self.Image = self.PressedImage

            self.hovering = True

            if pygame.mouse.get_pressed()[0]:

                if self.gotActivatedTimer <= 0:

                    self.activated = True
                if self.clickOnce:
                    self.gotActivatedTimer = 2

            else:
                self.gotActivatedTimer -= 1
        else:
            self.Image = self.unPressedImage

    def draw(self, screen):
        if not self.invisible:
            screen.blit(self.Image, self.pos.position)
            screen.blit(self.textRendered, (self.pos+self.textOffset).position)

class Slider:
    def __init__(self, pos, len, sliderPos, name):
        self.pos = pos
        self.sliderPos = sliderPos
        self.value = sliderPos*100
        self.len = len
        self.name = name
        self.name_rendered = ButtonFont.render(name, 1, (0, 0, 0))
        self.height = 40
        self.rect = pygame.Rect(self.pos.x, self.pos.y-self.height/2, self.len, self.height)


    def update(self):

        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos[0], mousePos[1]) and pygame.mouse.get_pressed()[0]:
            self.sliderPos = (mousePos[0]-self.pos.x) / self.len

        if self.sliderPos>0.97:
            self.sliderPos = 1
        self.textRendered = ButtonFont.render(str(int(self.value)), 1, (0, 0, 0))

    def draw(self, screen):
        pygame.draw.line(screen, (0,0,0), *(self.pos.position, (self.pos+Vec2((self.len,0))).position), 10)
        pygame.draw.circle(screen, (232, 32, 129), (self.pos+Vec2((self.len*self.sliderPos,0))).position,20)
        screen.blit(self.textRendered, (self.pos+Vec2((self.len+20,-self.textRendered.get_height()/2))).position)
        screen.blit(self.name_rendered, (self.pos+Vec2((-self.name_rendered.get_width(),-self.textRendered.get_height()/2))).position)

