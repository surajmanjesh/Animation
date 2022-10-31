from itertools import product
add_library('peasycam')

M = 30

def setup():
    fullScreen(P3D)
    cam = PeasyCam(this, 100)
    colorMode(HSB, M, M, M, M)
    
def draw():
    background(0, 0, 0)
    strokeWeight(3)
    for h in range(M):
        for s in range(M):
            for b in range(M):
                stroke((h + s + b)/3 , M, M)
                point(h - M/2, s - M/2, b - M/2)
