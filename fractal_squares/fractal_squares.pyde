add_library('peasycam')

n = 150
counter = 0
points = []

def setup():
    size(1200, 800, P3D)
    cam = PeasyCam(this, 300)
    colorMode(HSB, n, 100, 100, 100)
    lights()
    stroke(255)
    strokeWeight(4);
    
    radius = 100
    divisions = 4
    global points 
    for i in range(divisions):
        angle = i * TWO_PI/divisions 
        x = radius * cos(angle)
        y = 0
        z = radius * sin(angle) 
        points.append(PVector(x, y, z))

def draw():
    background(0)
    fractal(points, n)
    global counter 
    counter += 1
    counter %= n

def vector_to_points(p):
    return (p.x, p.y, p.z)

def ratio(a, b, r):
    p1 = a.copy()
    p2 = b.copy()
    p1 = p1.mult(r)
    p2 = p2.mult(1 - r)
    return p1.add(p2)

def fractal(points, n):
    noFill()
    r = 0.05
    
    for i in range(n):
        stroke((i + floor(counter)) % n, 100, 100)
        
        translate(0, i, 0)
        rotateY(r)
        scale(1 - r)
        
        beginShape()
        for p in points:
            vertex(*vector_to_points(p))
        endShape(CLOSE)
        
