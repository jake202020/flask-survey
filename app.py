from flask import Flask, render_template
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def survey_start():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('start.html', title=title, instructions=instructions)

@app.route('/questions/<que_num>')
def get_question(que_num):
    return render_template("form.html", que_num=que_num)