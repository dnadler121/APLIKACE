from flask import Blueprint, render_template, request, redirect, url_for, session
import csv
import os
from datetime import datetime
from email.message import EmailMessage
import smtplib

obcanka_bp = Blueprint(
    "obcanka",
    __name__,
    template_folder="templates",
    static_folder="static"
)
BASE_DIR = os.path.dirname(__file__)

QUESTIONS_FILE = os.path.join(BASE_DIR, "data", "questions.csv")
RESULTS_FILE = os.path.join(BASE_DIR, "data", "results.csv")


TEACHER_EMAIL = "dnadler121@gmail.com"


def load_questions():

    questions = []

    with open(QUESTIONS_FILE, encoding="utf-8-sig", newline="") as f:

        reader = csv.DictReader(f, delimiter=";")

        for row in reader:

            questions.append({
                "id": row["id"],
                "question": row["question"],
                "a": row["a"],
                "b": row["b"],
                "c": row["c"],
                "d": row["d"],
                "correct": row["correct"].strip().lower()
            })

    return questions[:50]


def save_result(result):

    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

    file_exists = os.path.exists(RESULTS_FILE)

    with open(RESULTS_FILE, "a", encoding="utf-8", newline="") as f:

        writer = csv.writer(f, delimiter=";")

        if not file_exists:

            writer.writerow([
                "čas",
                "příjmení",
                "body",
                "celkem",
                "procenta",
                "známka"
            ])

        writer.writerow([
            result["time"],
            result["surname"],
            result["score"],
            result["total"],
            result["percent"],
            result["grade"]
        ])


def send_result_email(result):

    username = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")

    if not username or not password:

        return False, "E-mail není nastavený."

    msg = EmailMessage()

    msg["Subject"] = f"Výsledek testu občanka - {result['surname']}"
    msg["From"] = username
    msg["To"] = TEACHER_EMAIL

    body = f"""
Výsledek testu občanská výchova

Příjmení: {result['surname']}
Čas: {result['time']}
Body: {result['score']} / {result['total']}
Procenta: {result['percent']} %
Známka: {result['grade']}
"""

    msg.set_content(body)

    try:

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(username, password)
            smtp.send_message(msg)

        return True, "Výsledek byl odeslán."

    except Exception as e:

        return False, f"Chyba e-mailu: {e}"


@obcanka_bp.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        surname = request.form.get("surname", "").strip()

        if not surname:

            return render_template(
                "login.html",
                error="Vyplň příjmení."
            )

        session.clear()

        session["surname"] = surname

        return redirect(url_for("obcanka.test"))

    return render_template("login.html")


@obcanka_bp.route("/test", methods=["GET", "POST"])
def test():

    if "surname" not in session:

        return redirect(url_for("obcanka.login"))

    questions = load_questions()

    if request.method == "POST":

        score = 0

        details = []

        for q in questions:

            student_answer = request.form.get(f"q{q['id']}", "")

            correct = q["correct"]

            options = {
                "a": q["a"],
                "b": q["b"],
                "c": q["c"],
                "d": q["d"]
            }

            is_correct = student_answer == correct

            if is_correct:
                score += 1

            details.append({
                "id": q["id"],
                "question": q["question"],
                "student_answer_text": options.get(
                    student_answer,
                    "Nezodpovězeno"
                ),
                "correct_answer_text": options.get(
                    correct,
                    ""
                ),
                "status": "správně" if is_correct else "špatně"
            })

        total = len(questions)

        percent = round(score / total * 100)

        if percent >= 90:
            grade = 1
        elif percent >= 75:
            grade = 2
        elif percent >= 55:
            grade = 3
        elif percent >= 35:
            grade = 4
        else:
            grade = 5

        result = {

            "surname": session["surname"],
            "score": score,
            "total": total,
            "percent": percent,
            "grade": grade,
            "details": details,
            "time": datetime.now().strftime("%d.%m.%Y %H:%M")
        }

        save_result(result)

        session["result"] = result

        return redirect(url_for("obcanka.result"))

    return render_template(
        "test.html",
        questions=questions,
        surname=session["surname"]
    )


@obcanka_bp.route("/result", methods=["GET", "POST"])
def result():

    if "result" not in session:

        return redirect(url_for("obcanka.login"))

    result = session["result"]

    email_message = None

    if request.method == "POST":

        success, email_message = send_result_email(result)

    return render_template(
        "result.html",
        result=result,
        email_message=email_message,
        teacher_email=TEACHER_EMAIL
    )


@obcanka_bp.route("/restart")
def restart():

    session.clear()

    return redirect(url_for("obcanka.login"))
