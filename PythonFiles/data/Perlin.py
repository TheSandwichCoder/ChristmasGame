# NOTE:
# All of this code(l1-43) is made by Supreme Sector so really thanks to him
# Video: https://www.youtube.com/watch?v=QHdU1XRB9uw
# Github: https://github.com/Supreme-Sector/Python-Perlin-Noise

import random
import numpy as np


class Perlin:
    def __init__(self):
        self.gradients = []
        self.lowerBound = 0


    def valueAt(self, t):
        if(t<self.lowerBound):
            print("ERROR: Input parameter out of bounds!")
            return
        # Add to gradients until it covers t
        while t >= len(self.gradients)-1+self.lowerBound:
            self.gradients.append(random.uniform(-1, 1))

        discarded = int(self.lowerBound) # getting number of gradients that have been discarded
        # Compute products between surrounding gradients and distances from them
        d1 = (t-t//1)
        d2 = d1-1
        a1 = self.gradients[(int)(t//1)-discarded]*d1
        a2 = self.gradients[(int)(t//1+1)-discarded]*d2

        amt = self.__ease(d1)

        return self.__lerp(a1,a2,amt)

    def discard(self, amount):
        gradientsToDiscard = int(amount+self.lowerBound%1)
        self.gradients = self.gradients[gradientsToDiscard:]
        self.lowerBound += amount

    def __ease(self, x):
        return 6*x**5-15*x**4+10*x**3


    def __lerp(self, start, stop, amt):
        return amt*(stop-start)+start

# NOTE:
# All of this code(l45-) is made by pvigier so really thanks to another smarter guy than me
# Github: https://github.com/pvigier/perlin-numpy/blob/master/perlin_numpy/perlin2d.py

def interpolant(t):
    return t*t*t*(t*(t*6 - 15) + 10)


def generate_perlin_noise_2d(shape, res, tileable=(False, False), interpolant=interpolant):
    # print("here")
    """Generate a 2D numpy array of perlin noise.

    Args:
        shape: The shape of the generated array (tuple of two ints).
            This must be a multple of res.
        res: The number of periods of noise to generate along each
            axis (tuple of two ints). Note shape must be a multiple of
            res.
        tileable: If the noise should be tileable along each axis
            (tuple of two bools). Defaults to (False, False).
        interpolant: The interpolation function, defaults to
            t*t*t*(t*(t*6 - 15) + 10).

    Returns:
        A numpy array of shape shape with the generated noise.

    Raises:
        ValueError: If shape is not a multiple of res.
    """
    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0], 0:res[1]:delta[1]]\
             .transpose(1, 2, 0) % 1
    # Gradients
    angles = 2*np.pi*np.random.rand(res[0]+1, res[1]+1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    if tileable[0]:
        gradients[-1,:] = gradients[0,:]
    if tileable[1]:
        gradients[:,-1] = gradients[:,0]
    gradients = gradients.repeat(d[0], 0).repeat(d[1], 1)
    g00 = gradients[    :-d[0],    :-d[1]]
    g10 = gradients[d[0]:     ,    :-d[1]]
    g01 = gradients[    :-d[0],d[1]:     ]
    g11 = gradients[d[0]:     ,d[1]:     ]
    # Ramps
    n00 = np.sum(np.dstack((grid[:,:,0]  , grid[:,:,1]  )) * g00, 2)
    n10 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]  )) * g10, 2)
    n01 = np.sum(np.dstack((grid[:,:,0]  , grid[:,:,1]-1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)
    # Interpolation
    t = interpolant(grid)
    n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
    n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
    return np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)


def generate_fractal_noise_2d(shape, res, octaves=1, persistence=0.4,lacunarity=1, tileable=(False, False),interpolant=interpolant
):
    """Generate a 2D numpy array of fractal noise.

    Args:
        shape: The shape of the generated array (tuple of two ints).
            This must be a multiple of lacunarity**(octaves-1)*res.
        res: The number of periods of noise to generate along each
            axis (tuple of two ints). Note shape must be a multiple of
            (lacunarity**(octaves-1)*res).
        octaves: The number of octaves in the noise. Defaults to 1.
        persistence: The scaling factor between two octaves.
        lacunarity: The frequency factor between two octaves.
        tileable: If the noise should be tileable along each axis
            (tuple of two bools). Defaults to (False, False).
        interpolant: The, interpolation function, defaults to
            t*t*t*(t*(t*6 - 15) + 10).

    Returns:
        A numpy array of fractal noise and of shape shape generated by
        combining several octaves of perlin noise.

    Raises:
        ValueError: If shape is not a multiple of
            (lacunarity**(octaves-1)*res).
    """
    noise = np.zeros(shape)
    frequency = 1
    amplitude = 1
    for _ in range(octaves):
        noise += amplitude * generate_perlin_noise_2d(
            shape, (frequency*res[0], frequency*res[1]), tileable, interpolant
        )
        frequency *= lacunarity
        amplitude *= persistence
    return noise

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(t, a, b):
    return a + t * (b - a)

def gradient(hash_value, x, y):
    h = hash_value & 15
    grad = 1 + (h & 7)  # Gradient value 1-8
    if h & 8:
        grad = -grad  # Randomly invert half of the gradients
    return (grad * x) + (grad * y)

def perlin_noise_2d(x, y):
    X = int(x) & 255
    Y = int(y) & 255

    x -= int(x)
    y -= int(y)

    u = fade(x)
    v = fade(y)

    # Hash coordinates of the 4 cube corners
    aa, ab, ba, bb = p[X] + Y, p[X + 1] + Y, p[X] + Y + 1, p[X + 1] + Y + 1

    # And add blended results from 4 corners of the cube
    result = lerp(v, lerp(u, gradient(p[aa], x, y), gradient(p[ba], x-1, y)),lerp(u, gradient(p[ab], x, y-1), gradient(p[bb], x-1, y-1)))

    return result

def generate_perlin_noise(width, height, scale=5, octaves=1, persistence=1, lacunarity=1, seed=42):
    global p
    p = list(range(512))
    random.seed(seed)
    random.shuffle(p)
    p += p  # Duplicate the permutation list to avoid index wrapping

    noise_map = [[0] * height for _ in range(width)]

    for i in range(width):
        for j in range(height):
            amplitude = 1
            frequency = 1
            noise_value = 0

            for _ in range(octaves):
                sample_x = i / scale * frequency
                sample_y = j / scale * frequency

                perlin_value = perlin_noise_2d(sample_x, sample_y)
                noise_value += perlin_value * amplitude

                amplitude *= persistence
                frequency *= lacunarity

            noise_map[i][j] = noise_value

    return noise_map
