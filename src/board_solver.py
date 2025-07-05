from parsers import parse_domain, parse_problem, Constant, UnaryPredicate, BinaryPredicate, Action, Domain
from math import inf as infinity

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
    # problem = parse_problem(problem_file, domain)

    # Solve the problem
    
def get_h_add(domain, problem):
    res = 0
    for cell in domain.constants:
        if cell.type == "cell" and cell.name not in get_init_cells_on(problem.init):
            res += 1
    return res

def get_init_cells_on(init):
    res = set()
    for fact in init:
        if isinstance(fact, UnaryPredicate) and fact.name == "cell_on":
            res.add(fact.parameter)
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