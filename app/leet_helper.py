import jsonlines
import random

leet_list = []

def reset(difficulty="Random"):
    global leet_list
    leet_list = []
    with jsonlines.open('leetcode-solutions.jsonl') as reader:
        if difficulty == "Random":
            leet_list = [line for line in reader]
        else:
            leet_list = [line for line in reader if line["difficulty"] == difficulty]
    random.shuffle(leet_list)
    return leet_list

def get_answers(lang="c++"):
    answers = []
    with jsonlines.open('leetcode-solutions.jsonl') as reader:
        for line in reader:
            answers.append(line["answer"][lang])
    return answers
