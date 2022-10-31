add_library('peasycam')

R = 100
def setup():
    size(1200, 800, P3D)
    cam = PeasyCam(this, 300)
    colorMode(HSB, R, 100, 100, 100)
    # sphereDetail(6)

def draw():
    background(0)
    fractal(R, 3)

def fractal(r, N):
    if N <= 0: 
        return 
    D = 3
    for d in range(D):
        
        angle = d * 2 * PI / D
        
        x = r * cos(angle)
        y = r * sin(angle)
        
        stroke((x + y)%R, 100, 100, 100)
        # fill((x + y)%R, 100, 100, 25)
        strokeWeight(1)

        line(0, 0, 0, x, y, 0)
        # point(x, y, 0)
        
        pushMatrix()
        translate(x, y, 0)
        rotate(PI/2, x, y, 0)
        # sphere(r)
        fractal(r/2, N-1)
        popMatrix()
