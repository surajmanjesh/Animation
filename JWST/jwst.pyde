import math

add_library('peasycam')

tin_foil = None
milky_way = None
ticks = 0
last_ticks = 0
stars = []
UNIT = 0.5
STAR_COUNT = 3000
GOLD = (50, 91, 97)
DARK_GRAY = (0, 0, 10)
LIGHT_GRAY = (0, 0, 20)
GLOBAL_MAX_STAR_BRIGHTNESS = 0

class Star:
    SIZE = 4000 * UNIT
    MIN_BRIGHTNESS = 1
    MAX_BRIGHTNESS = 5
    
    def __init__(self):
        while True:
            self.x = random(-self.SIZE, self.SIZE)
            self.y = random(-self.SIZE, self.SIZE)
            self.z = random(-self.SIZE, self.SIZE)
            if self.x ** 2 + self.y ** 2 + self.z ** 2 > (0.9 * self.SIZE) ** 2:
                break
        self.b = random(self.MIN_BRIGHTNESS, self.MAX_BRIGHTNESS)
        # self.color = [color(207 + random(-10, 10), 53, 99), color(0, 0, 100), color(64 + random(-10, 10), 53, 99)][int(random(0, 3))]
        self.color = color(0, 0, 100)
        
    def show(self):
        pushMatrix()
        pushStyle()
        stroke(self.color)
        b = min(self.b, GLOBAL_MAX_STAR_BRIGHTNESS)
        strokeWeight(b)
        translate(self.x, self.y, self.z)
        point(0, 0, 0)
        # for i in range(8):
        #     spike_length = b - 3 if i in [3, 6] else b - 2
        #     strokeWeight(1) 
        #     line(0, 0, 0, 10 * spike_length * cos(i * PI / 4), 10 * spike_length * sin(i * PI / 4), 0) 
        popStyle()
        popMatrix()
                    
class HexagonTile:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
    
    def show(self):
        PI_BY_3 = PI / 3
        PI_BY_6 = PI / 6
        
        pushMatrix()
        translate(self.x, self.y, self.z)
        pushStyle()
        stroke(0, 0, 0)
        strokeWeight(1)
        fill(*GOLD)
        shininess(200)
        
        beginShape()
        for i in range(6):
            x = self.r * math.sin(PI_BY_3 * i - PI_BY_6) 
            y = self.r * math.cos(PI_BY_3 * i - PI_BY_6)
            vertex(x, y, 0)
        endShape(CLOSE)
        popStyle()
        
        pushStyle()
        fill(*DARK_GRAY)
        noStroke()
        beginShape()
        for i in range(6):
            vertex(self.r * 1.2 * math.sin(PI_BY_3 * i - PI_BY_6), self.r * 1.2 * math.cos(PI_BY_3 * i - PI_BY_6), 2)
        endShape(CLOSE)
        popStyle()
        popMatrix()

