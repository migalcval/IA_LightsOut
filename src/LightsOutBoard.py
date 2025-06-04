import random
from py2pddl import Domain, create_type, predicate, action

class LightsOutBoardDomain(Domain):

    Object = create_type("Object")
    Cell = create_type("Cell", Object)

    @predicate(Cell)
    def on(self, cell):
        """Represents if a cell is on"""

    @predicate(Cell)
    def off(self, cell):
        """Represents if a cell is off"""

    """ Estoy liado con esto """
    # @action(Cell)
    # def set_on(self, cell):
    #     preconditions = [self.off(cell)]
    #     effects = [self.on(cell)]

    # @action(Cell)
    # def set_off(self, cell):
    #     preconditions = [self.on(cell)]
    #     effects = [self.off(cell)]

    
    def __init__(self, size=5, randomize=False):
        self.size = size
        if randomize:
            self.board = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]
        else:
            self.board = [[0 for _ in range(size)] for _ in range(size)]

    def toggle(self, i, j):
        if 0 <= i < self.size and 0 <= j < self.size:
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
    
    board = LightsOutBoard(size=5, randomize=False)
    print("Tablero inicial:")
    board.print_board()

    board.press(2, 2)
    board.print_board()
    board.press(2, 4)
    board.print_board()

    print("¿Tablero resuelto?:", board.win())
