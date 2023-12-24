import pygame
pygame.font.init()

resolution = 0
DEPTH = 7+resolution
EldestNodeSize = 2**(DEPTH+4-resolution)
TILESIZE = EldestNodeSize*(0.5**(DEPTH+1))
WorldSize = (5,2)

NUMOFTYPES = 11

HAVESURFACEDEPTH = 5
LOADCHUNKSPEED = 2
NUMOFNOISEMAPS = 4
ITEMSTACKMAX = 1024

NOISESIZE = int(EldestNodeSize/TILESIZE * 16)

font = pygame.font.Font("data/assets/font/PixelifySans-VariableFont_wght.ttf",10)




print(NOISESIZE)
