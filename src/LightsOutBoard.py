import random
from py2pddl import Domain, create_type, predicate, action, goal, init, Not

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

    @action(Cell)
    def set_on(self, cell):
        preconditions = [self.off(cell)]
        effects = [self.on(cell), Not(self.off(cell))]
        """ Not(self.off(cell)) ensures that the cell is not off after setting it on """
        adjacent_on_effects = [self.on(adj_cell), ~self.off(adj_cell)
            for adj_cell in self.board if self.adjacent(cell, adj_cell) and self.off(adj_cell)]
        adjacent_off_effects = [self.off(adj_cell), Not(self.on(adj_cell))
            for adj_cell in self.board if self.adjacent(cell, adj_cell) and self.on(adj_cell)]
        effects.extend(adjacent_on_effects)
        effects.extend(adjacent_off_effects)
        return preconditions, effects

    @action(Cell)
    def set_off(self, cell):
        preconditions = [self.on(cell)]
        effects = [self.off(cell), Not(self.on(cell))]
        """ Not(self.on(cell)) ensures that the cell is not on after setting it off """
        adjacent_on_effects = [self.on(adj_cell), Not(self.off(adj_cell))
            for adj_cell in self.board if self.adjacent(cell, adj_cell) and self.off(adj_cell)]
        adjacent_off_effects = [self.off(adj_cell), Not(self.on(adj_cell))
            for adj_cell in self.board if self.adjacent(cell, adj_cell) and self.on(adj_cell)]
        effects.extend(adjacent_on_effects)
        effects.extend(adjacent_off_effects)
        return preconditions, effects

class LightsOutBoardProblem(LightsOutBoardDomain):

    def __init__(self, rows=5, colums=5, randomize=False):
        self.size = (rows, colums)
        self.randomize = randomize
        self.board = LightsOutBoardDomain.Cell.create_objects([
            (f"c{i}-{j}", LightsOutBoardDomain.Cell) for i in range(rows) for j in range(colums)
        ])
    
    @init
    def init(self):
        for cell in self.board:
            if self.randomize:
                self.board[cell] = random.choice([0, 1])
            else:
                self.board[cell] = 0
        return [self.off(self.board[cell]) for cell in self.board if self.board[cell] == 0,
                self.on(self.board[cell]) for cell in self.board if self.board[cell] == 1,
                self.adjacent(self.board[f"c{i}-{j}"], self.board[f"c{i + 1}-{j}"]) for i in range(self.size[0]-1) for j in range(self.size[1]),
                self.adjacent(self.board[f"c{i}-{j}"], self.board[f"c{i}-{j + 1}"]) for i in range(self.size[0]) for j in range(self.size[1]-1),
                self.adjacent(self.board[f"c{i}-{j}"], self.board[f"c{i - 1}-{j}"]) for i in range(1, self.size[0]) for j in range(self.size[1]),
                self.adjacent(self.board[f"c{i}-{j}"], self.board[f"c{i}-{j - 1}"]) for i in range(self.size[0]) for j in range(1, self.size[1])]

    @goal
    def goal(self):
        return [self.on(self.board[cell]) for cell in self.board]

    # def toggle(self, i, j):
    #     if 0 <= i < self.size[0] and 0 <= j < self.size[1]:
    #         self.board[i][j] = 1 - self.board[i][j]

    # def press(self, i, j):
    #     for x, y in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
    #         self.toggle(i + x, j + y)

    # def win(self):
    #     return all(cell == 1 for row in self.board for cell in row)

    # def print_board(self):
    #     for row in self.board:
    #         print(" ".join(str(cell) for cell in row))
    #     print()

"""Test"""
if __name__ == "__main__":

    !pyperplan -H hmax -s astar dominio_mundo_bloques.pddl problema_mundo_bloques.pddl
    
#     board = LightsOutBoardProblem(colums=7, randomize=False)
#     print("Tablero inicial:")
#     board.print_board()

#     board.press(2, 2)
#     board.print_board()
#     board.press(2, 4)
#     board.print_board()

#     print("¿Tablero resuelto?:", board.win())
