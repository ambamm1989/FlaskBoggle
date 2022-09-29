from crypt import methods
from urllib import response
from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = abcd123

@app.route("/")
def homepage():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    newplays = session.get("newplays")
    return render_template("index.html", board = board, highscore = highscore, newplays = newplays)

@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    newplays = session.get("newplays", 0)
    session['newplays'] = newplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(recordBroken = score > highscore)
