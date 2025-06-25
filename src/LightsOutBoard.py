import random

from unified_planning.model import Fluent, Object
from unified_planning.shortcuts import (BoolType, InstantaneousAction, Problem,
                                        UserType)

# Types and Objects
Cell = UserType("Cell")
Board = dict((f"c{i}-{j}", Object(f"c{i}-{j}", Cell)) for i in range(5) for j in range(5))  # 5x5 grid of cells

# Predicates
cell_on = Fluent("cell_on", BoolType(), c=Cell)
cell_off = Fluent("cell_off", BoolType(), c=Cell)
cell_adjacent = Fluent("cell_adjacent", BoolType(), c1=Cell, c2=Cell)

# Problem
problem = Problem("LightsOutBoard")
problem.add_fluent(cell_on)
problem.add_fluent(cell_off)
problem.add_fluent(cell_adjacent)
for cell in Board:
    if random.choice([True, False]):
        problem.set_initial_value(cell_on(Board[cell]), True)
        problem.set_initial_value(cell_off(Board[cell]), False)
    else:
        problem.set_initial_value(cell_on(Board[cell]), False)
        problem.set_initial_value(cell_off(Board[cell]), True)
for i in range(5):
    for j in range(5):
        if i > 0:
            problem.set_initial_value(cell_adjacent(Board[f"c{i-1}-{j}"], Board[f"c{i}-{j}"]), True)
        if j > 0:
            problem.set_initial_value(cell_adjacent(Board[f"c{i}-{j-1}"], Board[f"c{i}-{j}"]), True)

# Actions
# set_on = InstantaneousAction("set_on", c=Cell)
# c = set_on.parameter("c")
# set_on.add_precondition(cell_off(c))
# set_on.add_effect(cell_on(c), True)
# set_on.add_effect(cell_off(c), False)
# for cell in Board:
#     counter = 0
#     if cell_adjacent(c, cell):
#         counter += 1
#         if cell_on(cell):
#             set_on.add_effect(cell_off(cell), True)
#             set_on.add_effect(cell_on(cell), False)
#         elif cell_off(cell):
#             set_on.add_effect(cell_on(cell), True)
#             set_on.add_effect(cell_off(cell), False)
#     if counter >= 4:
#         break

#------------------------ Generate PDDL files ------------------------#
if __name__ == "__main__":
    print(problem)
    print(set_on)
