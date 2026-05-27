from flask import Blueprint, render_template, request, redirect, url_for, session

excel_bp = Blueprint(
    "excel",
    __name__,
    template_folder="templates",
    static_folder="static"
)

QUESTIONS = [

{
    "title": "KDYŽ – podmínka",
    "icon": "🟢",
    "intro": "Doplň do sloupce C, zda je objednávka VELKÁ nebo MALÁ.",
    "task": "Pokud je částka ve sloupci B větší než 2000, napiš VELKÁ, jinak MALÁ.",
    "cols": ["", "A", "B", "C"],
    "rows": [
        ["1", "Produkt", "Částka", "Výsledek"],
        ["2", "Káva", "1200", "?"],
        ["3", "Čaj", "2500", "?"]
    ],
    "answer": '=KDYŽ(B2>2000;"VELKÁ";"MALÁ")',
    "result": "MALÁ"
},

{
    "title": "SVYHLEDAT – ceny",
    "icon": "🔍",
    "intro": "Najdi cenu produktu.",
    "task": "Vyhledej hodnotu z A2 v tabulce E2:F5 a vrať hodnotu z 2. sloupce.",
    "cols": ["", "A", "B", "", "", "E", "F"],
    "rows": [
        ["1", "Hledané", "Výsledek", "", "", "Jídlo", "Cena"],
        ["2", "Káva", "?", "", "", "Polévka", "45"],
        ["3", "", "", "", "", "Káva", "49"],
        ["4", "", "", "", "", "Řízek", "145"],
        ["5", "", "", "", "", "Dezert", "69"]
    ],
    "answer": '=SVYHLEDAT(A2;E2:F5;2;0)',
    "result": "49"
}

]

def normalize(text):
    return text.replace(" ", "").upper()

def grade(percent):

    if percent >= 90:
        return 1
    elif percent >= 80:
        return 2
    elif percent >= 70:
        return 3
    elif percent >= 60:
        return 4
    else:
        return 5

@excel_bp.route("/")
def index():

    session["current"] = 0
    session["score"] = 0

    return render_template(
        "excel.html",
        total=len(QUESTIONS)
    )

@excel_bp.route("/task", methods=["GET", "POST"])
def task():

    current = session.get("current", 0)
    score = session.get("score", 0)

    if current >= len(QUESTIONS):
        return redirect(url_for("excel.finish"))

    q = QUESTIONS[current]

    solved = False
    message = ""
    user_answer = ""

    if request.method == "POST":

        user_answer = request.form["answer"]

        if normalize(user_answer) == normalize(q["answer"]):

            solved = True

            score += 10

            session["score"] = score

            message = "✅ Správně! +10 bodů"

        else:

            message = "❌ Špatně, zkus to znovu."

    max_score = len(QUESTIONS) * 10

    percent = round((score / max_score) * 100)

    return render_template(
        "task.html",
        q=q,
        index=current + 1,
        total=len(QUESTIONS),
        score=score,
        percent=percent,
        grade=grade(percent),
        message=message,
        solved=solved,
        user_answer=user_answer
    )

@excel_bp.route("/next")
def next_task():

    session["current"] += 1

    return redirect(url_for("excel.task"))

@excel_bp.route("/finish")
def finish():

    score = session.get("score", 0)

    max_score = len(QUESTIONS) * 10

    percent = round((score / max_score) * 100)

    return render_template(
        "finish.html",
        score=score,
        max_score=max_score,
        percent=percent,
        grade=grade(percent)
    )

