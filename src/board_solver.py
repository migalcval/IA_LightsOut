from parsers import parse_domain, parse_problem, Constant, UnaryPredicate, BinaryPredicate, Action, Domain, Effect
from math import inf as infinity
from collections import defaultdict, namedtuple

Move = namedtuple("Move", ["previous_state", "action", "resulting_state"])

def solve_board(domain_file, problem_file):
    """
    Solve a PDDL domain and problem file using the unified-planning library.
    
    Args:
        domain_file (str): Path to the PDDL domain file.
        problem_file (str): Path to the PDDL problem file.

    Returns:
        str: The solution plan as a string.
    """

    # Parse the domain and problem files
    domain = parse_domain(domain_file)
    problem = parse_problem(problem_file)
    cells = get_cells(domain)
    actions = []
    for cell in cells:
        actions.append(f"press_cell {cell}")
    adjacencies = set()
    for predicate in problem.init:
        if isinstance(predicate, BinaryPredicate):
            adjacencies.add({predicate.parameter1, predicate.parameter2})
    # Initialize the A* search algorithm
    initial_cells_on = get_cells_on(problem.init)
    res = []

    # 1
    g = defaultdict(lambda: infinity)
    g[initial_cells_on] = 0
    # 2
    f = defaultdict(lambda: infinity)
    h = get_h_add(cells, initial_cells_on)
    f[initial_cells_on] = h
    # 3
    closed = set()
    # 4
    open_states = set(initial_cells_on)
    # 5
    while open_states:
        # 6
        s = min(open_states, key=lambda x: f[x])
        open_states.remove(s)
        # 7
        closed.add(s)
        # 8
        if get_cells_on(problem.goal) in s:
            # 9
            return res
        # 10
        for action in actions:
            # 11
            next_s = apply_action(domain.actions,s, action, adjacencies)
            # 12
            if next_s in open_states and g[s] + 1 < g[next_s]:
                # 13
                res.append(Move(s, action, next_s))
                # 14
                g[next_s] = g[s] + 1
                # 15
                f[next_s] = g[next_s] + get_h_add(cells, next_s)
            # 16
            elif next_s in closed and g[s] + 1 < g[next_s]:
                # 17
                res.append(Move(s, action, next_s))
                # 18
                g[next_s] = g[s] + 1
                # 19
                f[next_s] = g[next_s] + get_h_add(cells, next_s)
                # 20
                closed.remove(next_s)
                # 21
                open_states.add(next_s)
            # 22
            elif next_s not in open_states and next_s not in closed:
                # 23
                res.append(Move(s, action, next_s))
                # 24
                g[next_s] = g[s] + 1
                # 25
                f[next_s] = g[next_s] + get_h_add(cells, next_s)
                # 26
                open_states.add(next_s)
    # 27
    return []
    
def get_h_add(cells, state):
    res = 0
    for cell in cells:
        if cell.name not in state:
            res += 1
    return res

def get_cells_on(predicates):
    res = set()
    for fact in predicates:
        if isinstance(fact, UnaryPredicate) and fact.name == "cell_on":
            res.add(fact.parameter)
    return res

def get_cells(domain):
    res = set()
    for constant in domain.constants:
        if constant.type == "cell":
            res.add(constant.name)
    return res

def apply_action(actions, state, action, adjacencies):
    obj = action.split(" ")
    action_name = obj[0]
    cell = obj[1]
    action_effects = get_action_effects(actions, state, action_name, cell, adjacencies)
    new_state = set(state)
    for effect in action_effects:
        if effect.conditions in new_state:
            for cond in effect.conditions:
                new_state.remove(cond)
            for eff in effect.effects:
                new_state.add(eff)
    return new_state

def get_action_effects(actions, state, action_name, cell, adjacencies):
    res = []
    for action in actions:
        if action.name == action_name:
            for effect in action.effects:
                parsed_conditions = []
                conditions = effect.conditions
                for condition in conditions:
                    if isinstance(condition, UnaryPredicate):
                        if condition.parameter == "c":
                            condition = UnaryPredicate(condition.name, cell, condition.positive)
                        if condition in state:
                            parsed_conditions.append(condition)
                    elif isinstance(condition, BinaryPredicate):
                        if condition.parameter1 == "c" and {cell, condition.parameter2} in adjacencies:
                            parsed_conditions.append(BinaryPredicate(condition.name, cell, condition.parameter2, condition.positive))
                        elif condition.parameter2 == "c" and {cell, condition.parameter1} in adjacencies:
                            parsed_conditions.append(BinaryPredicate(condition.name, condition.parameter1, cell, condition.positive))
                if not parsed_conditions:
                    continue
                parsed_effects = []
                effects = effect.effects
                for eff in effects:
                    if eff.parameter == "c":
                        parsed_effects.append(UnaryPredicate(eff.name, cell, eff.positive))
                    else:
                        parsed_effects.append(eff)
                res.append(Effect(parsed_conditions, parsed_effects))
    return res


if __name__ == "__main__":
    # Example usage
    domain_file = "src/pddl/lightsout_domain.pddl"
    problem_file = "src/pddl/lightsout_problem.pddl"
    
    # Solve the board and print the solution
    # solution = solve_board(domain_file, problem_file)
    # print(solution)
    
    # Example of getting h_add value
    domain = parse_domain(domain_file)
    problem = parse_problem(problem_file)
    h_add_value = get_h_add(domain, problem)
    print(f"h_add value: {h_add_value}")