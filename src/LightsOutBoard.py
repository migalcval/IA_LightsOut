import random

from unified_planning.model import Fluent, Object, InstantaneousAction
from unified_planning.shortcuts import (BoolType, Problem, Not, UserType,
                                        And)
from unified_planning.io import PDDLWriter

Cell = UserType("Cell")
Board = dict((f"c{i}-{j}", Object(f"c{i}-{j}", Cell)) for i in range(5) for j in range(5))  # 5x5 grid of cells

#------------------------- Predicates -------------------------#

cell_on = Fluent("cell_on", BoolType(), c=Cell)
cell_off = Fluent("cell_off", BoolType(), c=Cell)
cell_adjacent = Fluent("cell_adjacent", BoolType(), c1=Cell, c2=Cell)

#------------------------ Problem -------------------------#

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

#------------------------ Actions -------------------------#

press_cell = InstantaneousAction("press_cell", c=Cell)
c = press_cell.parameter("c")

press_cell.add_precondition(cell_on(c) == True)
press_cell.add_precondition(cell_off(c) == False)

for cell in Board.values():
    press_cell.add_conditional_effects(cell_adjacent(c, cell), cell_on(cell), Not(cell_on(cell)))
    press_cell.add_conditional_effects(cell_adjacent(c, cell), cell_off(cell), Not(cell_off(cell)))

problem.add_action(press_cell)

#------------------------ Goal -------------------------#

goal = []
for cell in Board.values():
    goal.append(cell_on(cell) == True)
problem.add_goal(And(*goal))

#------------------------ Generate PDDL files ------------------------#

if __name__ == "__main__":

    print(problem)
    writer = PDDLWriter(problem)
    writer.write_domain("dominio_mundo_bloques.pddl")
    writer.write_problem("problema_mundo_bloques.pddl")

