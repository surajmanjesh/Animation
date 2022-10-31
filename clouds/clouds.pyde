add_library('peasycam')

clouds = []

class Cloudlet:
    def __init__(self, x, y, radius, completion_percentage):
        self.x = x
        self.y = y
        self.radius = radius
        self.cloud_brightness = 230 + noise(x, y) * 15    
        self.resolution = 30
        self.completion_percentage = int(completion_percentage * self.resolution / 100)
        
    
    def show(self):
        fill(self.cloud_brightness)
        noStroke()
        for i in range(2):
            pushMatrix()
            translate(self.x, self.y, 0)
            rotateX(PI * i)
            
            r = self.radius
            lon_divisions = TWO_PI / self.resolution
            lat_divisions = PI / self.resolution
            
            angle = self.completion_percentage * lat_divisions
            ellipse(0, 0, 2 * r * sin(angle), 2 * r * sin(angle))
            
            translate(0, 0, - r * cos(angle))
            
            beginShape(QUAD_STRIP)
            for i in range(self.resolution):
                for j in range(self.completion_percentage + 1):
                    a = i * lon_divisions
                    b = j * lat_divisions
                    
                    x1 = r * cos(a) * sin(b)
                    y1 = r * sin(a) * sin(b)
                    z1 = r * cos(b)
            
                    x2 = r * cos(a + lon_divisions) * sin(b)
                    y2 = r * sin(a + lon_divisions) * sin(b)
                            
                    vertex(x1, y1, z1)
                    vertex(x2, y2, z1)    
            endShape()
            popMatrix()
    

def setup():
    fullScreen(P3D)
    cam = PeasyCam(this, 700)
    
    cam.rotateX(-PI/2)
    radius = 50
    
    for x in range(-3, 1):
        for y in range(-1, 2):    
            clouds.append(Cloudlet(radius * x, radius * y, random(1, 2) * radius, random(40, 70)))
    
def draw():
    background(70, 100, 220)
    # lights()
    # directionalLight(200, 200, 200, 1, 1, 1)
    # directionalLight(255, 255, 255, 0, 0, -1)
    

    for c in clouds:
        c.show()
        
