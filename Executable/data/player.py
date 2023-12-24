import pygame
from data import functions
from data import vector
from data import UI

Vec2 = vector.Vec2

playerscale = 2
playersize = Vec2((10,20))*playerscale


animationFrames = functions.getImages(pygame.transform.scale(pygame.image.load("data/assets/christmasGame_player_runningAnimation.png"),(80*playerscale, 20*playerscale)),10*playerscale)
blockImages = functions.getImages(functions.scale(pygame.image.load("data/assets/christmasGameTiles.png"),4),4*4)
gunImage = functions.scale(pygame.image.load("data/assets/christmasGame_player_gun.png"), playerscale)

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.paintPos = Vec2((0,0))
        self.vec = Vec2((0,0))
        self.keysPressed = None
        self.keysPressed_once = None
        self.speed = 20
        self.running = False
        self.grounded = False
        self.jumpTimer = 0
        self.size = playersize
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y,self.size.x, self.size.y)
        self.mainImage = pygame.transform.scale(pygame.image.load("data/assets/christmasGame_player_standing.png"),(10*playerscale, 20*playerscale))
        self.direction = True
        self.Image = self.mainImage
        self.runAnimationFrame = 0
        self.range = 100
        self.radius = 20
        self.radiusMax = 20
        self.makeBlockType = 0

        self.gunAngle = 0
        self.selectedItem = 0
        self.UI = UI.UI



    def move(self):
        self.keysPressed = pygame.key.get_pressed()
        if self.keysPressed[pygame.K_a]:
            self.running = True
            self.direction = 1
            self.runAnimationFrame += 0.2
            self.vec.decrement(Vec2((2, 0)))
        elif self.keysPressed[pygame.K_d]:
            self.running = True
            self.direction = 0
            self.runAnimationFrame += 0.2
            self.vec.increment(Vec2((2, 0)))
        else:
            self.running = False
            self.runAnimationFrame = 0

        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    if self.radius < self.radiusMax:
                        self.radius += 1
                elif event.y == -1:
                    if self.radius > 1:
                        self.radius -= 1

        self.vec.update_x(self.vec.x/1.1)

        if self.keysPressed[pygame.K_SPACE]:
            if self.jumpTimer < -10 and self.grounded:
                self.grounded = False
                self.jumpTimer = 10

        if self.jumpTimer > 0:
            self.vec.increment(Vec2((0, -self.jumpTimer/3)))

        self.jumpTimer -= 1

    def update(self):
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        #gravity

        self.vec+=Vec2((0,1))
        self.direction = self.vec.x > 0

    def updateHitbox(self):
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def WorldEditUpdate(self, world,offset, mouse_pos):
        self.selectedItem = self.UI.Inventory.selectedStack

        direction = mouse_pos - (self.pos + offset)
        if direction.mag > self.range:
            paintPos = self.pos + (direction.normalise() * self.range)
        else:
            paintPos = self.pos + direction
        self.paintPos = paintPos
        if pygame.mouse.get_pressed()[0]:


            world.paint(self.paintPos+offset, self.radius, 0, self.UI.Inventory.stacks[0])

        elif pygame.mouse.get_pressed()[2]:
            if self.selectedItem != -1:
                world.paint(self.paintPos + offset, self.radius, self.UI.Inventory.stacks[self.selectedItem].type, self.UI.Inventory.stacks[self.selectedItem])


    def draw(self, offset, screen):
        # pygame.draw.rect(screen, (255,0,0), self.hitbox.move(offset.x, offset.y))
        self.Image = self.mainImage
        if abs(self.vec.x) > 0:
            if self.runAnimationFrame >= 8:
                self.runAnimationFrame = 1
            self.Image = animationFrames[int(self.runAnimationFrame)]
        else:
            self.runAnimationFrame = 0




        mouse_pos = Vec2(pygame.mouse.get_pos())
        direction = mouse_pos - (self.pos+offset)
        self.gunAngle = direction.get_angle()
        screen.blit(pygame.transform.flip(self.Image, not self.direction, False), (self.pos + offset).position)

        if not pygame.mouse.get_pressed()[2] or self.selectedItem == -1:
            angleOffset = 0
            if self.gunAngle < 0:
                image = pygame.transform.flip(gunImage, 1, 0)
                angleOffset = 180
            else:
                image = gunImage

            gunRotImage = pygame.transform.rotate(image, self.gunAngle-90+angleOffset)

            anotherGunOffset = direction.normalise() * self.size.x / 2

            gunOffset = Vec2(gunRotImage.get_size())/2


            screen.blit(gunRotImage, (self.pos + self.size/2-gunOffset + offset +anotherGunOffset).position)

            # if pygame.mouse.get_pressed()[0]:


        else:
            blockRotImage = pygame.transform.rotate(blockImages[self.selectedItem], self.gunAngle - 90)
            blockOffset = Vec2(blockRotImage.get_size()) / 2
            anotherBlockOffset = direction.normalise() * self.size.x / 2

            screen.blit(blockRotImage, (self.pos+self.size/2-blockOffset + offset + anotherBlockOffset).position)

        pygame.draw.circle(screen, (0, 0, 0), (self.paintPos + offset).position, self.radius + 2, 2)

    def UIUpdate(self):
        self.UI.update(self)

    def UIDraw(self, screen):
        self.UI.draw(screen)