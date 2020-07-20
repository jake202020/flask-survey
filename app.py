from flask import Flask, request, render_template, redirect, flash
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
debug = DebugToolbarExtension(app)

"""Store user responses"""
responses = []

@app.route('/')
def survey_start():
    """Display survey title, instructions, start button"""

    return render_template('start.html', survey=survey)

@app.route('/questions/<int:que_num>')
def get_question(que_num):
    """Display current survey question"""
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        # survey is complete, thank you page
        return redirect("/complete")

    if (len(responses) != que_num):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {que_num}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[que_num]
    return render_template("form.html", que_num=que_num, question=question)

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses.append(choice)

    if (len(responses) == len(survey.questions)):
        # survey is complete, thank you page
        return redirect("/complete")

    else:
        # logic in questions route for handling curr question num
        return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("complete.html")