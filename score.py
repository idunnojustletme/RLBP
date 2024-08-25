# score.py

previous_score = 0
score_increase = 0


def calculate_score_increase(value):
    global previous_score, score_increase
    current_score = value
    if current_score != previous_score:
        print(f"Current score: {current_score}")
    score_increase = current_score - previous_score
    if score_increase > 0:
        print(f"Score increased by: {score_increase}")
    previous_score = current_score
    return score_increase
