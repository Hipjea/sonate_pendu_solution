import random
import secrets

from unidecode import unidecode
from flask import Flask, render_template, request, session


# Déclaration de la variable globale de l'application Flask :
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)


def debug_game(message):
    """
    Fonction permettant la mise en forme en couleur des logs dans la console pour le debug.
    """
    ORANGE = "\033[93m"
    END = "\033[0m"

    print("{}{}{}".format(ORANGE, "#" * 80, END))
    print("{}word to find : {}{}".format(ORANGE, message, END))
    print("{}{}{}".format(ORANGE, "#" * 80, END))


def take_a_word(filepath):
    """
    Fonction réalisant le tirage aléatoire dans le fichier dictionnaire.txt

    filepath -- Chemin vers le fichier dictionnaire.txt
    return -- Une ligne du fichier dictionnaire.txt
    """
    f = open(filepath, encoding="utf-8")
    lignes = f.readlines()
    rnd = random.randint(0, len(lignes) - 1)
    return lignes[rnd]


def get_word():
    """
    Fonction permettant de tirer un mot au hasard dans le fichier dictionnaire.txt

    return -- Un mot du fichier converti en minuscule
    """
    mot = take_a_word("static/dictionnaire.txt").split(";")[0]
    session['mot'] = unidecode(mot.lower())
    session['display'] = "_" * len(mot)

    return session['mot']


@app.route("/")
def home():
    """
    Affichage de la page d'accueil.
    """
    # Variables de session du projet :
    session['won'] = False
    session['score'] = 0
    session['found'] = []
    session['life'] = 5
    session['display'] = ""
    session['user_name'] = ""

    return render_template("home.html")


@app.route("/play", methods=["POST"])
def play():
    """
    Affichage de la page du jeu après lancement.
    """
    get_word()

    if request.method == "POST":
        session['user_name'] = request.form["user_name"]

    return render_template("play.html", user_name=session['user_name'], life=session['life'], secret_word=session['display'])


@app.route("/guess", methods=["POST"])
def guess():
    """
    Affichage de la page du jeu après une tentative.
    """
    longueur = len(session['mot'])
    debug_game(session['mot'])

    # Récupération de la valeur de l'input du formulaire :
    user_input = request.form.get("user_input").lower()

    if user_input:
        if user_input in session['mot']:
            for index in range(len(session['mot'])):
                if session['mot'][index] == user_input:
                    session['found'].extend([user_input])
                    session['display'] = session['display'][:index] + user_input + session['display'][index + 1 :]
        else:
            session['life'] -= 1

        if session['display'] == session['mot']:
            session['won'] = True
            return render_template(
                "end.html",
                user_name=session['user_name'],
                life=session['life'],
                secret_word=session['display'],
                won=session['won']
            )

        if session['life'] <= 0:
            won = False
            return render_template(
                "end.html",
                user_name=session['user_name'],
                life=session['life'],
                secret_word=session['display'],
                won=session['won'],
                solution=session['mot']
            )

        return render_template(
            "play.html",
            user_name=session['user_name'],
            life=session['life'],
            secret_word=session['display'],
            user_input=user_input,
        )

    return render_template(
      "play.html",
      user_name=session['user_name'],
      life=session['life'],
      secret_word=session['display']
    )


@app.route("/reset")
def reset():
    """
    Remise à zéro du jeu.
    """

    session['mot'] = ''
    session['display'] = ''
    session['won'] = False
    session['score'] = 0
    session['life'] = 5
    session['found'] = []

    return render_template("home.html", user_name=session['user_name'])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')