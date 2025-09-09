from flask import Flask, render_template, redirect, url_for, request
import jsonlines
import random

app = Flask(__name__)

# Global state
leet_list = []
curr_idx = 0
flip = False
lang = "c++"  # default language
difficulty = "Random"  # default difficulty

def load_problems(difficulty_filter="Random"):
    global leet_list, curr_idx
    leet_list = []
    with jsonlines.open("leetcode-solutions.jsonl") as reader:
        if difficulty_filter == "Random":
            leet_list = [line for line in reader]
        else:
            leet_list = [line for line in reader if line["difficulty"] == difficulty_filter]
    random.shuffle(leet_list)
    curr_idx = 0

@app.route("/", methods=["GET", "POST"])
def index():
    global lang, difficulty
    if request.method == "POST":
        lang = request.form.get("language", "c++")
        difficulty = request.form.get("difficulty", "Random")
        load_problems(difficulty)
        return redirect(url_for("show_question", idx=0))
    return render_template("index.html", languages=["c++", "Python", "Java", "Javascript"], difficulties=["Random","Easy","Medium","Hard"])

@app.route("/question/<int:idx>")
def show_question(idx):
    global curr_idx, flip, lang
    curr_idx = idx
    if idx < 0 or idx >= len(leet_list):
        return "No more problems!", 404
    problem = leet_list[idx]
    return render_template(
        "question.html",
        problem=problem,
        idx=idx,
        total=len(leet_list),
        show_answer=flip,
        lang=lang,
    )

@app.route("/flip/<int:idx>")
def flip_card(idx):
    global flip
    flip = not flip
    return redirect(url_for("show_question", idx=idx))

@app.route("/next/<int:idx>")
def next_question(idx):
    return redirect(url_for("show_question", idx=idx + 1))

@app.route("/prev/<int:idx>")
def prev_question(idx):
    return redirect(url_for("show_question", idx=idx - 1))

if __name__ == "__main__":
    app.run(debug=True)
