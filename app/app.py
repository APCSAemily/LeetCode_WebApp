from flask import Flask, render_template, request, redirect, url_for
import jsonlines
import random
import os
import re

app = Flask(__name__)

# Load JSON file (outside app folder)
JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "leetcode-solutions.jsonl")

# Global variables
leet_list = []
curr_idx = 0

def format_markdown(text):
    if not text:
        return ""
    
    # Bold: **text** → <strong>text</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Italic: _text_ → <em>text</em>
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    
    # Inline code: `code` → <code>code</code>
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Lists: lines starting with * or - → <ul><li>...</li></ul>
    lines = text.split('\n')
    html_lines = []
    in_list = False
    for line in lines:
        if re.match(r'^\s*[\*\-]\s+', line):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            item = re.sub(r'^\s*[\*\-]\s+', '', line)
            html_lines.append(f'<li>{item}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(line)
    if in_list:
        html_lines.append('</ul>')
    
    text = '<br>'.join(html_lines)
    return text


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

    # Format content and explanation
    if question:
        question['formatted_content'] = format_markdown(question['content'])
        if question.get('answer') and question['answer'].get('explanation'):
            question['answer']['formatted_explanation'] = format_markdown(question['answer']['explanation'])

    # Always show the question when navigating
    return render_template(
        "question.html",
        problem=question,
        idx=curr_idx,
        total=len(leet_list),
        flip=False  # <- important
    )

@app.route("/flip/<int:idx>")
def flip(idx):
    global curr_idx
    curr_idx = idx

    question = leet_list[curr_idx]

    # Format content and explanation
    if question:
        question['formatted_content'] = format_markdown(question['content'])
        if question.get('answer') and question['answer'].get('explanation'):
            question['answer']['formatted_explanation'] = format_markdown(question['answer']['explanation'])

    # Determine flip state from query param ?flip=true/false
    show_answer = request.args.get('flip', 'true').lower() == 'true'

    return render_template(
        "question.html",
        problem=question,
        idx=curr_idx,
        total=len(leet_list),
        flip=show_answer
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

