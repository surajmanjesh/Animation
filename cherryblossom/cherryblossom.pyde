add_library('peasycam')

trees = []
clouds = []
stars = []
grass_blades = []

NIGHT = not True

tick = 0

def setup():
    fullScreen(P3D)
    # size(1720, 900, P3D)
    cam = PeasyCam(this, 1000)
    cam.rotateX(PI/32)

    
    colorMode(HSB, 360, 100, 100, 100)
    global trees, clouds, stars, grass_blades
    trees = [Tree(130, 0, -800), Tree(-160, 0, -750), 
             # Tree(230, 0, -600), Tree(-300, 0, -550), 
             Tree(190, 0, -450), Tree(-150, 0, -480), 
             # Tree(250, 0, -320), Tree(-270, 0, -370), 
             Tree(130, 0, -200), Tree(-200, 0, -250), 
             Tree(170, 0, -100), Tree(-280, 0, -160), 
             Tree(240, 0, 0), Tree(-180, 0, 20),
             # Tree(180, 0, 100), Tree(-180, 0, 160),
             Tree(120, 0, 200), Tree(-220, 0, 230)]
    
    for x in range(-500, 500, 10):
        if x in range(-80, 100):
                continue
        for z in range(-900, 0, 20):
            grass_blades.append(Grass(x + random(-10, 10), 0, z + random(-10, 10), random(30, 60)))
    
    for x in range(-3000, 3000, 900):
        clouds.append(Cloud(x + random(-300, 300), random(500, 1000), random(700, 1800), random(30, 70)))

    stars = [((random(-3000, 3000), random(400, 1500), 2000), random(1, 4)) for i in range(100)]
    
    
def draw_stars(global_brightness):
    stroke(0, 0, 100)
    for p, b in stars:
        if b < global_brightness:
            continue
        strokeWeight(max(0, b - global_brightness + random(0, 1)))
        point(*p)
    
def draw_ground():
    noStroke()
    SIZE = 2000
    DELTA = 80
    RISE = -40
    createShape()
    beginShape(QUAD)
    fill(117, 86, 67)
    vertex(-10 * SIZE, RISE - 10, -10 * SIZE)
    vertex(-10 * SIZE, RISE - 10, 10 * SIZE)
    vertex(10 * SIZE, RISE - 10, 10 * SIZE)
    vertex(10 * SIZE, RISE - 10, -10 * SIZE)
    endShape()
    
    createShape()
    beginShape(QUAD)
    for x in range(-SIZE, SIZE, DELTA):
        for z in range(-SIZE, SIZE, DELTA):
            fill(117 + 20 * noise(x, z), 76 + 25 * noise(x, z), 50 + 25 * noise(x, z))
            
            vertex(x, RISE * noise(x, z), z)
            vertex(x, RISE * noise(x, z + DELTA), z + DELTA)
            vertex(x + DELTA, RISE * noise(x + DELTA, z + DELTA), z + DELTA)
            vertex(x + DELTA, RISE * noise(x + DELTA, z), z)
    endShape()

def draw_mountains():
    for H, R, C_X, C_Z in [[650, 900, -1000, 1200], [700, 1000, 0, 1300], [600, 1100, 1000, 1400]]:
        H_DELTA = 50
        THETA_DIVISIONS = 200
        THETA_DELTA = 2 * PI/THETA_DIVISIONS
        ROUGHNESS = 100
        noStroke()
        createShape()
        beginShape(QUAD)
        for y in range(0, H, H_DELTA):
            R1 = R * (1.0 - (float(y)/H))
            R2 = R * (1.0 - (float(y + H_DELTA)/H))
            for i in range(THETA_DIVISIONS + 1):
                THETA1 = i * THETA_DELTA
                THETA2 = (i+1) * THETA_DELTA
                fill(237, 70 - 60 * float(y)/H - 10 * noise(y), 30 + 65 * float(y)/H + 5 * noise(y))
                x1 = C_X + R1 * cos(THETA1)
                x2 = C_X + R1 * cos(THETA2)
                x3 = C_X + R2 * cos(THETA2)
                x4 = C_X + R2 * cos(THETA1)
                z1 = C_Z + R1 * sin(THETA1)
                z2 = C_Z + R1 * sin(THETA2)
                z3 = C_Z + R2 * sin(THETA2)
                z4 = C_Z + R2 * sin(THETA1)
                vertex(x1 + ROUGHNESS * noise(x1, z1), y + 0.5 * ROUGHNESS * noise(x1, z1), z1 + ROUGHNESS * noise(x1, z1))
                vertex(x2 + ROUGHNESS * noise(x2, z2), y + 0.5 * ROUGHNESS * noise(x2, z2), z2 + ROUGHNESS * noise(x2, z2))
                vertex(x3 + ROUGHNESS * noise(x3, z3), y + H_DELTA + 0.5 * ROUGHNESS * noise(x3, z3), z3 + ROUGHNESS * noise(x3, z3))
                vertex(x4 + ROUGHNESS * noise(x4, z4), y + H_DELTA + 0.5 * ROUGHNESS * noise(x4, z4), z4 + ROUGHNESS * noise(x4, z4))
        endShape()
        


