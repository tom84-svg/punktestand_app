from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Spiel-Variablen ---
players = []
scores = {}
current_round = 0
max_rounds = 11  # 1,2,3,4,5,5,4,3,2,1
card_sequence = [1,2,3,4,5,5,4,3,2,1]
card_count = 0
beer_count = 0
game_started = False
final_result = False

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    global players, scores, current_round, card_count, beer_count, game_started, final_result

    if request.method == "POST":
        # Spieler hinzufügen (nur vor Spielstart)
        if "add_player" in request.form and not game_started:
            name = request.form.get("player_name", "").strip()
            if name and name not in players and len(players) < 8:
                players.append(name)
                scores[name] = 0

        # Spiel starten
        if "start_game" in request.form and len(players) > 0:
            game_started = True
            current_round = 0
            card_count = card_sequence[current_round]

        # Punkte aktualisieren
        if "update_scores" in request.form:
            for player in players:
                try:
                    val = int(request.form.get(player, 0))
                    scores[player] += val
                except:
                    pass

        # Neue Runde abschließen
        if "new_round" in request.form and game_started and not final_result:
            current_round += 1
            if current_round < len(card_sequence):
                card_count = card_sequence[current_round]
            else:
                card_count = card_sequence[-1]
                final_result = True

        # Bier zählen
        if "add_beer" in request.form:
            beer_count += 1

        # Bier zurücksetzen
        if "reset_beer" in request.form:
            beer_count = 0

        # Spiel zurücksetzen
        if "reset_game" in request.form:
            players = []
            scores = {}
            current_round = 0
            card_count = 0
            beer_count = 0
            game_started = False
            final_result = False

    return render_template("index.html",
                           players=players,
                           scores=scores,
                           current_round=current_round,
                           card_count=card_count,
                           beer_count=beer_count,
                           game_started=game_started,
                           final_result=final_result,
                           max_rounds=len(card_sequence))

# --- Main ---
if __name__ == "__main__":
    app.run(debug=True)
