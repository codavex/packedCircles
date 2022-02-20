#!/usr/bin/python3

import Circle
import configparser
import math
import random
import sys


def intersect(test, circles, cushion):
    for circle in circles:
        if test.intersect(circle, cushion):
            return True
    return False


if len(sys.argv) != 3:
    print("Incorrect number of command line parameters.")
    print("Usage:")
    print("  %s config_file output_file" % (sys.argv[0]))
    exit(0)

Config = configparser.ConfigParser()
Config.read(sys.argv[1])

# get the authentication information from the cfg file
NUM_CIRCLES = Config.getint("circles", "NUM_CIRCLES")
RADIUS = Config.getfloat("circles", "RADIUS")
RADIUS_PLUSMINUS = Config.getfloat("circles", "RADIUS_PLUSMINUS")

SEED_STRING = Config.get("variables", "SEED_STRING")
DELTA = RADIUS/100
START_HEIGHT = RADIUS*2
CUSHION = Config.getfloat("variables", "CUSHION")
MAX_RIGHT = Config.getfloat("variables", "MAX_RIGHT")

random.seed(SEED_STRING)

maxHeight = 0
circles = []
baseRadius = RADIUS - (RADIUS_PLUSMINUS/2)
for i in range(NUM_CIRCLES):
    radius = baseRadius + (RADIUS_PLUSMINUS * random.random())
    testX = radius + (MAX_RIGHT - 2*RADIUS)*random.random()
    testY = (maxHeight + (RADIUS+RADIUS_PLUSMINUS))*3
    testR = radius

    cantDrop = False
    while cantDrop is False:
        while (intersect(Circle.Circle(testX, testY-DELTA, testR), circles, CUSHION) is False) and testY-DELTA > radius:
            testY -= DELTA
        cantDrop = True
        if (intersect(Circle.Circle(testX-DELTA, testY, testR), circles, CUSHION) is False) and testX-DELTA > radius:
            testX -= DELTA
            cantDrop = False
            continue
        if (intersect(Circle.Circle(testX+25*DELTA, testY-DELTA, testR), circles, CUSHION) is False) and testX+25*DELTA < MAX_RIGHT and testY-DELTA > radius:
            testX += 25*DELTA
            testY -= DELTA
            cantDrop = False
            continue
        if testY - radius <= DELTA:
            break
    circles.insert(0, Circle.Circle(testX, testY, testR))
    if(testY > maxHeight):
        maxHeight = testY
    print("%d / %d" % (i + 1, NUM_CIRCLES), end="\r", flush=True)
print("")

f = open(sys.argv[2], "w")
f.write("include \"pigment_function.inc\"\n")
f.write("\n")
for circle in circles:
    f.write("object {")
    f.write(" sphere { <%f, %f, 0> %f }" % (circle._x, circle._y, circle._r))
    f.write(" texture { finish { ambient 1 }")
    f.write(" pigment { color <")
    f.write(" pigment_function(%f, %f, 0).red," % (circle._x, circle._y))
    f.write(" pigment_function(%f, %f, 0).green," % (circle._x, circle._y))
    f.write(" pigment_function(%f, %f, 0).blue" % (circle._x, circle._y))
    f.write("> } } }\n")
f.close()