class Branch:
    def __init__(self, x1, y1, z1, x2, y2, z2, level, max_level):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.level = level
        self.max_level = max_level
        self.leaves = self.generate_leaves() if level <= max_level - 1 else []
    
    def generate_leaves(self):
        leaves = []
        SIZE = 1.5
        x, y, z = self.x2, self.y2, self.z2
        for i in range(int(random(6, 12))):
            leaves.append([(x, y, z), (x + SIZE, y + SIZE, z), (x, y + 3 * SIZE, z), (x - 1.5 * SIZE, y + 2 * SIZE, z)])
        
        return leaves
        
    def show(self):
        if self.level in [0, 1]:
            strokeWeight(2 * (self.max_level - self.level - 1))
        else: 
            strokeWeight(self.max_level - self.level - 1)
            
        stroke(27, 70, 55, 100 * (1 - float(self.level)/self.max_level))
        line(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)
        
        if not self.leaves:
            return 
        
        noStroke()
        for leaf in self.leaves:
            fill(337 + 5 * sin(tick) + 20 * noise(leaf[0][0]), 
             40 + 5 * sin(tick) + 20 * noise(leaf[0][1]), 
             70 + 5 * sin(tick) + 20 * noise(leaf[0][2]))
        
            createShape()
            beginShape(QUAD)
            for x, y, z in leaf:
                vertex(x, y, z  + random(-2, 2))
            endShape()

class Tree:
    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.max_level = 4  
        self.branches = [Branch(self.X, self.Y, self.Z, self.X, self.Y + 80, self.Z, 0, self.max_level)]
        self.branches.extend(self.generate_branches((self.X, self.Y + 80, self.Z), level=1))
    
    def generate_branches(self, previous_point, level):
        if level >= self.max_level:
            return []
        branches = []
        ratio = (1 - 0.5 * (float(level)/self.max_level))
        x1, y1, z1 = previous_point
        multiplier = 1.5 if z1 < -500 else 1
        SIZE = 30 * multiplier
        for i in range(int(multiplier * level)):
            x2 = x1 + random(-SIZE * ratio, 0)
            y2 = y1 + random(-5, SIZE * ratio)
            z2 = z1 + random(-SIZE * ratio, 0)
            branches.append(Branch(x1, y1, z1, x2, y2, z2, level, self.max_level))
            branches.extend(self.generate_branches((x2, y2, z2), level+1))
            
            x2 = x1 + random(0, SIZE * ratio)
            y2 = y1 + random(-5, SIZE * ratio)
            z2 = z1 + random(0, SIZE * ratio)
            branches.append(Branch(x1, y1, z1, x2, y2, z2, level, self.max_level))
            branches.extend(self.generate_branches((x2, y2, z2), level+1))
            
            
            x2 = x1 + random(0, SIZE * ratio)
            y2 = y1 + random(-5, SIZE * ratio)
            z2 = z1 + random(-SIZE * ratio, 0)
            branches.append(Branch(x1, y1, z1, x2, y2, z2, level, self.max_level))
            branches.extend(self.generate_branches((x2, y2, z2), level+1))
            
            
            x2 = x1 + random(-SIZE * ratio, 0)
            y2 = y1 + random(-5, SIZE * ratio)
            z2 = z1 + random(0, SIZE * ratio)
            branches.append(Branch(x1, y1, z1, x2, y2, z2, level, self.max_level))
            branches.extend(self.generate_branches((x2, y2, z2), level+1))
            
            
        return branches
    
    def show(self):
        for branch in self.branches:
            branch.show()


