from flask import Flask, render_template

from MATEMATIKA.app import matematika_bp
from EXCEL.app import excel_bp
from OBCANKA.app import obcanka_bp

app = Flask(__name__)
app.secret_key = "tajny_klic"

# registrace aplikací
app.register_blueprint(matematika_bp, url_prefix="/matematika")
app.register_blueprint(excel_bp, url_prefix="/excel")
app.register_blueprint(obcanka_bp, url_prefix="/obcanka")

@app.route("/")
def menu():
    return render_template("menu.html")

if __name__ == "__main__":
    app.run(debug=True)