from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "geheimespasswort"

ROUND_CARDS = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        players = [p for p in request.form.getlist("player") if p.strip()]
        if len(players) == 0:
            return render_template("index.html", error="Mindestens ein Name nötig.")
        session["players"] = players
        session["scores"] = {p: [] for p in players}
        session["round"] = 0
        if "bier" not in session:
            session["bier"] = 0  # Bier-Zähler initialisieren
        return redirect(url_for("game"))
    return render_template("index.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    players = session.get("players")
    scores = session.get("scores")
    current_round = session.get("round", 0)
    bier_count = session.get("bier", 0)

    if players is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        # Punkte speichern
        for p in players:
            val = request.form.get(p)
            try:
                val = int(val)
            except:
                val = 0
            scores[p].append(val)
        session["scores"] = scores
        session["round"] = current_round + 1

        if session["round"] >= len(ROUND_CARDS):
            return redirect(url_for("summary"))

        return redirect(url_for("game"))

    cards = ROUND_CARDS[current_round]
    return render_template("game.html", players=players, round_num=current_round+1,
                           cards=cards, total_rounds=len(ROUND_CARDS), bier=bier_count)

@app.route("/summary")
def summary():
    scores = session.get("scores")
    if not scores:
        return redirect(url_for("index"))
    totals = {p: sum(v) for p, v in scores.items()}
    winner = max(totals, key=totals.get)
    bier_count = session.get("bier", 0)
    return render_template("summary.html", totals=totals, winner=winner, bier=bier_count)

# Neuer Route für Bier-Zähler
@app.route("/bier", methods=["POST"])
def bier():
    if "bier" not in session:
        session["bier"] = 0
    session["bier"] += 1
    return jsonify({"bier": session["bier"]})

if __name__ == "__main__":
    app.run(debug=True)
