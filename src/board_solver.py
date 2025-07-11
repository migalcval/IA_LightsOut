from parsers import parse_domain, parse_problem, Constant, UnaryPredicate, BinaryPredicate, Action, Domain, Effect
from math import inf as infinity
from collections import defaultdict
from Node import Node

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
            adjacencies.add(frozenset([predicate.parameter1, predicate.parameter2]))
    goal_cells = get_cells_on(problem.goal)
    # Initialize the A* search algorithm
    initial_cells_on = frozenset(get_cells_on(problem.init))
    nodes = set()
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
    open_states = {initial_cells_on}
    nodes.add(Node(initial_cells_on, None, None))
    # 5
    while open_states:
        # 6
        s = min(open_states, key=lambda x: f[x])
        print(get_h_add(cells, s))
        open_states.remove(s)
        # 7
        closed.add(s)
        # 8
        if goal_cells in s:
            # 9
            return get_solution_path(s, None, nodes)
        # 10
        for action in actions:
            # 11
            next_s = frozenset(apply_action(domain.actions,s, action, adjacencies))
            node = Node(next_s, s, action)
            # 12
            if next_s in open_states and g[s] + 1 < g[next_s]:
                # print("1st condition met")
                # 13
                if node in nodes:
                    nodes.remove(node)
                nodes.add(node)
                # 14
                g[next_s] = g[s] + 1
                # 15
                f[next_s] = g[next_s] + get_h_add(cells, next_s)
            # 16
            elif next_s in closed and g[s] + 1 < g[next_s]:
                # print("2nd condition met")
                # 17
                if node in nodes:
                    nodes.remove(node)
                nodes.add(node)
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
                # print("3rd condition met")
                # 23
                if node in nodes:
                    nodes.remove(node)
                nodes.add(node)
                # 24
                g[next_s] = g[s] + 1
                # 25
                f[next_s] = g[next_s] + get_h_add(cells, next_s)
                # 26
                open_states.add(next_s)
            # else:
            #     print("No condition met")
    # 27
    return []
    
def get_h_add(cells, state):
    res = 0
    for cell in cells:
        if cell not in state:
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
        for eff in effect.effects:
            if eff.positive:
                new_state.add(eff.parameter)
            else:
                new_state.remove(eff.parameter)
    return new_state

def get_action_effects(actions, state, action_name, cell, adjacencies):
    res = []
    for action in actions:
        if action.name == action_name:
            for effect in action.effects:
                parsed_conditions = []
                skip = True
                conditions = effect.conditions
                if len(conditions) == 1:
                    condition = conditions[0]
                    if isinstance(condition, UnaryPredicate):
                        if condition.parameter == "c":
                            condition = UnaryPredicate(condition.name, cell, condition.positive)
                            if condition.parameter in state and condition.positive or condition.parameter not in state and not condition.positive:
                                parsed_conditions.append(condition)
                else:
                    for condition in conditions:
                        if isinstance(condition, UnaryPredicate):
                            if condition.parameter == "c":
                                parsed_conditions.append(UnaryPredicate(condition.name, cell, condition.positive))
                            if (condition.parameter in state and condition.positive or condition.parameter not in state and not condition.positive) and {cell, condition.parameter} in adjacencies:
                                parsed_conditions.append(condition)
                            else:
                                continue
                        elif isinstance(condition, BinaryPredicate):
                            if condition.parameter1 == "c" and {cell, condition.parameter2} in adjacencies:
                                parsed_conditions.append(BinaryPredicate(condition.name, cell, condition.parameter2, condition.positive))
                            elif condition.parameter2 == "c" and {cell, condition.parameter1} in adjacencies:
                                parsed_conditions.append(BinaryPredicate(condition.name, condition.parameter1, cell, condition.positive))
                for parsed_condition in parsed_conditions:
                    if isinstance(parsed_condition, UnaryPredicate):
                        skip = False
                if skip:
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

def get_solution_path(state, action, nodes):
    path = []
    node = get_equal(nodes, state)
    if node is None:
        raise ValueError("State not found in nodes")
    father, father_action = node.father
    if father is not None:
        path = get_solution_path(father, father_action, nodes)
    path.append((state, action))
    return path

def get_equal(in_set, in_element):
   for element in in_set:
       if element == in_element:
           return element
   return None

if __name__ == "__main__":
    # Example usage
    domain_file = "src/pddl/lightsout_domain.pddl"
    problem_file = "src/pddl/lightsout_problem.pddl"
    
    # Solve the board and print the solution
    solution = solve_board(domain_file, problem_file)
    print(solution)