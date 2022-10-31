add_library('peasycam')
rotate_angle = 0

def setup():
    size(1200, 800, P3D)
    cam = PeasyCam(this, 500)
    

def draw():
    global rotate_angle
    background(0)
    lights()
    stroke(255, 0, 0)
    line(-1000, 0, 0, 1000, 0, 0)
    line(0, -1000, 0, 0, 1000, 0)
    line(0, 0, -1000, 0, 0, 1000)
    
    rotate_angle += 0.1
    # rotateY(rotate_angle)
    stroke(120)
    diamond()
    
    
def diamond():
    y_distance = 50
    center = (0, 3*y_distance, 0)
    
    radius = 200
    divisions = 400
    lower_points = []
    upper_points = []
    for i in range(divisions):
        angle = i * TWO_PI/divisions 
        x = radius * cos(angle)
        y = 0
        z = radius * sin(angle) 
        lower_points.append((x, y, z))
        upper_points.append((0.5 * x, y - y_distance, 0.5 * z))
        
    noFill()
    beginShape()
    for p in upper_points:
        vertex(*p)    
    endShape(CLOSE)
    
    beginShape()
    for p in lower_points:
        vertex(*p)    
    endShape(CLOSE)
    
    for l, u in zip(lower_points, upper_points):
        line(*(l + u))
        
    for p in lower_points:
        line(*(p + center))
