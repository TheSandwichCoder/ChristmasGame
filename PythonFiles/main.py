import pygame
from data import settings
from data import vector
from data import Interatables
Vec2 = vector.Vec2
# settings.DEPTH = input("")

pygame.init()
pygame.display.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280,720), pygame.RESIZABLE)
clock = pygame.time.Clock()
Title = pygame.transform.scale_by(pygame.image.load("data/assets/TitleImage.png"), (15,15))
BackgroundImage = pygame.transform.scale(pygame.image.load("data/assets/christmasGame_background.png"),(1280,720))
gameScreen = pygame.transform.scale_by(pygame.image.load("data/assets/NNN_gameScreen.png"), (35.5,37))
music = pygame.mixer.music.load("data/assets/SFX/enchanted-chimes-177906.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

fader = pygame.Surface((1280, 720))  # the size of your rect
fader.set_alpha(100)  # alpha level
fader.fill((0,0,0))  # this fills the entire surface

playButton = Interatables.ButtonResizeable(Vec2((527.5, 375)),Vec2((225,75)),False, True, "PLAY", 0)

WorldSizeX_slider = Interatables.Slider(Vec2((350,200)),300, 0, "X-SIZE")
WorldSizeY_slider = Interatables.Slider(Vec2((350,250)),300, 0, "Y-SIZE")
WorldResolution_slider = Interatables.Slider(Vec2((350,300)),300, 0.5, "RESOLUTION")
makeWorldButton = Interatables.ButtonResizeable(Vec2((250, 400)),Vec2((225,75)),False, True, "CREATE WORLD", 0)

font = pygame.font.Font("data/assets/font/PixelifySans-VariableFont_wght.ttf",30)
largerFont = pygame.font.Font("data/assets/font/PixelifySans-VariableFont_wght.ttf",60)


running = True
InSettings = True
initialise = False
gamestate = "Menu"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()


    screen.fill((255,255,255))

    if InSettings:
        screen.blit(BackgroundImage, (0, 0))
        screen.blit(fader, (0, 0))
        screen.blit(Title, (152.5, 60))
        if gamestate == "Menu":
            playButton.update(Vec2((0,0)))
            playButton.draw(screen)
            if playButton.activated:
                gamestate = "Settings"

        elif gamestate == "Settings":
            screen.blit(gameScreen, (0,0))
            WorldSizeX_slider.update()
            WorldSizeY_slider.update()
            WorldResolution_slider.update()
            makeWorldButton.update(Vec2((0,0)))

            WorldSizeX_slider.value = int(WorldSizeX_slider.sliderPos*19+5)
            WorldSizeY_slider.value = int(WorldSizeY_slider.sliderPos*6+2)
            WorldResolution_slider.value = int(WorldResolution_slider.sliderPos*5-3)

            settings.WorldSize = (WorldSizeX_slider.value, WorldSizeY_slider.value)
            settings.resolution = WorldResolution_slider.value

            settings.DEPTH = 7 + settings.resolution
            settings.EldestNodeSize = 2 ** (settings.DEPTH + 4 - settings.resolution)
            settings.TILESIZE = settings.EldestNodeSize * (0.5 ** (settings.DEPTH + 1))
            settings.NOISESIZE = int(settings.EldestNodeSize / settings.TILESIZE * 16)

            if WorldResolution_slider.value == 2:
                screen.blit(font.render("Do you hate your PC?",1,(255,255,255)), (800,300))

            WorldSizeX_slider.draw(screen)
            WorldSizeY_slider.draw(screen)
            WorldResolution_slider.draw(screen)
            makeWorldButton.draw(screen)
            if makeWorldButton.activated:
                screen.blit(BackgroundImage, (0, 0))
                screen.blit(fader, (0, 0))



                screen.blit(largerFont.render("Creating World...",1,(0,0,0)), (400,324))
                screen.blit(font.render("Just Trust Bro",1,(0,0,0)), (519.5,392))
                pygame.display.flip()
                initialise = True

        if initialise:
            #import and initialise everything

            from data import World
            from data import player

            from data import Particles
            from data import SantaShop
            from data import backgroundOptimisation
            from data import functions
            from data import SFX

            player = player.Player(Vec2((100, 0)))
            SantaShop = SantaShop.SantaShop(Vec2((100, 650)))
            particles = Particles.particleContainer
            background = functions.scale(pygame.image.load("data/assets/christmasGame_background.png"), 20)
            backgroundObject = backgroundOptimisation.Background(background)
            backgroundSize = ((backgroundObject.backgroundSize.x-1280) * 20, backgroundObject.backgroundSize.y * 2)
            chunks = World.ChunksHandler(Vec2(settings.WorldSize))
            initialise = False
            InSettings = False




    else:
        # screen.blit(background, (0+chunks.offset.x/40,0+chunks.offset.y/2))
        # print(chunks.offset.position, abs(chunks.offset.x)%backgroundSize[0])
        backgroundObject.draw(screen, Vec2((((functions.myCorrectModulo(chunks.offset.x, backgroundSize[0]))/20-100),functions.min2(chunks.offset.y/2-100, -backgroundSize[1]/2+1280))))
        pygame.draw.rect(screen, (184, 184, 184), pygame.Rect(0,settings.WorldSize[1]*settings.EldestNodeSize/2+chunks.offset.y, 1280,400))
        pygame.draw.rect(screen, (184, 184, 184), pygame.Rect(chunks.offset.x-800,functions.min2(1000+chunks.offset.y,0), 800,720))
        pygame.draw.rect(screen, (181, 119, 85), pygame.Rect(chunks.offset.x-800,860+chunks.offset.y, 800,140))
        pygame.draw.rect(screen, (87, 204, 103), pygame.Rect(chunks.offset.x-800,800+chunks.offset.y, 800,60))
        pygame.draw.rect(screen, (184, 184, 184),pygame.Rect(settings.WorldSize[0]*settings.EldestNodeSize/2+chunks.offset.x, functions.min2(1000 + chunks.offset.y, 0), 800, 720))
        pygame.draw.rect(screen, (181, 119, 85), pygame.Rect(settings.WorldSize[0]*settings.EldestNodeSize/2+chunks.offset.x, 860 + chunks.offset.y, 800, 140))
        pygame.draw.rect(screen, (87, 204, 103), pygame.Rect(settings.WorldSize[0]*settings.EldestNodeSize/2+chunks.offset.x, 800 + chunks.offset.y, 800, 60))

        mouse_pos = Vec2(pygame.mouse.get_pos())
        keys = pygame.key.get_pressed()


        chunks.loadChunks(player)

        player.WorldEditUpdate(chunks, chunks.offset, mouse_pos)

        SantaShop.update(player, chunks.offset)
        chunks.updateAllBlocks()

        chunks.updateSurfaces()
        SFX.updateSFX()
        SantaShop.draw(chunks.offset, screen)
        chunks.draw(player.pos, screen)

        player.move()
        player.update()
        chunks.offset = -player.pos + Vec2((1280 / 2, 720 / 2))
        particles.update(player)
        particles.draw(chunks.offset, screen)
        player.draw(chunks.offset, screen)
        chunks.playerCollision(player)

        player.UIUpdate()
        player.UIDraw(screen)

        if keys[pygame.K_n]:
            pack = chunks.getBlockNum()
            print("Number of Nodes",pack[0],"              Nodes Loaded", pack[1], "           Nodes Unloaded", len(chunks.chunks)-pack[1])
        if keys[pygame.K_r]:
            player.pos.update(100,0)



    clock.tick(60)
    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.flip()

