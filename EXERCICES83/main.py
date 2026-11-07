
import os
import re
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_mail import Mail, Message

# Configuration de Flask
load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Configuration de Flask-Mail
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")
mail = Mail(app)

# Page d'accueil
@app.route("/")
def home():
    return render_template("index.html")

# Page à propos
@app.route("/about")
def about():
    return render_template("about.html")

# Page projets
@app.route("/projects")
def projects():
    return render_template("projects.html")

# Page contact
@app.route("/contact", methods=["GET", "POST"])
def contact():
    success, error = False, None
    name = email = message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            error = "Tous les champs sont obligatoires."
        elif not re.match(r"^[\w.-]+@[\w.-]+\.\w+$", email):
            error = "Adresse email invalide."
        else:
            try:
                msg = Message(
                    subject=f"Message de {name}",
                    recipients=[os.getenv("RECIPIENT_EMAIL")],
                    reply_to=email,
                    body=f"Nom : {name}\nEmail : {email}\n\n{message}"
                )
                mail.send(msg)
                success = True
                name = email = message = ""

            except Exception as e:
                error = f"Erreur lors de l'envoi : {e}"

    return render_template(
        "contact.html",
        success=success,
        error=error,
        name=name,
        email=email,
        message=message
    )

# Lancement du serveur
if __name__ == "__main__":
    app.run(debug=True, port=5000)
