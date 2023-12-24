import math



class Vec2():
    def __init__(self,pos):
        self.x = pos[0]
        self.y = pos[1]
        self.position = pos
        self.mag = self.get_len()

    def get_len(self):
        len = math.sqrt(self.x**2+self.y**2)

        if len == 0:
            return 0.1

        return len

    def normalise_self(self):
        self.x, self.y = self.x / self.mag, self.y / self.mag
        self.mag = 1

    def makeToLength(self, len):
        self.normalise_self()
        self.update(self.x*len, self.y*len)

    def normalise(self):
        return Vec2((self.x / self.mag, self.y / self.mag))

    def update(self,x,y):
        self.x = x
        self.y = y
        self.position = (x,y)
        self.mag = self.get_len()


    def update_x(self, x):
        self.update(x, self.y)


    def update_y(self, y):
        self.update(self.x, y)

    def __add__(self, vec2_2):
        return Vec2((self.x + vec2_2.x, self.y+vec2_2.y))

    def __sub__(self, vec2_2):
        return Vec2((self.x - vec2_2.x, self.y-vec2_2.y))

    def __mul__(self, n):
        return Vec2((self.x*n, self.y*n))

    def __truediv__(self, n):
        if n != 0:
            return Vec2((self.x/n, self.y/n))
        else:
            return ZeroDivisionError

    def __neg__(self):
        return Vec2((-self.x, -self.y))

    def int(self):
        return Vec2((int(self.x), int(self.y)))

    def get_angle(self):
        return math.atan2(self.x, self.y)*180/math.pi


    def increment(self,vec):
        self.update(self.x + vec.x, self.y + vec.y)

    def decrement(self,vec):
        self.update(self.x - vec.x, self.y - vec.y)

    def x_increment(self,x):
        self.update(self.x + x, self.y)

    def y_increment(self,y):
        self.update(self.x, self.y + y)

    def __floordiv__(self, n):
        return Vec2((self.x//n, self.y//n))

    def __hash__(self):
        return int(((self.x * (31 / (math.tan(self.x + 1) ** 2 + 1) + 0.34324)) * (self.y * 5.12) / 237) % 5000)
