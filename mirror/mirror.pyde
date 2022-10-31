add_library('peasycam')
    
def mirror():
    loadPixels()
    for x in range(width/2):
        for y in range(height):
            # pixels[width*y + width - x - 1] = pixels[width*y + x] 
            if False and pixels[width * y + x] == -8355712:   
                pixels[width*y + width - x - 1] = 0x2030CF
            else:
                pixels[width*y + width - x - 1] = ~pixels[width*y + x]
    updatePixels()
    

def setup():
    # fullScreen(P3D)
    size(400, 400, P3D)
    cam = PeasyCam(this, 700)
    
    
def draw():
    # background(128, 128, 128)
    background(0)

    noStroke()
    
    translate(0, -300, 0)
    fill(255, 40, 50)
    sphere(50)
    
    translate(-300, 0, 0)
    fill(40, 255, 50)
    sphere(50)
    
    mirror()
    
