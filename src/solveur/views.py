from django.shortcuts import redirect, render
from PIL import Image
from django.urls import reverse
import google.generativeai as genai
import pytesseract
import re
import json

from .utils import parse_constraints, parse_objective

genai.configure(api_key="AIzaSyD83g8POO_8rslMcPD5JrEKdvN7d4Fd-LE")
model = genai.GenerativeModel("gemini-1.5-flash")


def index(request):
    if request.method == "POST":
        image = request.FILES["image"]

        try:
            img = Image.open(image)
            text = pytesseract.image_to_string(img)

            prompt = """
            {}

            respond strictly in string can be Deserialisable in json:

            
            Objective: Maximize Z = a1*x1 + a2*x2 + ... + an*xn

            Constraints:
            c1: a1*x1 + a2*x2 <= b1
            c2: a1*x1 + a2*x2 <= b2
            ...
            
            Do not include any additional information or commentary outside this format.
            """.format(
                text
            )

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

            objective = parse_objective(data["Objective"])
            constraints = parse_constraints(data["Constraints"])
            return render(
                request,
                "solveur/result.html",
                {"result": {"objective": objective, "constraints": constraints}},
            )
        except:
            return render(
                request,
                "solveur/index.html",
                {"error": "Veuillez entrer une image valide"},
            )
    else:
        return render(request, "solveur/index.html")


def resolve(request):
    if request.method == "POST":
        prompt = f"""
        Solve this linear problem in json where i provide the type of the linear problem and all of the constraint using simplex
        Do not include any additional information or commentary.

        
        f{request.POST["lp_problem"]}
"""
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
            print(json_str)
            data = json.loads(json_str)

        return render(
            request,
            "solveur/solution.html",
            {"data": data},
        )
    else:
        return redirect(reverse("solveur:index"))
