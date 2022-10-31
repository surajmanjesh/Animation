from p5 import *

angle = 0

width = 640
height = 360

radius = 100


def setup():
    size(width, height, P3D)
    background(255, 255, 100)


def draw():
    global angle
    start = (width/2, height/2)
    x = radius * cos(angle)
    y = radius * sin(angle)
    end = (width/2 + x, height/2 + y)

    line(start, end)

    if angle < 5 * TWO_PI:
        angle += 0.1
    else:
        no_loop()


if __name__ == '__main__':
    run()
