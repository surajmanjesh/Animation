CELLS = {}

BOX_SIZE = 5
MAX_AGE = 1000
WRAP_AROUND = False
IMMORTALITY= True
SAVE_FRAMES = False

class Cell:
    def __init__(self, x, y, alive):
        self.x = x
        self.y = y
        self.age = MAX_AGE / 2
        self.was_alive = alive
        self.is_alive = alive
        self.neighbours = []
        for dx in [-BOX_SIZE, 0, BOX_SIZE]:
            for dy in [-BOX_SIZE, 0, BOX_SIZE]:
                if dx == 0 and dy == 0:
                    continue
                if WRAP_AROUND:
                    self.neighbours.append(((x + dx)%width, (y + dy)%height))
                else:
                    self.neighbours.append((x + dx, y + dy))

    def draw(self):
        stroke(24)
        # noStroke()
        if self.is_alive:
            fill(self.age % MAX_AGE, 100, 100 - 0 * (self.age // MAX_AGE))
        else: 
            fill(0, 0, 0)
        rect(self.x, self.y, BOX_SIZE, BOX_SIZE)

    def update(self):
        alive_neighbour_count = sum([int(CELLS[coordinate].was_alive) for coordinate in self.neighbours if CELLS.get(coordinate) is not None])
        self.is_alive = (self.was_alive and alive_neighbour_count in [2, 3]) or (not self.was_alive and alive_neighbour_count in [3])
        
        if self.is_alive:
            self.age += 10
        else:
            self.age = MAX_AGE / 2
        
        if not IMMORTALITY and self.age > MAX_AGE:
            self.is_alive = False


def setup():
    # fullScreen()
    size(1200, 600)
    
    # frameRate(10)
    colorMode(HSB, MAX_AGE, 100, 100)
    background(0, 0, 0)
    global CELLS
    
    alive_function = lambda x, y: random(0, 10) < 3.14159
    # alive_function = lambda x, y: noise(y) > 0.3
    
    for x in range(0, width + BOX_SIZE, BOX_SIZE):
        for y in range(0, height + BOX_SIZE, BOX_SIZE):
            CELLS[(x, y)] = Cell(x, y, alive_function(x, y))
        
def draw():
    global CELLS
    for c in CELLS.values():
        c.draw()
        c.update()
    
    for c in CELLS.values():
        c.was_alive = c.is_alive
    
    if SAVE_FRAMES:
        saveFrame('images/image-######.tif')
