from parsers import parse_domain, parse_problem, Constant, UnaryPredicate, BinaryPredicate, Action, Domain, Effect
from math import inf as infinity
from collections import defaultdict
from Node import Node
import random

def mcts_algorithm(domain_file, problem_file, k, tries):
    values = None
    for i in range(tries):
        for j in range(k):
            if i==0 and j==0:
                values = mcts_iteration(domain_file, problem_file)
            else:
                values = mcts_iteration(domain_file, problem_file, values, extra_selections=i)
    return values

def mcts_iteration(domain_file, problem_file, mcts_value=None, extra_selections=0):
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
    # Initialize the MCTS algorithm
    initial_cells_on = frozenset(get_cells_on(problem.init))
    nodes = set()
    nodes.add(Node(initial_cells_on, None, None))
    value = 0
    path = []
    if mcts_value == None:
        mcts_value = defaultdict(int)
    # Selection
    states_sequence = [initial_cells_on]
    visited_states = {initial_cells_on}
    for i in range(3):
        action = random.choice(actions)
        new_state = frozenset(apply_action(domain.actions, states_sequence[i], action, adjacencies))
        states_sequence.append(new_state)
        visited_states.add(new_state)
        nodes.add(Node(new_state, states_sequence[i], action))
    if extra_selections > 0:
        for i in range(extra_selections):
            min_value = infinity
            next_state = None
            action_to_take = None
            for action in actions:
                new_state = frozenset(apply_action(domain.actions, states_sequence[-1], action, adjacencies))
                if mcts_value[new_state] < min_value:
                    min_value = mcts_value[new_state]
                    next_state = new_state
                    action_to_take = action
            states_sequence.append(next_state)
            visited_states.add(next_state)
            nodes.add(Node(next_state, states_sequence[-1], action_to_take))
    # Expansion
    expansion_state = None
    while expansion_state == None or expansion_state in visited_states:
        new_action = random.choice(actions)
        expansion_state = frozenset(apply_action(domain.actions, states_sequence[-1], new_action, adjacencies))
    states_sequence.append(expansion_state)
    visited_states.add(expansion_state)
    # Simulation
    g = defaultdict(lambda: infinity)
    g[initial_cells_on] = 0
    f = defaultdict(lambda: infinity)
    h = get_h_add(cells, expansion_state)
    f[initial_cells_on] = h
    f = defaultdict(lambda: infinity)
    h = get_h_add(cells, expansion_state)
    f[initial_cells_on] = h
    closed = set()
    open_states = {expansion_state}
    for i in range(5*5):
        s = min(open_states, key=lambda x: f[x])
        visited_states.add(s)
        states_sequence.append(s)
        open_states.remove(s)
        closed.add(s)
        if goal_cells in s:
            path = get_solution_path(s, None, nodes)
        elif s in visited_states:
            value = -1
            break
        for action in actions:
            next_s = frozenset(apply_action(domain.actions,s, action, adjacencies))
            node = Node(next_s, s, action)
            if next_s in open_states and g[s] + 1 < g[next_s]:
                if node in nodes:
                    nodes.remove(node)
                nodes.add(node)
                g[next_s] = g[s] + 1
                f[next_s] = g[next_s] + get_h_add(cells, next_s)
            elif next_s in closed and g[s] + 1 < g[next_s]:
                if node in nodes:
                    nodes.remove(node)
                nodes.add(node)
                g[next_s] = g[s] + 1
                f[next_s] = g[next_s] + get_h_add(cells, next_s)
                closed.remove(next_s)
                open_states.add(next_s)
            elif next_s not in open_states and next_s not in closed:
                if node in nodes:
                    nodes.remove(node)
                nodes.add(node)
                g[next_s] = g[s] + 1
                f[next_s] = g[next_s] + get_h_add(cells, next_s)
                open_states.add(next_s)
    # Retropropagation
    if len(path) > 0:
        value = 26-len(path)
    mcts_value[states_sequence[-1]] = value
    for i in range(len(states_sequence) - 2, -1, -1):
        mcts_value[states_sequence[i]] = mcts_value[states_sequence[i + 1]]/states_sequence.count(states_sequence[i])
    return mcts_value
    
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
    
    solution = mcts_algorithm(domain_file, problem_file, k=5, tries=10)
    print(solution)