def draw_river():
    THETA_DIVISIONS = 40
    MAX_THETA = 6 * PI
    THETA_DELTA = MAX_THETA/THETA_DIVISIONS
    ROUGHNESS = 100
    A = 80
    B = 90
    WIDTH = 100
    
    bright = 85
    
    fill(210 + random(-1, 1), 90 + random(-1, 1), bright)
    noStroke()
    createShape()
    beginShape()
    theta = -MAX_THETA
    while theta <= MAX_THETA:
        x = A * cos(theta) - WIDTH
        z = B * theta
        vertex(x, 0, z)
        theta += THETA_DELTA
    
    while theta >= -MAX_THETA:
        x = A * cos(theta) + WIDTH
        z = B * theta
        vertex(x, 0, z)
        theta -= THETA_DELTA
    
    endShape()
    
    strokeWeight(1)
        
    for w in range(1, 3):
        createShape()
        beginShape(LINES)
        
        stroke(190 + random(-10, 10), 50 + random(-20, 20), bright + 15)
    
        theta = -MAX_THETA
        while theta <= MAX_THETA:
            x = A * cos(theta) + 20 * w + random(-10, 0)
            z = B * theta + random(-10, 10)
            vertex(x, 0, z)
            theta += THETA_DELTA
        
        while theta >= -MAX_THETA:
            x = A * cos(theta) - 20 * w + random(0, 10)
            z = B * theta + random(-10, 10)
            vertex(x, 0, z)
            theta -= THETA_DELTA
                
        endShape()
    
class Grass:
    def __init__(self, x, y, z, h):
        self.x = x
        self.y = y
        self.z = z
        self.h = h
    
    def show(self):
        stroke(107, 80,75)
        strokeWeight(2)
        noFill()
        pushMatrix()
        translate(self.x, self.y, self.z)
        arc(self.x, self.y, self.h, 3 * self.h + random(-30, 30), PI - PI/5, PI)
        popMatrix()
        
class Cloud:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.offsets = [(random(0, 2 * r), 
                         random(0, r), 
                         random(0, 2 * r), 
                         random(0.65 * r, 1.2 * r), 
                         random(75, 100), 
                         random(1.3, 1.7), 
                         random(0.9, 1.1), 
                         random(0.5, 0.8)) for i in range(int(random(3, 5)))] 
        self.offsets += [(random(-2 * r, 0), 
                         random(0, r), 
                         random(-2 * r, 0), 
                         random(0.65 * r, 1.2 * r), 
                         random(75, 100), 
                         random(1.3, 1.7), 
                         random(0.9, 1.1), 
                         random(0.5, 0.8)) for i in range(int(random(3, 5)))] 

    def show(self):
        for dx, dy, dz, dr, b, sx, sy, sz in self.offsets:
            fill(180, 40, b)
            noStroke()
            pushMatrix()
        
            translate(self.x + dx - 50 * tick, self.y + dy, self.z + dz)
            scale(sx, sy, sz)
            sphere(self.r + dr)
            popMatrix()
        
        
def draw():
    global tick
    
    # global_brightness = 50 + 50 * cos(tick)
    
    # background_hues = [(190, 100, 100), (190, 70, 100), (190, 30, 100),
    #                    (305, 34, 95), (305, 34, 95), (305, 34, 95), (305, 34, 95), 
    #                    (190, 30, 20), (190, 30, 0), (190, 30, 0), (190, 30, 0)]
    # background(*background_hues[int(global_brightness//10)])
    # background(190, global_brightness, global_brightness)
    
    tick += 0.2
    if NIGHT: 
        background(190, 30, 0)
    else: 
        background_hues = [(190, 100, 100), (190, 70, 100), (190, 30, 100)]
        # background(*background_hues[int(tick)%(len(background_hues))])
        background(*background_hues[0])
        
    lights()
    rotateX(PI)
    ambientLight(200, 0, 100, 0, 1, 0)
    sphereDetail(12)
    
    draw_ground()
    draw_river()
    draw_mountains()
    
    for cloud in clouds: 
        cloud.show()
    
    for tree in trees: 
        tree.show()
    
    for grass_blade in grass_blades:
        grass_blade.show()
    
    if NIGHT:
        draw_stars(0)
    
    var = 'night' if NIGHT else 'day'
    saveFrame('cherry_blossoms_' + var + '/img_#####.tiff')
