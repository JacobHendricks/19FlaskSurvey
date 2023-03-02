from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def start_page():
    """Return Start Page."""

    return render_template("start.html", title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session["responses_key"] = []

    return redirect("/questions/0")


@app.route("/questions/<int:id>")
def question_page(id):
    responses = session["responses_key"]

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) != id):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    """Return Question page"""
    return render_template("questions.html", question=satisfaction_survey.questions[id].question, choices=satisfaction_survey.questions[id].choices)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    responses = session['responses_key']
    responses.append(choice)
    session['responses_key'] = responses
    print("***************************")
    print(responses)
    print(session['responses_key'])
    print("***************************")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    '''Show completion page'''
    responses = session["responses_key"]
    return render_template("completion.html", responses=responses)
