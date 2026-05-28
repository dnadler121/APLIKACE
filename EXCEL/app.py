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
    "intro": "Doplň do sloupce C výsledek.",
    "task": "Když je hodnota v B2 větší než 2000 napiš VELKÁ, jinak napiš MALÁ.",
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
    "task": "Vezmi hodnotu z A2, hledej ji v tabulce E2:F5, vrať druhý sloupec a nakonec napiš 0.",
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
},

{
    "title": "KDYŽ – sleva",
    "icon": "🟢",
    "intro": "Rozhodni o slevě.",
    "task": "Když je hodnota v A2 větší než 500 napiš ANO, jinak napiš NE.",
    "cols": ["", "A", "B"],
    "rows": [
        ["1", "Cena", "Sleva"],
        ["2", "650", "?"]
    ],
    "answer": '=KDYŽ(A2>500;"ANO";"NE")',
    "result": "ANO"
},

{
    "title": "SVYHLEDAT – zaměstnanec",
    "icon": "🔍",
    "intro": "Najdi plat.",
    "task": "Vezmi jméno z A2, najdi ho v tabulce E2:F2, vrať druhý sloupec a nakonec napiš 0.",
    "cols": ["", "A", "B", "", "", "E", "F"],
    "rows": [
        ["1", "Jméno", "Plat", "", "", "Eva", "32000"],
        ["2", "Eva", "?"]
    ],
    "answer": '=SVYHLEDAT(A2;E2:F2;2;0)',
    "result": "32000"
},

{
    "title": "KDYŽ – docházka",
    "icon": "🟢",
    "intro": "Vyhodnoť docházku.",
    "task": "Když je číslo v A2 větší než 80 napiš SPLNIL, jinak napiš NESPLNIL.",
    "cols": ["", "A", "B"],
    "rows": [
        ["1", "Docházka", "Výsledek"],
        ["2", "90", "?"]
    ],
    "answer": '=KDYŽ(A2>80;"SPLNIL";"NESPLNIL")',
    "result": "SPLNIL"
},

{
    "title": "SVYHLEDAT – města",
    "icon": "🔍",
    "intro": "Najdi stát.",
    "task": "Vezmi město z A2, najdi ho v tabulce E1:F1, vrať druhý sloupec a nakonec napiš 0.",
    "cols": ["", "A", "B", "", "", "E", "F"],
    "rows": [
        ["1", "Město", "Stát", "", "", "Praha", "ČR"],
        ["2", "Praha", "?"]
    ],
    "answer": '=SVYHLEDAT(A2;E1:F1;2;0)',
    "result": "ČR"
},

{
    "title": "KDYŽ – věk",
    "icon": "🟢",
    "intro": "Urči dospělost.",
    "task": "Když je číslo v A2 větší nebo rovno 18 napiš DOSPĚLÝ, jinak napiš DÍTĚ.",
    "cols": ["", "A", "B"],
    "rows": [
        ["1", "Věk", "Výsledek"],
        ["2", "20", "?"]
    ],
    "answer": '=KDYŽ(A2>=18;"DOSPĚLÝ";"DÍTĚ")',
    "result": "DOSPĚLÝ"
},

{
    "title": "SVYHLEDAT – známky",
    "icon": "🔍",
    "intro": "Najdi známku.",
    "task": "Vezmi jméno z A2, najdi ho v tabulce E1:F1, vrať druhý sloupec a nakonec napiš 0.",
    "cols": ["", "A", "B", "", "", "E", "F"],
    "rows": [
        ["1", "Žák", "Známka", "", "", "Tomáš", "2"],
        ["2", "Tomáš", "?"]
    ],
    "answer": '=SVYHLEDAT(A2;E1:F1;2;0)',
    "result": "2"
},

{
    "title": "KDYŽ – sklad",
    "icon": "🟢",
    "intro": "Zkontroluj sklad.",
    "task": "Když je číslo v A2 menší než 10 napiš OBJEDNAT, jinak napiš SKLADEM.",
    "cols": ["", "A", "B"],
    "rows": [
        ["1", "Počet", "Výsledek"],
        ["2", "5", "?"]
    ],
    "answer": '=KDYŽ(A2<10;"OBJEDNAT";"SKLADEM")',
    "result": "OBJEDNAT"
},

