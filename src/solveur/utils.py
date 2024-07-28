import re
import google.generativeai as genai
import json


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


def gemini_generate(prompt):
    genai.configure(api_key="AIzaSyD83g8POO_8rslMcPD5JrEKdvN7d4Fd-LE")
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(prompt)
    current_res = (
        response.candidates[0]
        .content.parts[0]
        .text.replace("```", "")
        .replace("\n", "")
    )
    json_match = re.search(r"{.*}", current_res)

    if json_match:
        json_str = json_match.group(0)
        data = json.loads(json_str)
        return data
    return None
