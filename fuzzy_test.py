import fuzzySpeed
import random


if __name__ == '__main__':

    speed = 3
    angle = -50
    inf10 = -5
    inf30 = 15
    inf50 = 52
    inf70 = 38

    g = fuzzySpeed.Algorithm()
    r = g.findSpeed(speed, angle, inf10, inf30, inf50, inf70)
    # print(r)
