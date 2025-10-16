from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "geheimespasswort"  # für Sessions - in Prod anders setzen

# Runden / Kartenfolge
ROUND_CARDS = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
MAX_ROUNDS = len(ROUND_CARDS)

BIER_FILE = "bier_count.txt"

def load_bier_count():
    if not os.path.exists(BIER_FILE):
        return 0
    try:
        with open(BIER_FILE, "r") as f:
            return int(f.read().strip() or 0)
    except:
        return 0

def save_bier_count(count):
    with open(BIER_FILE, "w") as f:
        f.write(str(count))

# initial persistent bier count
bier_count = load_bier_count()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Spieler einlesen (bis 8)
        players = [p.strip() for p in request.form.getlist("player") if p.strip()]
        if len(players) == 0:
            return render_template("index.html", error="Bitte mindestens einen Namen eingeben.")
        if len(players) > 8:
            players = players[:8]
        # Session initialisieren
        session["players"] = players
        session["scores"] = {p: [] for p in players}
        session["round"] = 0  # index der Runde 0..9
        # Bier in session falls nicht vorhanden (persistenz in file)
        session["bier"] = bier_count
        return redirect(url_for("game"))
    return render_template("index.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    players = session.get("players")
    if players is None:
        return redirect(url_for("index"))

    scores = session.get("scores", {p: [] for p in players})
    current_round = session.get("round", 0)
    bier = session.get("bier", load_bier_count())

    # POST: Punkte dieser Runde speichern (einfache Werte)
    if request.method == "POST":
        for p in players:
            val = request.form.get(p, "0").strip()
            try:
                val = int(val)
            except:
                val = 0
            scores.setdefault(p, []).append(val)
        session["scores"] = scores
        # Runde erhöhen
        current_round += 1
        session["round"] = current_round
        # Wenn fertig
        if current_round >= MAX_ROUNDS:
            return redirect(url_for("summary"))
        return redirect(url_for("game"))

    # aktuelle Kartenzahl aus ROUND_CARDS
    if 0 <= current_round < MAX_ROUNDS:
        cards = ROUND_CARDS[current_round]
    else:
        cards = 0

    # Gesamtsummen berechnen für Anzeige
    totals = {p: sum(scores.get(p, [])) for p in players}

    return render_template("game.html",
                           players=players,
                           round_num=current_round + 1,
                           total_rounds=MAX_ROUNDS,
                           cards=cards,
                           totals=totals,
                           bier=bier)

@app.route("/summary")
def summary():
    scores = session.get("scores")
    players = session.get("players")
    bier = session.get("bier", load_bier_count())
    if not scores or not players:
        return redirect(url_for("index"))
    totals = {p: sum(scores.get(p, [])) for p in players}
    sorted_scores = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    winner = sorted_scores[0][0] if sorted_scores else None
    return render_template("summary.html", totals=sorted_scores, winner=winner, bier=bier)

# Bier-Button endpoint: erhöht persistent Zähler (Datei + session)
@app.route("/bier", methods=["POST"])
def bier():
    # lade aktuell aus file, erhöhe und speichere
    current = load_bier_count()
    current += 1
    save_bier_count(current)
    session["bier"] = current
    # nach Klick zurück zur aktuellen Runde
    return redirect(url_for("game"))

if __name__ == "__main__":
    app.run(debug=True)
