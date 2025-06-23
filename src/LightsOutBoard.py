import random
from py2pddl import Domain, action, create_type, goal, init, predicate

class LightsOutBoardDomain(Domain):

    Object = create_type("Object")
    Cell = create_type("Cell", Object)

    @predicate(Cell)
    def on(self, cell):
        """Represents if a cell is on"""

    @predicate(Cell)
    def off(self, cell):
        """Represents if a cell is off"""

    @predicate(Cell)
    def adjacent(self, cell1, cell2):
        """Represents if two cells are adjacent"""

class LightsOutBoardProblem(LightsOutBoardDomain):

    #------------------------ Initialize the board with a given size or a random state ------------------------#
    def __init__(self, rows=5, columns=5, randomize=False):
        self.size = (rows, columns)
        self.randomize = randomize
        self.cells = [self.Cell(f"c{i}-{j}") for i in range(rows) for j in range(columns)]
        self.cell_map = {f"c{i}-{j}": cell for i in range(rows) for j in range(columns) 
                        for cell in self.cells if str(cell) == f"c{i}-{j}"}

    #------------------------ Define the action to turn on a cell ------------------------#
    @action(LightsOutBoardDomain.Cell)
    def set_on(self, cell):
        preconditions = [self.off(cell)]
        effects = [self.on(cell), ~self.off(cell)]
        
        for adj_cell in self.cells:
            if self.adjacent(cell, adj_cell) in self.init():
                if self.off(adj_cell) in self.init():
                    effects.extend([self.on(adj_cell), ~self.off(adj_cell)])
                elif self.on(adj_cell) in self.init():
                    effects.extend([self.off(adj_cell), ~self.on(adj_cell)])
        return preconditions, effects

    #------------------------ Define the action to turn off a cell ------------------------#
    @action(LightsOutBoardDomain.Cell)
    def set_off(self, cell):
        preconditions = [self.on(cell)]
        effects = [self.off(cell), ~self.on(cell)]
        
        for adj_cell in self.cells:
            if self.adjacent(cell, adj_cell) in self.init():
                if self.off(adj_cell) in self.init():
                    effects.extend([self.on(adj_cell), ~self.off(adj_cell)])
                elif self.on(adj_cell) in self.init():
                    effects.extend([self.off(adj_cell), ~self.on(adj_cell)])
        return preconditions, effects
    
    #----------------------- Define the initial state ------------------------#
    @init
    def init(self):
        initial_state = []
        rows, cols = self.size
        
        # Add adjacency relationships
        for i in range(rows):
            for j in range(cols):
                current = self.cell_map[f"c{i}-{j}"]
                if i > 0:
                    initial_state.append(self.adjacent(current, self.cell_map[f"c{i-1}-{j}"]))
                if i < rows-1:
                    initial_state.append(self.adjacent(current, self.cell_map[f"c{i+1}-{j}"]))
                if j > 0:
                    initial_state.append(self.adjacent(current, self.cell_map[f"c{i}-{j-1}"]))
                if j < cols-1:
                    initial_state.append(self.adjacent(current, self.cell_map[f"c{i}-{j+1}"]))
                
                # Initial cell states
                if self.randomize:
                    initial_state.append(
                        self.on(current) if random.choice([True, False]) 
                        else self.off(current)
                    )
                else:
                    initial_state.append(self.off(current))
        
        return initial_state

    #------------------------ Define the goal state ------------------------#
    @goal
    def goal(self):
        return [self.on(cell) for cell in self.cells]

#------------------------ Generate PDDL files ------------------------#
if __name__ == "__main__":
    domain = LightsOutBoardDomain()
    problem = LightsOutBoardProblem(rows=3, columns=3, randomize=True)
    
    domain.generate_domain_pddl(filename="dominio_lightsout")
    problem.generate_problem_pddl(filename="problema_lightsout")

    #pyperplan -H hmax -s astar dominio_lightsout.pddl problema_lightsout.pddl