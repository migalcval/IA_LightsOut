import random
from py2pddl import Domain, create_type, predicate, action, goal, init

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
        effects = [self.on(cell)]
        return preconditions, effects

    @action(Cell)
    def set_off(self, cell):
        preconditions = [self.on(cell)]
        effects = [self.off(cell)]
        return preconditions, effects

class LightsOutBoardProblem(LightsOutBoardDomain):

    def __init__(self, rows=5, colums=5, randomize=False):
        self.size = (rows, colums)
        if randomize:
            self.board = [[random.choice([0, 1]) for _ in range(colums)] for _ in range(rows)]
        else:
            self.board = [[0 for _ in range(colums)] for _ in range(rows)]

    def toggle(self, i, j):
        if 0 <= i < self.size[0] and 0 <= j < self.size[1]:
            self.board[i][j] = 1 - self.board[i][j]

    def press(self, i, j):
        for x, y in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.toggle(i + x, j + y)

    def win(self):
        return all(cell == 1 for row in self.board for cell in row)

    def print_board(self):
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print()

#Test
if __name__ == "__main__":
    
    board = LightsOutBoardProblem(colums=7, randomize=False)
    print("Tablero inicial:")
    board.print_board()

    board.press(2, 2)
    board.print_board()
    board.press(2, 4)
    board.print_board()

    print("¿Tablero resuelto?:", board.win())
