import random

from unidecode import unidecode
from flask import Flask, render_template, request


# Déclaration de la variable globale de l'application Flask :
app = Flask(__name__)

# Variables globales du projet :
mot = False
won = False
score = 0
life = 5
found = []
user_name = ""


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
    global mot, display

    if mot == False and won == False:
        mot = take_a_word("static/dictionnaire.txt").split(";")[0]
        display = "_" * len(mot)

    return unidecode(mot.lower())


@app.route("/")
def home():
    """
    Affichage de la page d'accueil.
    """
    return render_template("home.html")


@app.route("/play", methods=["POST"])
def play():
    """
    Affichage de la page du jeu après lancement.
    """
    global user_name, life

    mot = get_word()
    
    if request.method == "POST":
        user_name = request.form["user_name"]

    return render_template("play.html", user_name=user_name, life=life, secret_word=display)


@app.route("/guess", methods=["POST"])
def guess():
    """
    Affichage de la page du jeu après une tentative.
    """
    global score, found, display, user_name, life

    mot = get_word()
    longueur = len(mot)
    debug_game(mot)

    # Récupération de la valeur de l'input du formulaire :
    user_input = request.form.get("user_input").lower()

    if user_input:
        if user_input in mot:
            for index in range(len(mot)):
                if mot[index] == user_input:
                    found.extend([user_input])
                    display = display[:index] + user_input + display[index + 1 :]
        else:
            life -= 1

        if display == mot:
            won = True
            return render_template(
                "end.html", user_name=user_name, life=life, secret_word=display, won=won
            )

        if life <= 0:
            won = False
            return render_template(
                "end.html", user_name=user_name, life=life, secret_word=display, won=won, solution=mot
            )

        return render_template(
            "play.html", user_name=user_name, life=life, user_input=user_input, secret_word=display
        )

    return render_template("play.html", user_name=user_name, life=life, secret_word=display)


@app.route("/reset")
def reset():
    """
    Remise à zéro du jeu.
    """
    global mot, won, score, life, found

    mot = False
    won = False
    score = 0
    life = 5
    found = []

    return render_template("home.html", user_name=user_name)


if __name__ == "__main__":
    app.run(debug=True)
