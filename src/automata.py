import random
from abc import ABC, abstractmethod
from typing import Optional
from collections import defaultdict

class FastGrid:
    def __init__(self, width, height, fill: bool =False):
        self.width = width
        self.height = height
        self.data = [fill] * (width * height)

    def get(self, x, y):
        if 0 <= x < self.width and 0<= y < self.height:
            return self.data[y * self.width + x]

    def set(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.data[y * self.width + x] = value


    def __str__(self): 
        lines = []
        for y in range(self.height):
            line = ''.join(str(self.get(x, y)) for x in range(self.width))
            lines.append(line)
        return '\n'.join(lines)

class Automata(ABC):
    def create_grid(self):
        self.grid = FastGrid(self.width, self.height)

    def __init__(self, name: str, height: int, width: int, generations: int, initial_state: Optional[list] = None):
        self.name = name
        self.width = width
        self.height = height
        self.generations = generations
        self.initial_state = initial_state
        self.grid = None
        self.live_cells = set()
        self.create_grid()

    def set_initial_state(self):
        #'Block' 'Glider' 'Random' 'Single'
        if self.initial_state == 'Block':
            self.place_block()
        elif self.initial_state == 'Glider':
            self.place_glider()
        elif self.initial_state == 'Random':
            self.place_random()
        elif self.initial_state == 'Single':
            self.place_single()
        else:
            raise ValueError(f"Unknown state: {self.initial_state}")

    def update_grid(self, x, y, state: bool):
        if 0 <= x < self.width and 0 <= y < self.height:
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

    @abstractmethod
    def run_automata(self):
        pass

class Conways(Automata):
    def __init__(self, width, height, generations, initial_state=None):
        super().__init__('Conway', width, height, generations, initial_state)

    def run_automata(self):
        neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
        ]
            
        for generation in range(self.generations):
            dead_neighbor_counts = defaultdict(int)
            next_live_cells = set()

            for x, y in self.live_cells:
                live_neighbours = 0

                for dx, dy in neighbor_offsets:
                    nx = x + dx
                    ny = y + dy

                    if self.get_cell(nx, ny):
                        live_neighbours += 1
                    else:
                        dead_neighbor_counts[(nx, ny)] += 1 #Each time a live cell sees a dead neighbor, that dead neighbor’s count increases by 1.


                if live_neighbours in [2, 3]:
                    next_live_cells.add((x,y)) # Rules 1, 2, 3
                
            for (x, y), count in dead_neighbor_counts.items():
                if count == 3:  # Rule 4
                    next_live_cells.add((x, y))
            
            self.live_cells.clear()
            for x, y in self.live_cells:
                self.set_cell(x, y, False) #only clear cells that were alive


            for x, y in next_live_cells:
                self.update_grid(x, y, True)

            
        
