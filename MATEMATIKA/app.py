from flask import Blueprint, render_template, request

matematika_bp = Blueprint(
    "matematika",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@matematika_bp.route("/", methods=["GET", "POST"])
def index():

    vysledek = None
    znamka = None
    procenta = None

    if request.method == "POST":

        spravne = {

            # Nerovnice
            "n1": "2",
            "n2": "3",
            "n3": "-2",
            "n4": "3",
            "n5": "-2",

            "n6": "2",
            "n7": "3",
            "n8": "-2",
            "n9": "3",
            "n10": "-2",

            # Intervaly
            "i1": "2",
            "i2": "4",

            # Rovnice
            "r1": "4",
            "r2": "4",
            "r3": "8",
            "r4": "16",
            "r5": "16",
            "r6": "8",
            "r7": "10",
            "r8": "5",

            # Soustava
            "s1": "-15",
            "s2": "-6",
            "s3": "-7",
            "s4": "-21",
            "s5": "3",
            "s6": "3",
            "s7": "5",
            "s8": "2",
        }

        body = 0

        for klic, hodnota in spravne.items():

            uzivatel = request.form.get(klic, "").strip()

            if uzivatel == hodnota:
                body += 1

        celkem = len(spravne)

        procenta = round((body / celkem) * 100)

        if procenta >= 90:
            znamka = 1
        elif procenta >= 80:
            znamka = 2
        elif procenta >= 70:
            znamka = 3
        elif procenta >= 50:
            znamka = 4
        else:
            znamka = 5

        vysledek = f"{body} / {celkem}"

    return render_template(
        "matematika.html",
        vysledek=vysledek,
        procenta=procenta,
        znamka=znamka
    )

