from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

# key name to store answers in the session;
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def survey_start():
    """Display survey title, instructions, start button"""

    return render_template('start.html', survey=survey)

@app.route('/session', methods=["POST"])
def start_session():
    """Clear the session of responses."""
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route('/questions/<int:que_num>')
def get_question(que_num):
    """Display current survey question"""
    responses = session.get(RESPONSES_KEY)

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
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # survey is complete, thank you page
        return redirect("/complete")

    else:
        # logic in questions route for handling curr question num
        return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""
    responses = session.get(RESPONSES_KEY)
    
    questions = survey.questions
    return render_template("complete.html", responses=responses, questions=questions)