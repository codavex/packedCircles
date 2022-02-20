from math import sqrt


class Circle:
    def __init__(self, x, y, r):
        self._x = x
        self._y = y
        self._r = r

    def __repr__(self):
        return "(%f, %f, %f)" % (self._x, self._y, self._r)

    def __str__(self):
        return "(%f, %f, %f)" % (self._x, self._y, self._r)

    def getCentre(self):
        ruturn(self._x, self._y)

    def getRadius(self):
        return self._r

    def intersect(self, other, cushion=0):
        xdiff = self._x - other._x
        ydiff = self._y - other._y
        dist = sqrt(xdiff**2+ydiff**2)
        if dist < self._r + other._r + cushion:
            return True
        return False
