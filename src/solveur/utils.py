import re


def parse_objective(objective_str):
    match = re.search(r"(Maximize|Minimize) Z = (.+)", objective_str)
    if match:
        objective_type = match.group(1)
        equation = match.group(2)
        return {"type": objective_type, "equation": equation}
    return None


def parse_constraints(constraints_list):
    constraints = []
    for constraint in constraints_list:
        match = re.match(r"(c\d+): (.+)", constraint)
        if match:
            constraint_id = match.group(1)
            equation = match.group(2)
            constraints.append({"id": constraint_id, "equation": equation})
    return constraints
