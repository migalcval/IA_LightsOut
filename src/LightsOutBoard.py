import random
from unified_planning.model import Fluent, Object, InstantaneousAction
from unified_planning.shortcuts import BoolType, Problem, Not, UserType, And
from unified_planning.io import PDDLWriter

random.seed(33)  # For reproducibility

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

for cell in Board.values():
    problem.add_object(cell)
    if random.choice([True, False]):
        problem.set_initial_value(cell_on(cell), True)
        problem.set_initial_value(cell_off(cell), False)
    else:
        problem.set_initial_value(cell_on(cell), False)
        problem.set_initial_value(cell_off(cell), True)

for i in range(5):
    for j in range(5):
        if i > 0:
            problem.set_initial_value(cell_adjacent(Board[f"c{i-1}-{j}"], Board[f"c{i}-{j}"]), True)
        if j > 0:
            problem.set_initial_value(cell_adjacent(Board[f"c{i}-{j-1}"], Board[f"c{i}-{j}"]), True)

#------------------------ Actions -------------------------#

press_cell = InstantaneousAction("press_cell", c=Cell)
c = press_cell.parameter("c")
press_cell.add_effect(fluent=cell_on(c), value=Not(cell_on(c)))
press_cell.add_effect(fluent=cell_off(c), value=Not(cell_off(c)))

for cell in Board.values():
    press_cell.add_effect(condition=cell_adjacent(c, cell), fluent=cell_on(cell), value=Not(cell_on(cell)))
    press_cell.add_effect(condition=cell_adjacent(c, cell), fluent=cell_off(cell), value=Not(cell_off(cell)))

problem.add_action(press_cell)

#------------------------ Goal -------------------------#

goal = []
for cell in Board.values():
    problem.add_goal(cell_on(cell))

#------------------------ Generate PDDL files ------------------------#

if __name__ == "__main__":

    print(problem)
    writer = PDDLWriter(problem, rewrite_bool_assignments=True)
    writer.write_domain("src/pddl/lightsout_domain.pddl")
    writer.write_problem("src/pddl/lightsout_problem.pddl")

#pyperplan -H hmax -s astar src/pddl/lightsout_domain.pddl src/pddl/lightsout_problem.pddl