class Mirror:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        PI_BY_3 = math.pi / 3
        PI_BY_6 = math.pi / 6

        self.tiles = [HexagonTile(x=self.r * 0.87 * (1 - 0.13 * int(i % 2 == 1)) * math.sin(PI_BY_6 * i), 
                                  y=self.r * 0.87 * (1 - 0.13 * int(i % 2 == 1)) * math.cos(PI_BY_6 * i), 
                                  z=0, 
                                  r=self.r/4) for i in range(12)] 
        self.tiles.extend([HexagonTile(x=self.r/2 * 0.85 * math.sin(PI_BY_3 * i), 
                                       y=self.r/2 * 0.85 * math.cos(PI_BY_3 * i), 
                                       z=0, 
                                       r=self.r/4) for i in range(6)])
    
    def draw_support_arms(self):
        
        pushStyle()
        pushMatrix()
        
        strokeWeight(10)
        stroke(*DARK_GRAY)
        line(0, self.r * 1.125, 0, 0, self.r * 0.09, -self.r * 1.5)
        
        pushMatrix()
        rotateZ(math.pi * 0.875)
        line(0, self.r * 1.05, 0, 0, self.r * 0.09, -self.r * 1.5)
        
        rotateZ(math.pi * 0.25)
        line(0, self.r * 1.05, 0, 0, self.r * 0.09, -self.r * 1.5)
        popMatrix()
        
        popMatrix()
        popStyle()
        
    def draw_secondary_mirror(self):
        pushStyle()
        pushMatrix()
        stroke(0, 0, 0)
        strokeWeight(2)
        
        fill(*DARK_GRAY)
        translate(0, 0, -self.r * 1.5)
        circle(0, 0, self.r * 0.2)    
        
        fill(*GOLD)
        translate(0, 0, 1 * UNIT)
        circle(0, 0, self.r * 0.18)  
        
        fill(*DARK_GRAY)
        translate(0, 0, -3 * UNIT)
        beginShape()
        vertex(-0.05 * self.r, 0.20 * self.r, 0)
        vertex(-0.15 * self.r, 0, 0)
        vertex(-0.10 * self.r, -0.15 * self.r, 0)
        vertex(0.10 * self.r, -0.15 * self.r, 0)
        vertex(0.15 * self.r, 0, 0)
        vertex(0.05 * self.r, 0.20 * self.r, 0)
        endShape()
        popMatrix()
        popStyle()
    
    def draw_instrument_box(self):
        pushStyle()
        fill(*LIGHT_GRAY)
        rectMode(CENTER)
        pushMatrix()
        translate(0, 0.13 * self.r, 2)
        
        pushMatrix()
        translate(0, self.r/2, self.r / (2 * sqrt(2)))
        rotateX(-PI/4)
        rect(0, 0, self.r, self.r)  
        
        # Antenna
        pushStyle()
        strokeWeight(5)
        for i in [-1, 1]:
            line(i * 0.1 * self.r, 0, 0, i * 0.4 * self.r, 0, self.r)     
        popStyle() 
        popMatrix()
        
        fill(*DARK_GRAY)
        for i in [-1, 1]:
            x = i * 0.45 * self.r
            beginShape()
            vertex(x, self.r/2 + self.r/(2 * sqrt(2)), 0)
            vertex(x, self.r/2 - self.r/(2 * sqrt(2)), 0)
            vertex(x, self.r/2 - self.r/(2 * sqrt(2)), self.r/sqrt(2))
            endShape()

        pushMatrix()
        translate(0, -self.r / (2 * sqrt(2)) - self.r/4, self.r / (2 * sqrt(2)))
        box(0.9 * self.r, self.r * 1.5, self.r/sqrt(2))
        
        fill(*LIGHT_GRAY)
        pushMatrix()
        translate(self.r/4, -self.r/4, self.r/3)
        box(self.r/4, self.r/2, self.r/4)
        popMatrix()
        
        pushMatrix()
        translate(-self.r/4, -self.r/4, self.r/3)
        box(self.r/4, self.r/4, self.r/4)
        popMatrix()
        
        pushMatrix()
        translate(0, self.r/3, self.r/3)
        box(self.r/2)
        popMatrix()
        
        popMatrix()

        popMatrix()
        popStyle()
    
    def draw_receiver(self):
        pushStyle()
        pushMatrix()
        fill(*DARK_GRAY)
        circle(0, 0, 0.4 * self.r)
        
        box(0.18 * self.r, 0.18 * self.r, 0.7 * self.r)
        
        beginShape()
        z = -0.36 * self.r
        y = 0.10 * self.r
        vertex(-0.10 * self.r, y, z)
        vertex(-0.15 * self.r, -y, z)
        vertex(0.15 * self.r, -y, z)
        vertex(0.10 * self.r, y, z)
        endShape()
        
        popMatrix()
        popStyle()
        
    def show(self):
        pushMatrix()
        translate(self.x, self.y, self.z)
        for tile in self.tiles:
            tile.show()
        self.draw_receiver()
        self.draw_support_arms()
        self.draw_secondary_mirror()
        self.draw_instrument_box()        
        popMatrix()


class SolarShield:
    def __init__(self, x, y, z, l, w):
        self.x = x
        self.y = y
        self.z = z
        self.l = l
        self.w = w
    
    def show(self):
        # Foil shields
        pushMatrix()
        translate(self.x, self.y, self.z)
        pushStyle()
        stroke(0, 0, 0)
        
        beginShape()
        texture(tin_foil)
        textureMode(NORMAL)
        vertex(0.1 * self.w, 0.1 * self.w, -self.l, 0, 0)
        vertex(self.w, 0, -0.1 * self.l, 0, 0.4)
        vertex(self.w, 0, 0.1 * self.l, 0, 0.6)
        vertex(0.1 * self.w, 0.1 * self.w, self.l, 0, 1)
        
        vertex(-0.1 * self.w, 0.1 * self.w, self.l, 1, 1)
        vertex(-self.w, 0, 0.1 * self.l, 0.6, 1)
        vertex(-self.w, 0, -0.1 * self.l, 0.4, 1)
        vertex(-0.1 * self.w, 0.1 * self.w, -self.l, 1, 0)
        endShape(CLOSE)
        popStyle()
        popMatrix()

