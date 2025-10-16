from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Kartenfolge als Gedankenstütze
card_pattern = [1,2,3,4,5,5,4,3,2,1]
current_round = 0
max_rounds = len(card_pattern)
beer_count = 0
final_result = False
game_started = False  # NEU: Flag, ob das Spiel gestartet wurde

# Spielerverwaltung
players = []
scores = {}

@app.route("/", methods=["GET", "POST"])
def index():
    global current_round, beer_count, final_result, game_started

    # Spieler hinzufügen (nur vor Spielstart)
    if request.method == "POST" and "add_player" in request.form and not game_started:
        if len(players) < 8:
            name = request.form.get("player_name")
            if name and name not in players:
                players.append(name)
                scores[name] = 0
        return redirect("/")

    # Spiel starten Button
    if request.method == "POST" and "start_game" in request.form and len(players) > 0:
        game_started = True
        return redirect("/")

    if not game_started:
        return render_template("index.html", players=players, game_started=game_started)

    # Punkte aktualisieren
    if request.method == "POST" and "update_scores" in request.form:
        for p in players:
            if p in request.form:
                try:
                    points = int(request.form[p])
                    scores[p] += points
                except ValueError:
                    pass
        return redirect("/")

    # Runde abschließen
    if request.method == "POST" and "new_round" in request.form:
        current_round += 1
        if current_round < max_rounds:
            pass
        else:
            final_result = True
        return redirect("/")

    # Bier zählen
    if request.method == "POST" and "add_beer" in request.form:
        beer_count += 1
        return redirect("/")

    # Bier zurücksetzen
    if request.method == "POST" and "reset_beer" in request.form:
        beer_count = 0
        return redirect("/")

    # Spiel zurücksetzen
    if request.method == "POST" and "reset_game" in request.form:
        players.clear()
        scores.clear()
        current_round = 0
        beer_count = 0
        final_result = False
        game_started = False
        return redirect("/")

    return render_template("index.html",
                           players=players,
                           scores=scores,
                           current_round=current_round,
                           max_rounds=max_rounds,
                           card_count=card_pattern[current_round] if current_round < max_rounds else 0,
                           beer_count=beer_count,
                           final_result=final_result,
                           game_started=game_started)

if __name__ == "__main__":
    app.run(debug=True)
