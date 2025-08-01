# from flask import Flask, request, render_template, redirect
# import json
# import os

# app = Flask(__name__)


# def load_questions():
#     with open('questions.json') as f:
#         return json.load(f)

# def save_response(username, q_id, option_id):
#     data = {}
#     if os.path.exists("answers.json"):
#         with open("answers.json") as f:
#             data = json.load(f)
#     if username not in data:
#         data[username] = {}
#     data[username][q_id] = option_id
#     with open("answers.json", "w") as f:
#         json.dump(data, f)


# def submit(questions, username):
#     q_id = request.form["question_id"]
#     option_id = request.form["option"]
#     save_response(username, q_id, option_id)

#     next_q_id = str(int(q_id) + 1)
#     if next_q_id in questions:
#         return redirect(f"/?user={username}&q_id={next_q_id}")
#     else:
#         return render_template("complete_quiz.html", username=username)




# def return_questions(questions, username):
#     q_id = request.args.get("q_id", "1")
#     question_data = questions[q_id][0]
#     return render_template("quiz.html", question=question_data, username=username)



# @app.route("/", methods=["GET", "POST"])
# def quiz():
#     questions = load_questions()
#     username = request.args.get("user", "")

#     if not username:
#         return render_template("start_quiz.html")

#     if request.method == "POST":
#         return submit(questions, username)

#     return return_questions(questions, username)


# def get_all_usernames():
#     if os.path.exists("answers.json"):
#         with open("answers.json") as f:
#             data = json.load(f)
#             return list(data.keys())
#     return []




# def generate_results(username):
#     with open("answers.json") as f:
#         all_answers = json.load(f)

#     responses = all_answers.get(username, {})

#     questions = load_questions()
#     score = 0
#     results = []

#     for q_id, q_data in questions.items():
#         q = q_data[0]
#         user_ans = responses.get(q_id)

#         if user_ans == q["correct_option"]:
#             score += 1

#         results.append({
#             "question": q["question_string"],
#             "options": q["options"],
#             "correct_option": q["correct_option"],
#             "user_option": user_ans
#         })

#     return score, results



# @app.route("/preview")
# def preview():
#     username = request.args.get("user", "")
#     if not username:
#         users = get_all_usernames()
#         return render_template("preview.html", username=None, users=users)
#     score, results = generate_results(username)
#     return render_template("preview.html", username=username, score=score, results=results, users=[])




# if __name__ == "__main__":
#     app.run()



# def generate_results(username):
#     with open("answers.json") as f:
#         responses = json.load(f).get(username, {})

#     questions = load_questions()
#     score = 0
#     results = []

#     for q_id, question_list in questions.items():
#         question = question_list[0]
#         correct = question["correct_option"]
#         user_ans = responses.get(q_id)

#         if user_ans == correct:
#             score += 1

#         results.append({
#             "question": question["question_string"],
#             "options": question["options"],
#             "correct_option": correct,
#             "user_option": user_ans
#         })

#     return score, results

# @app.route("/preview")
# def preview():
#     username = request.args.get("user", "")
#     if not username:
#         return redirect("/")

#     score, results = generate_results(username)
#     return render_template("preview.html", username=username, score=score, results=results)





from flask import Flask, request, render_template, redirect
import json
import os

app = Flask(__name__)

def load_questions():
    with open('questions.json') as f:
        return json.load(f)

def save_response(username, q_id, option_id):
    data = {}
    if os.path.exists("answers.json"):
        with open("answers.json") as f:
            try:
                data = json.load(f)
                if not isinstance(data, dict):
                    data = {}
            except:
                data = {}
    if username not in data:
        data[username] = {}
    data[username][q_id] = option_id
    with open("answers.json", "w") as f:
        json.dump(data, f)

def submit(questions, username):
    q_id = request.form["question_id"]
    option_id = request.form["option"]
    save_response(username, q_id, option_id)

    next_q_id = str(int(q_id) + 1)
    if next_q_id in questions:
        return redirect(f"/?user={username}&q_id={next_q_id}")
    else:
        score, results = generate_results(username)
        return render_template("preview.html", username=username, score=score, results=results)

def return_questions(questions, username):
    q_id = request.args.get("q_id", "1")
    if q_id not in questions:
        score, results = generate_results(username)
        return render_template("preview.html", username=username, score=score, results=results)
    question_data = questions[q_id][0]
    return render_template("quiz.html", question=question_data, username=username)

@app.route("/", methods=["GET", "POST"])
def quiz():
    questions = load_questions()
    username = request.args.get("user", "")
    if not username:
        return render_template("start_quiz.html")
    if request.method == "POST":
        return submit(questions, username)
    return return_questions(questions, username)

def generate_results(username):
    with open("answers.json") as f:
        all_answers = json.load(f)
    responses = all_answers.get(username, {})
    questions = load_questions()
    score = 0
    results = []
    for q_id, q_data in questions.items():
        q = q_data[0]
        user_ans = responses.get(q_id)
        if user_ans == q["correct_option"]:
            score += 1
        results.append({
            "question": q["question_string"],
            "options": q["options"],
            "correct_option": q["correct_option"],
            "user_option": user_ans
        })
    return score, results

if __name__ == "__main__":
    app.run()
