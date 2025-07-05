from parsers import parse_domain, parse_problem, Constant, UnaryPredicate, BinaryPredicate, Action, Domain
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
    # Initialize the A* search algorithm
    initial_cells_on = get_cells_on(problem.init)
    res = []
    actions = []
    for cell in cells:
        actions.append(f"press cell {cell}")

    # 1 and 2
    g = defaultdict(lambda: infinity)
    f = defaultdict(lambda: infinity)

    h = get_h_add(cells, initial_cells_on)
    g[initial_cells_on] = 0
    f[initial_cells_on] = h
    # 3
    closed = set()
    # 4
    open_states = set(initial_cells_on)
    # 5
    while open_states:
        # 6
        s = min(open_states, key=lambda x: f[x])
        # 7
        closed.add(s)
        # 8
        if get_cells_on(problem.goal) in s:
            # 9
            return res
        # 10
        for action in actions:
            next_s = apply_action(s, action)


    # Solve the problem
    
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