from collections import namedtuple

Constant = namedtuple("Constant", ["name", "type"])
UnaryPredicate = namedtuple("UnaryPredicate", ["name", "parameter"])
BinaryPredicate = namedtuple("BinaryPredicate", ["name", "parameter1", "parameter2"])
Action = namedtuple("Action", ["name", "parameters", "preconditions", "effects"])

def parse_domain(file_path):
    with open(file_path) as file:
        lines = file.readlines()
    in_types = False
    in_constants = False
    in_predicates = False
    in_action = False
    types = []
    constants = []
    predicates = []
    actions = []
    action_name = None
    action_params = []
    action_preconditions = []
    action_effects = []
    for line in lines:
        line = line.strip()
        if line.startswith("(:types"):
            if line.strip() == "(:types)":
                in_types = True
                continue
            else:
                types.append(line.replace("(:types", "").replace(")", "").split(" "))
        elif in_types:
            # Do if necessary, I think unified-planning does not behave like this
            pass
        elif line.startswith("(:constants"):
            in_types = False
            if line.strip() == "(:constants)":
                in_constants = True
                continue
            else:
                # Do if necessary, I think unified-planning does not behave like this
                pass
        elif in_constants:
            if line.strip() != ")":
                objs = line.split("-")
                constant_type = objs[1]
                if constant_type not in types:
                    raise ValueError(f"Type {constant_type} not in domain")
                for constant in objs[0].split(" "):
                    constants.append(Constant(constant.strip(), constant_type.strip()))
            else:
                continue
        elif line.startswith("(:predicates"):
            in_constants = False
            if line.strip() == "(:predicates)":
                in_predicates = True
                continue
            else:
                objs = line.replace("(:predicates", "").replace("))", "").split(") (")
                for predicate in objs:
                    if len(predicate.split(" ")) == 2:
                        name, param = predicate.split(" ?")
                        parsed_param = parse_constant(param, types)
                        predicates.append(UnaryPredicate(name.strip(), parsed_param.strip()))
                    elif len(predicate.split(" ")) == 3:
                        name, param1, param2 = predicate.split(" ?")
                        parsed_param1 = parse_constant(param1, types)
                        parsed_param2 = parse_constant(param2, types)
                        predicates.append(BinaryPredicate(name.strip(), parsed_param1.strip(), parsed_param2.strip()))
        elif in_predicates:
            # Do if necessary, I think unified-planning does not behave like this
            pass
        elif line.startswith("(:action"):
            in_action = True
            action_name = line.replace("(:action)").strip()
            action_params = []
            action_preconditions = []
            action_effects = []
            continue
        elif in_action:
            if line.startswith(":parameters"):
                params = line.replace(":parameters (", "").strip()[1:].split(" ?")
                for param in params:
                    parsed_param = parse_constant(param, types)
                    action_params.append(parsed_param)
            elif line.startswith(":precondition"):
                preconditions = line.replace(":precondition ()", "").replace("and (","").replace("))", "").strip()
                objs = preconditions.split(") (")
                for precondition in objs:
                    if len(precondition.split(" ")) == 2:
                        name, param = precondition.split(" ?")
                        action_preconditions.append(UnaryPredicate(name.strip(), param.strip()))
                    elif len(precondition.split(" ")) == 3:
                        name, param1, param2 = precondition.split(" ?")
                        action_preconditions.append(BinaryPredicate(name.strip(), param1.strip(), param2.strip()))
            elif line.startswith(":effect"):
                effects = line.replace(":effect ()", "").replace("and (","").replace("))", "").strip()
                objs = effects.split(") (")
                for effect in objs:
                    #TODO los objetos tienen muchas clausulas hay q tener cuidado
                    pass
            elif line == ")":
                actions.append(Action(action_name, action_params, action_preconditions, action_effects))
                in_action = False
        row = list(map(int, line.strip().split()))
        board.append(row)
    
    return board

def parse_constant(constant, types):
    name, constant_type = constant.split("-")
    if constant_type not in types:
        raise ValueError(f"Type {constant_type} not in domain")
    param = Constant(name.strip(), constant_type.strip())