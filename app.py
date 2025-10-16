from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Variablen global
players = []
scores = {}
current_round = 1
card_sequence = [1,2,3,4,5,5,4,3,2,1]
beer_count = 0
game_started = False
final_result = False

@app.route("/", methods=["GET", "POST"])
def index():
    global players, scores, current_round, beer_count, game_started, final_result

    # Spieler hinzufügen
    if request.method == "POST":
        if "add_player" in request.form:
            name = request.form.get("player_name", "").strip()
            if name and name not in players and len(players) < 8:
                players.append(name)
                scores[name] = 0
            return redirect("/")

        # Punkte aktualisieren
        for player in players:
            if player in request.form:
                try:
                    scores[player] += int(request.form[player])
                except:
                    pass
        if "update_scores" in request.form:
            return redirect("/")

        # Neue Runde
        if "new_round" in request.form:
            if current_round < len(card_sequence):
                current_round += 1
            else:
                final_result = True
            return redirect("/")

        # Bier zählen
        if "beer_count_btn" in request.form:
            beer_count += 1
            return redirect("/")

        # Bier zurücksetzen
        if "reset_beer" in request.form:
            beer_count = 0
            return redirect("/")

        # Spiel zurücksetzen
        if "reset_game" in request.form:
            players = []
            scores = {}
            current_round = 1
            beer_count = 0
            game_started = False
            final_result = False
            return redirect("/")

    # Start des Spiels
    if len(players) > 0:
        game_started = True

    return render_template("index.html",
                           players=players,
                           scores=scores,
                           current_round=current_round,
                           card_count=card_sequence[current_round-1],
                           beer_count=beer_count,
                           game_started=game_started,
                           final_result=final_result,
                           max_rounds=len(card_sequence))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
