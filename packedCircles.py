#!/usr/bin/python3

import Circle
import configparser
import math
import random
import sys

# does a test circle intersect with a list of circles, with a given 'cushion'
def intersect(test, circles, cushion):
    for circle in circles:
        if test.intersect(circle, cushion):
            return True
    return False

# check we have a config file and an output file
if len(sys.argv) != 3:
    print("Incorrect number of command line parameters.")
    print("Usage:")
    print("  %s config_file output_file" % (sys.argv[0]))
    exit(0)

Config = configparser.ConfigParser()
Config.read(sys.argv[1])

# get the information from the cfg file
NUM_CIRCLES = Config.getint("circles", "NUM_CIRCLES")
RADIUS = Config.getfloat("circles", "RADIUS")
RADIUS_PLUSMINUS = Config.getfloat("circles", "RADIUS_PLUSMINUS")

SEED_STRING = Config.get("variables", "SEED_STRING")
DELTA = RADIUS/100
CUSHION = Config.getfloat("variables", "CUSHION")
MAX_RIGHT = Config.getfloat("variables", "MAX_RIGHT")

# set up variables using config data
baseRadius = RADIUS - (RADIUS_PLUSMINUS/2)
headNum = int(2 * (MAX_RIGHT / RADIUS))

# set up other variables needed
currentMaxHeight = 0
circles = []

# lets do this
random.seed(SEED_STRING)
for i in range(NUM_CIRCLES):
    # X and Y might change, so they are test values
    # radius stays the same
    radius = baseRadius + (RADIUS_PLUSMINUS * random.random())
    testX = radius + (MAX_RIGHT - 2*RADIUS)*random.random()
    testY = (currentMaxHeight + (RADIUS+RADIUS_PLUSMINUS))*3

    # find a subset of circles to test intersections against
    # because we prepend new circles, these will always be the most recent
    # and therefore highest circles. As new circles start from the top and
    # move down, we don't need to check if the test circle intersects with
    # circles at the bottom
    circlesSubset = circles[0:headNum]

    cantDrop = False
    while cantDrop is False:
        while (intersect(Circle.Circle(testX, testY-DELTA, radius), circlesSubset, CUSHION) is False) and testY-DELTA > radius:
            testY -= DELTA
        cantDrop = True
        if (intersect(Circle.Circle(testX-DELTA, testY, radius), circlesSubset, CUSHION) is False) and testX-DELTA > radius:
            testX -= DELTA
            cantDrop = False
            continue
        if (intersect(Circle.Circle(testX+25*DELTA, testY-DELTA, radius), circlesSubset, CUSHION) is False) and testX+25*DELTA < MAX_RIGHT and testY-DELTA > radius:
            testX += 25*DELTA
            testY -= DELTA
            cantDrop = False
            continue
        if testY - radius <= DELTA:
            break
    # insert at the start, therefore all the circles at the 'top'
    # are at the head of the list, so we can use that to just test
    # intersections against the 'highest' circles
    circles.insert(0, Circle.Circle(testX, testY, radius))

    # set a new currentMaxHeight so we're start higher than the highest circle
    if(testY > currentMaxHeight):
        currentMaxHeight = testY
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
