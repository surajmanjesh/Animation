add_library('peasycam')

class Particle:
    def __init__(self, position=None, velocity=None):
        self.position = position or random(50, 100) * PVector.random3D()
        self.velocity = velocity or PVector.random3D()

    def move(self):
        self.position += self.velocity/5
   
    def show(self):
        vertex(self.position.x, self.position.y, self.position.z) 

    
particles = []
tick = 0
        
def setup():
    fullScreen(P3D)
    # size(800, 600, P3D)
    colorMode(HSB, 100, 100, 100, 100)
    cam = PeasyCam(this, 700)
    for _ in range(50):
        particles.append(Particle())    
    
def draw():
    global tick
    background(70, 100, 220)
    strokeWeight(4)
    rotateY(radians(tick/2.0))
    # beginShape(POINTS)
    beginShape(TRIANGLE_STRIP)
    fill(tick%100, 100, 100)
    # stroke(tick%100, 100, 100)
    for particle in particles: 
        particle.move()
        particle.show()
    endShape()
    tick += 1
    
    saveFrame('abstract/img_#####.tiff')
