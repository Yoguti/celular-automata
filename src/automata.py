import random
from abc import ABC, abstractmethod
from typing import Optional

class FastGrid:
    def __init__(self, width, height, fill: bool =False):
        self.width = width
        self.height = height
        self.data = [fill] * (width * height)

    def get(self, x, y):
        if 0 <= x < self.width and 0<= y < self.height:
            return self.data[y * self.width + x]

    def set(self, x, y, value):
        self.data[y * self.width + x] = value

    def __str__(self): 
        lines = []
        for y in range(self.height):
            line = ''.join(str(self.get(x, y)) for x in range(self.width))
            lines.append(line)
        return '\n'.join(lines)

class Automata(ABC):
    def __init__(self, name: str, height: int, width: int, generations: int, initial_state: Optional[list] = None):
        self.name = name
        self.width = width
        self.height = height
        self.generations = generations
        self.state = initial_state
        self.grid = None
        self.live_cells = set()
        self.live_cells_neighbours = dict()

    def create_grid(self):
        self.grid = FastGrid(self.width, self.height)

    def set_initial_state(self):
        #'Block' 'Glider' 'Random' 'Single'
        if self.state == 'Block':
            self.place_block()
        elif self.state == 'Glider':
            self.place_glider()
        elif self.state == 'Random':
            self.place_random()
        elif self.state == 'Single':
            self.place_single()
        else:
            raise ValueError(f"Unknown state: {self.state}")

    def update_grid(self, x, y, state: bool):
        self.grid.set(x, y, state)
        cell = (x,y)
        if state:
            self.live_cells.add(cell)
        else:
            self.live_cells.discard(cell)
           

    def get_cell(self, x, y):
        return self.grid.get(x,y)

    def place_block(self):
        hw = self.width // 2
        hh = self.height // 2
        
        for y in range (-1,2):
            for x in range (-1,2):
                self.update_grid(hh + x, hw +y, True)
    
    def place_glider(self):
        cx = self.width // 2
        cy = self.height // 2

        self.update_grid(cx + 1, cy,     True)
        self.update_grid(cx + 2, cy + 1, True)
        self.update_grid(cx,     cy + 2, True)
        self.update_grid(cx + 1, cy + 2, True)
        self.update_grid(cx + 2, cy + 2, True)
      
    def place_random(self):
        life_max = random.randint(0, (self.width * self.height) - 1)

        for life in range(life_max):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.update_grid(x, y, True)
    
    def place_single(self):
        cx = self.width // 2
        cy = self.height // 2
        self.update_grid(cx, cy, True)

    def count_neighbours(self):
        neighbours_list = []  # List of lists for each cell's neighbors
        neighbor_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for cell in self.live_cells:
            neighbours = []  # List for neighbors of the current cell
            for row_offset, col_offset in neighbor_offsets:
                neighbour = self.grid.get(cell[0] + row_offset, cell[1] + col_offset)
                # Keep all neighbors, including None for out-of-bounds (mantains same lenght to avoid storing coords)
                neighbours.append(neighbour)
            neighbours_list.append(neighbours)
            
        return neighbours_list

    def build_neighbours_dict(self):
        neighbours = self.count_neighbours(self)
        pass

    @abstractmethod
    def run_automata(self):
        pass



class Conways(Automata):
    def __init__(self, width, height, generations, initial_state=None):
        super().__init__('Conway', width, height, generations, initial_state)

    def run_automata(self):
        pass