{
    "title": "SVYHLEDAT – telefon",
    "icon": "🔍",
    "intro": "Najdi telefon.",
    "task": "Vezmi jméno z A2, najdi ho v tabulce E1:F1, vrať druhý sloupec a nakonec napiš 0.",
    "cols": ["", "A", "B", "", "", "E", "F"],
    "rows": [
        ["1", "Jméno", "Telefon", "", "", "Petr", "777888999"],
        ["2", "Petr", "?"]
    ],
    "answer": '=SVYHLEDAT(A2;E1:F1;2;0)',
    "result": "777888999"
},

{
    "title": "KDYŽ – bonus",
    "icon": "🟢",
    "intro": "Rozhodni o bonusu.",
    "task": "Když je číslo v A2 větší než 10000 napiš BONUS, jinak napiš BEZ BONUSU.",
    "cols": ["", "A", "B"],
    "rows": [
        ["1", "Prodej", "Výsledek"],
        ["2", "15000", "?"]
    ],
    "answer": '=KDYŽ(A2>10000;"BONUS";"BEZ BONUSU")',
    "result": "BONUS"
},

{
    "title": "SVYHLEDAT – suroviny",
    "icon": "🔍",
    "intro": "Najdi cenu suroviny.",
    "task": "Vezmi hodnotu z A2, najdi ji v tabulce E1:F1, vrať druhý sloupec a nakonec napiš 0.",
    "cols": ["", "A", "B", "", "", "E", "F"],
    "rows": [
        ["1", "Surovina", "Cena", "", "", "Mouka", "25"],
        ["2", "Mouka", "?"]
    ],
    "answer": '=SVYHLEDAT(A2;E1:F1;2;0)',
    "result": "25"
},

{
    "title": "KDYŽ – úspěšnost",
    "icon": "🟢",
    "intro": "Vyhodnoť test.",
    "task": "Když je číslo v A2 větší než 50 napiš PROSPĚL, jinak napiš NEPROSPĚL.",
    "cols": ["", "A", "B"],
    "rows": [
        ["1", "Body", "Výsledek"],
        ["2", "75", "?"]
    ],
    "answer": '=KDYŽ(A2>50;"PROSPĚL";"NEPROSPĚL")',
    "result": "PROSPĚL"
},

{
    "title": "SVYHLEDAT – učebny",
    "icon": "🔍",
    "intro": "Najdi učebnu.",
    "task": "Vezmi hodnotu z A2, najdi ji v tabulce E1:F1, vrať druhý sloupec a nakonec napiš 0.",
    "cols": ["", "A", "B", "", "", "E", "F"],
    "rows": [
        ["1", "Předmět", "Učebna", "", "", "ICT", "12"],
        ["2", "ICT", "?"]
    ],
    "answer": '=SVYHLEDAT(A2;E1:F1;2;0)',
    "result": "12"
},

{
    "title": "KDYŽ – mzda",
    "icon": "🟢",
    "intro": "Urči výši mzdy.",
    "task": "Když je číslo v A2 větší než 30000 napiš VYSOKÁ, jinak napiš NÍZKÁ.",
    "cols": ["", "A", "B"],
    "rows": [
        ["1", "Mzda", "Výsledek"],
        ["2", "35000", "?"]
    ],
    "answer": '=KDYŽ(A2>30000;"VYSOKÁ";"NÍZKÁ")',
    "result": "VYSOKÁ"
},

{
    "title": "SVYHLEDAT – menu",
    "icon": "🔍",
    "intro": "Najdi cenu menu.",
    "task": "Vezmi hodnotu z A2, najdi ji v tabulce E1:F1, vrať druhý sloupec a nakonec napiš 0.",
    "cols": ["", "A", "B", "", "", "E", "F"],
    "rows": [
        ["1", "Menu", "Cena", "", "", "Menu 1", "139"],
        ["2", "Menu 1", "?"]
    ],
    "answer": '=SVYHLEDAT(A2;E1:F1;2;0)',
    "result": "139"
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

    session.clear()

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

            already_solved = session.get(f"solved_{current}", False)

            if not already_solved:
                score += 10
                session["score"] = score
                session[f"solved_{current}"] = True

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

    current = session.get("current", 0)

    if current + 1 >= len(QUESTIONS):
        return redirect(url_for("excel.finish"))

    session["current"] = current + 1

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
