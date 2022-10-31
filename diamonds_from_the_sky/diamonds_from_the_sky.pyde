from itertools import product
add_library('peasycam')

cam = None
octagons = []

def setup():
    fullScreen(P3D)
    global cam, o
    cam = PeasyCam(this, 700)
    colorMode(HSB, 100, 100, 100, 100)
    for i in range(100):
        octagons.append(Octahedron(PVector(random(-width/2, width/2),
                                           random(-height/2, height/2),
                                           random(-width/2, width/2)), random(5, 20)))
    
def draw():
    background(0)
    # rotateX(PI/2)
    for o in octagons:
        o.update()
        o.show()
    saveFrame("diamonds_sky/img-####.tif")
        
def normalize_color(c):
    return map(c, -1, 1, 0, 255)

class Triangle:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
  
    def __repr__(self):
        return "Triangle(v1={v1}, v2={v2}, v3={v3})".format(v1=self.v1, v2=self.v2, v3=self.v3)
    
    def normal(self):
        line1 = self.v2 - self.v1
        line2 = self.v3 - self.v1
        return (line1).cross(line2).normalize();

    def show(self):
        fill(self.get_color())
        
        beginShape()
        
        vertex(self.v1[0], self.v1[1], self.v1[2])
        vertex(self.v2[0], self.v2[1], self.v2[2])
        vertex(self.v3[0], self.v3[1], self.v3[2])
        
        endShape(CLOSE)
    
    def get_color(self):
        camera_points = cam.getPosition()
        camera_position = PVector(camera_points[0], camera_points[1], camera_points[2])
        n = self.normal()
        colors = n.cross(camera_position).normalize()
        
        r = map(colors.x, -1, 1, 0, 50)
        g = map(colors.y, -1, 1, 25, 50)
        b = map(colors.z, -1, 1, 80, 100)
        
        r = map(colors.x, -1, 1, 50, 100)
        g = map(colors.y, -1, 1, 50, 100)
        b = map(colors.z, -1, 1, 50, 100)
        a = 100
        
        return color(r, g, b, a)
    
class Octahedron:
    def __init__(self, center, side):
        self.center = center
        self.side = side
        self.height_scale = random(1.5, 2)
        self.velocity = PVector(0, 1, 0)
        self.rotation_angle = 0
       
    def update(self):
        # self.center += self.velocity
        self.rotation_angle += TAU/200
        
    def show(self):
        c_x, c_y, c_z = 0, 0, 0 #self.center
        v1 = PVector(c_x + self.side, c_y, c_z + self.side)
        v2 = PVector(c_x + self.side, c_y, c_z - self.side)
        v3 = PVector(c_x - self.side, c_y, c_z + self.side)
        v4 = PVector(c_x - self.side, c_y, c_z - self.side)
        
        v5 = PVector(c_x, c_y + self.height_scale * self.side, c_z)
        v6 = PVector(c_x, c_y - self.height_scale * self.side, c_z)
        
        faces = []
        faces.append(Triangle(v1, v5, v2))
        faces.append(Triangle(v1, v3, v5))
        faces.append(Triangle(v4, v5, v2))
        faces.append(Triangle(v4, v3, v5))
        
        faces.append(Triangle(v1, v6, v2))
        faces.append(Triangle(v1, v3, v6))
        faces.append(Triangle(v4, v6, v2))
        faces.append(Triangle(v4, v3, v6))
        
        pushMatrix()
        translate(self.center.x, self.center.y, self.center.z)
        rotateY(self.rotation_angle)
        for face in faces:
            face.show()
        popMatrix()
