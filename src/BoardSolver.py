from collections import namedtuple

Constant = namedtuple("Constant", ["name", "type"])
UnaryPredicate = namedtuple("UnaryPredicate", ["name", "parameter", "positive"])
BinaryPredicate = namedtuple("BinaryPredicate", ["name", "parameter1", "parameter2", "positive"])
Action = namedtuple("Action", ["name", "parameters", "preconditions", "effects"])
Effect = namedtuple("Effect", ["conditions", "effects"])
Dominio = namedtuple("Dominio", ["types", "constants", "predicates", "actions"])

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
        if line != "":
            if line.startswith("(:types"):
                if line.strip() == "(:types)":
                    in_types = True
                else:
                    for domain_type in line.replace("(:types", "").replace(")", "").split(" ")[1:]:
                        types.append(domain_type.strip())
            elif in_types:
                # Do if necessary, I think unified-planning does not behave like this
                pass
            elif line.startswith("(:constants"):
                in_types = False
                if line.strip() == "(:constants":
                    in_constants = True
                else:
                    # Do if necessary, I think unified-planning does not behave like this
                    pass
            elif in_constants:
                if line.strip() != ")":
                    objs = line.split("-")
                    constant_type = objs[1].strip()
                    if constant_type not in types:
                        raise ValueError(f"Type {constant_type} not in domain ({types})")
                    for constant in objs[0].split(" "):
                        constants.append(Constant(constant.strip(), constant_type))
                else:
                    in_constants = False
            elif line.startswith("(:predicates"):
                if line.strip() == "(:predicates":
                    in_predicates = True
                else:
                    objs = line.replace("(:predicates", "").replace("))", "").split(") (")
                    for predicate in objs:
                        predicate = predicate.replace("(", "").replace(")", "").replace(" - ", "-").strip()
                        if len(predicate.split(" ")) == 2:
                            name, param = predicate.split(" ?")
                            parsed_param = parse_constant(param, types)
                            predicates.append(UnaryPredicate(name.strip(), parsed_param, True))
                        elif len(predicate.split(" ")) == 3:
                            name, param1, param2 = predicate.split(" ?")
                            parsed_param1 = parse_constant(param1, types)
                            parsed_param2 = parse_constant(param2, types)
                            predicates.append(BinaryPredicate(name.strip(), parsed_param1, parsed_param2, True))
            elif in_predicates:
                # Do if necessary, I think unified-planning does not behave like this
                pass
            elif line.startswith("(:action"):
                in_action = True
                action_name = line.replace("(:action", "").strip()
                action_params = []
                action_preconditions = []
                action_effects = []
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
                            action_preconditions.append(UnaryPredicate(name.strip(), param.strip(), True))
                        elif len(precondition.split(" ")) == 3:
                            name, param1, param2 = precondition.split(" ?")
                            action_preconditions.append(BinaryPredicate(name.strip(), param1.strip(), param2.strip(), True))
                elif line.startswith(":effect"):
                    effects = line.replace(":effect (and (","").strip()
                    objs = effects.split("(when (")
                    for effect in objs:
                        if effect.strip() != "":
                            conditions = []
                            effects = []
                            effect_parts = effect.strip().split(") (")
                            if effect.strip().startswith("and ("):
                                effect = effect.replace("and (","").strip()
                            for i in range(len(effect_parts)):
                                part = effect_parts[i].replace("(","").replace(")","").replace("?","").strip()
                                positive = True
                                if part.startswith("not"):
                                    positive = False
                                if i < len(effect_parts) - 1:
                                    condition_parts = part.split(" ")
                                    if len(condition_parts) == 2:
                                        conditions.append(UnaryPredicate(condition_parts[0], condition_parts[1], positive))
                                    elif len(condition_parts) == 3:
                                        conditions.append(BinaryPredicate(part.split(" ")[0], part.split(" ")[1], part.split(" ")[2], positive))
                                else:
                                    effects.append(UnaryPredicate(part.split(" ")[0], part.split(" ")[1], positive))
                            action_effects.append(Effect(conditions, effects))
                elif line == ")":
                    actions.append(Action(action_name, action_params, action_preconditions, action_effects))
                    in_action = False
    domain = Dominio(types, constants, predicates, actions)
    return domain

def parse_constant(constant, types):
    parts = constant.replace("(","").replace(")","").split("-")
    if parts[1].strip() not in types:
        raise ValueError(f"Type {parts[1].strip()} not in domain ({types})")
    param = Constant(parts[0].strip(), parts[1].strip())
    return param

if __name__ == "__main__":
    dominio = parse_domain("src/pddl/lightsout_domain.pddl")
    print(dominio)