from flask import Flask, render_template, request, redirect, url_for
import jsonlines
import random
import os

app = Flask(__name__)

# Load JSON file (outside app folder)
JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "leetcode-solutions.jsonl")

# Global variables
leet_list = []
curr_idx = 0

def load_questions(difficulty="Random"):
    global leet_list, curr_idx
    leet_list = []
    with jsonlines.open(JSON_PATH) as reader:
        for line in reader:
            if difficulty == "Random" or line["difficulty"] == difficulty:
                leet_list.append(line)
    random.shuffle(leet_list)
    curr_idx = 0

@app.route("/", methods=["GET", "POST"])
def index():
    global curr_idx
    if request.method == "POST":
        difficulty = request.form.get("difficulty", "Random")
        load_questions(difficulty)
    if not leet_list:
        load_questions()
    return redirect(url_for("navigate", direction="current", idx=0))

@app.route("/navigate/<direction>/<int:idx>")
def navigate(direction, idx):
    global curr_idx
    if direction == "next" and idx < len(leet_list) - 1:
        curr_idx = idx + 1
    elif direction == "prev" and idx > 0:
        curr_idx = idx - 1
    elif direction == "current":
        curr_idx = idx

    question = leet_list[curr_idx] if leet_list else None

    return render_template(
        "question.html",
        problem=question,
        idx=curr_idx,
        max_idx=len(leet_list) - 1
    )

if __name__ == "__main__":
    app.run(debug=True)