class JWST:
    def __init__(self):
        self.l = 700 * UNIT
        self.w = 460 * UNIT
        self.mirror = Mirror(x=0, y=0, z=0, r=200 * UNIT)
        self.shields = [SolarShield(x=0, y=(-250 - 20 * i) * UNIT, z=0, l=self.l, w=self.w) for i in range(5)]

    def draw_shield_support(self):
        pushStyle()
        stroke(*DARK_GRAY)
        strokeWeight(5)
        y1 = -250 * UNIT
        y2 = -330 * UNIT
        line(0.1 * self.w, y1 + 0.1 * self.w, -self.l, 
               0.1 * self.w, y2 + 0.1 * self.w, -self.l)
        line(self.w, y1, -0.1 * self.l,
               self.w, y2, -0.1 * self.l)
        line(self.w, y1, 0.1 * self.l,
               self.w, y2, 0.1 * self.l)
        line(0.1 * self.w, y1 + 0.1 * self.w, self.l,
               0.1 * self.w, y2 + 0.1 * self.w, self.l)
        line(-0.1 * self.w, y1 + 0.1 * self.w, self.l,
               -0.1 * self.w, y2 + 0.1 * self.w, self.l)
        line(-self.w, y1, 0.1 * self.l,
               -self.w, y2, 0.1 * self.l)
        line(-self.w, y1, -0.1 * self.l,
               -self.w, y2, -0.1 * self.l)
        line(-0.1 * self.w, y1 + 0.1 * self.w, -self.l,
             -0.1 * self.w, y2 + 0.1 * self.w, -self.l)
        
        popStyle()
        
    def show(self):
        for shield in self.shields:
            shield.show()                                                                                                                            
        self.mirror.show()
        
        self.draw_shield_support()
                                                                                                                                                                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                                                                                        
def setup():
    # fullScreen(P3D)
    size(1720, 900, P3D)
    # size(800, 534, P3D)
    cam = PeasyCam(this, 1500)
    cam.rotateX(PI/32)

    colorMode(HSB, 360, 100, 100, 100)
    global stars, tin_foil, milky_way
    stars = [Star() for _ in range(STAR_COUNT)]
    tin_foil = loadImage('gray-background-gradient-abstract-silver-600nw-724372420.jpg')

def draw():
    global ticks, last_ticks, GLOBAL_MAX_STAR_BRIGHTNESS, UNIT
    
    WHITE = color(0, 0, 100)
    BLACK = color(190, 30, 0)
    
    ROTATION_FACTOR = 2 * PI
    TICK_FACTOR = 0.02
    ROTATION_ANIMATION_STOP = 3.0625 * ROTATION_FACTOR
    ROTATE_ANIMATION = True
    
    # Start with box for 1st rotation
    # Transition to space with sped up animation in 2nd rotation - Fade out box and fade in stars
    # Show JWST in space for 3rd rotation
    # Stop rotating at 3 and 1/8th rotation and zoom out
    if ticks < ROTATION_FACTOR:
        tick_increment = TICK_FACTOR 
        GLOBAL_MAX_STAR_BRIGHTNESS = 0
        SHOW_BOX = True
        UNIT = 0.7
        box_color = WHITE
    elif ticks < 2 * ROTATION_FACTOR:
        MAX_TICK_FACTOR = 3
        if ticks < 1.25 * ROTATION_FACTOR:
            tick_increment = lerp(1 * TICK_FACTOR, MAX_TICK_FACTOR * TICK_FACTOR, (ticks - ROTATION_FACTOR)/(ROTATION_FACTOR/4))
        elif ticks > 1.75 * ROTATION_FACTOR :
            tick_increment = lerp(MAX_TICK_FACTOR * TICK_FACTOR, 0.5 * TICK_FACTOR, (ticks - (1.75 * ROTATION_FACTOR))/(ROTATION_FACTOR/4))
        else: 
            tick_increment = MAX_TICK_FACTOR * TICK_FACTOR
        
        SHOW_BOX = True
        interpolation_value = (ticks - ROTATION_FACTOR)/ROTATION_FACTOR
        GLOBAL_MAX_STAR_BRIGHTNESS = int(lerp(0, 6, interpolation_value))
        UNIT = lerp(0.7, 1, interpolation_value)
        box_color = lerpColor(WHITE, color(0, 0, 100, 0), interpolation_value)
    else: 
        tick_increment = 0.5 * TICK_FACTOR 
        GLOBAL_MAX_STAR_BRIGHTNESS = 5
        SHOW_BOX = False
        UNIT = 1
        
        if ticks > ROTATION_ANIMATION_STOP:
            UNIT = max(0.4, lerp(1, 0.4, (ticks - ROTATION_ANIMATION_STOP)/(ROTATION_FACTOR/2)))
            ROTATE_ANIMATION = False
    
    lights()
    rotateX(PI)
    background(BLACK)
    ticks += tick_increment
    
    pushMatrix()
    rotateX(ticks/10)    
    for star in stars:
        star.show()
    popMatrix()
    
    pushMatrix()
    if SHOW_BOX: 
        pushStyle()
        stroke(BLACK)
        fill(box_color)
        rotateY(PI/4)
        box(6000)
        popStyle()
    popMatrix()
    
    if ROTATE_ANIMATION:
        rotateY(ticks)
        last_ticks = ticks
    else: 
        rotateY(last_ticks)
    
    rotateZ(-PI/16)
        
    JWST().show()
    
    SAVE_FRAMES = 0
    if SAVE_FRAMES:
        if ticks > ROTATION_ANIMATION_STOP + 1.125 * ROTATION_FACTOR:
            exit()
        saveFrame("images/jwst-######.tiff") 
