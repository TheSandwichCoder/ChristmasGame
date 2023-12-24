import math
from data import Perlin
from data import settings
import pygame

noise=Perlin.Perlin()

size = int(settings.EldestNodeSize/settings.TILESIZE*settings.WorldSize[0])
print("Here")
print(settings.EldestNodeSize)
print(settings.TILESIZE)
print(settings.WorldSize[0])
print(size)
print(settings.WorldSize[0]*size)
terrain=[noise.valueAt(i/size*settings.WorldSize[0]) for i in range(size*settings.WorldSize[0])]
#
# for i in range(100):
#     print(terrain[i])

# perlinNoise = Perlin.generate_fractal_noise_2d([settings.WorldSize[0]*size,settings.WorldSize[1]*size],[8,8])
# print("done 1")
# perlinNoise2 = Perlin.generate_fractal_noise_2d([settings.WorldSize[0]*size,settings.WorldSize[1]*size],[8,8])
# print("done 2")
# perlinNoise3 = Perlin.generate_fractal_noise_2d([settings.WorldSize[0]*size,settings.WorldSize[1]*size],[8,8])
# print("done 3")
# perlinNoise4 = Perlin.generate_fractal_noise_2d([settings.WorldSize[0]*size,settings.WorldSize[1]*size],[8,8])
# print("done 4")

caveNoiseArray = []

print("CREATING CAVE NOISE")
for i in range(settings.NUMOFNOISEMAPS):
    caveNoiseArray.append(Perlin.generate_fractal_noise_2d([settings.NOISESIZE,settings.NOISESIZE],[8,8]))
    # caveNoiseArray.append(Perlin.generate_perlin_noise(int(settings.NOISESIZE/2), int(settings.NOISESIZE/2)))
    print("NOISE",i,"CREATED")

ironNoiseArray = []

print("CREATING IRON ORE NOISE")
for i in range(settings.NUMOFNOISEMAPS*2):
    ironNoiseArray.append(Perlin.generate_fractal_noise_2d([int(settings.NOISESIZE/4),int(settings.NOISESIZE/4)],[8,8]))
    print("NOISE",i,"CREATED")

diamondNoiseArray = []
print("CREATING DIAMOND ORE NOISE")
for i in range(settings.NUMOFNOISEMAPS*2):
    diamondNoiseArray.append(Perlin.generate_fractal_noise_2d([int(settings.NOISESIZE/4),int(settings.NOISESIZE/4)],[8,8]))
    print("NOISE",i,"CREATED")




def clamp(low, high, n):
    if n < low:
        return low
    if n > high:
        return high
    return n

def clip(image, x, y, width, height):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    surf.blit(image,(-x,-y))
    return surf

def getImages(image, x):
    image_size = image.get_size()
    array = [clip(image,x*i,0,x,image_size[1]) for i in range(int(image_size[0]/x))]
    return array

def scale(image, x):
    image_size = image.get_size()
    image = pygame.transform.scale(image, (x*image_size[0], x*image_size[1]))
    return image

def getRepeatedTiles(image, n, list):
    if n<=0:
        return list

    imageSize = image.get_size()
    surface = pygame.Surface((imageSize[0]*2, imageSize[1]*2))
    for x in range(2):
        for y in range(2):
            surface.blit(image, (x*imageSize[0], y*imageSize[1]))

    list.append(surface)
    return getRepeatedTiles(surface, n-1, list)

def fastLog2(n):
    counter = 0
    n2 = n
    while n2 > 2:
        n2/=2
        counter += 1
    return counter


def distance_point_to_square(p1, s1, sidelength):
    half_side_length = sidelength / 2

    dx = abs(p1.x - (s1.x+half_side_length)) - half_side_length
    dy = abs(p1.y - (s1.y+half_side_length)) - half_side_length
    return max(dx, dy, 0) if min(dx, dy) < 0 else math.sqrt(dx ** 2 + dy ** 2)

def min2(x, n):
    if x<n:
        return n
    else:
        return x

def max2(x, n):
    if x > n:
        return n
    return x

def myCorrectModulo(x,n):
    if x > 0:
        return x%n
    elif x < 0:
        return -(abs(x)%n)
    else:
        return 0


