from django.shortcuts import redirect, render
from PIL import Image
from django.urls import reverse
import google.generativeai as genai
import pytesseract
import re
import json

from .utils import parse_constraints, parse_objective


def index(request):
    if request.method == "POST":
        image = request.FILES["image"]

        try:
            img = Image.open(image)
            text = pytesseract.image_to_string(img)

            genai.configure(api_key="AIzaSyD83g8POO_8rslMcPD5JrEKdvN7d4Fd-LE")

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
    pass
