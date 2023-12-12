import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Vector(' + str(self.x) + ',' + str(self.y) + ')'

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def size(self):
        return (self.x ** 2 + self.y ** 2) ** (1 / 2)

    def norm(self):
        size = self.size()
        return Vector(round(self.x / size, 3), round(self.y / size, 3))

    def right(self):
        return Vector(self.y, -self.x)

    def left(self):
        return Vector(-self.y, self.x)

    def crossproduct(self, other):
        return self.x * other.y - self.y * other.x

    def rotate(self, theta):
        new_x = self.x * math.cos(theta) - self.y * math.sin(theta)
        new_y = self.x * math.sin(theta) + self.y * math.cos(theta)

        return Vector(new_x,new_y)


    def degree(self, other):
        inner_product = self.x * other.x + self.y * other.y
        size = self.size() * other.size()
        cos = inner_product / size
        if cos > 1:
            cos = 1
        if cos < -1:
            cos = -1
        degree = math.acos(cos)
        return degree