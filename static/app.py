from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

rounds = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
players = []
scores = []
current_round = 0

@app.route("/", methods=["GET", "POST"])
def index():
    global players, scores, current_round
    if request.method == "POST":
        players = [p for p in request.form.getlist("player") if p.strip()]
        scores = [0] * len(players)
        current_round = 0
        return redirect(url_for("game"))
    return render_template("index.html")

@app.route("/runde", methods=["GET", "POST"])
def game():
    global current_round, scores
    if current_round >= len(rounds):
        return redirect(url_for("summary"))

    if request.method == "POST":
        for i, _ in enumerate(scores):
            scores[i] += int(request.form.get(f"points_{i}", 0))
        current_round += 1
        if current_round >= len(rounds):
            return redirect(url_for("summary"))

    return render_template("game.html",
                           round_number=current_round + 1,
                           total_rounds=len(rounds),
                           card_count=rounds[current_round],
                           players=players)

@app.route("/summary")
def summary():
    result = list(zip(players, scores))
    result.sort(key=lambda x: x[1], reverse=True)
    return render_template("summary.html", results=result)

@app.route('/manifest.json')
def manifest():
    return send_from_directory(os.path.dirname(__file__), 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service_worker.js')

if __name__ == "__main__":
    app.run(debug=True)
