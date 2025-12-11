from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from projectsecrets import app_secrets
from functions import all_quotes
import random

app = Flask(__name__)
app.secret_key = app_secrets.app_key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy()
db.init_app(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deadline = db.Column(db.String)
    tasktext = db.Column(db.String, nullable=False)
    quote = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        random_quote = random.choice(all_quotes())
        taskItem = Task(
            tasktext = request.form['task'],
            deadline = request.form['deadline'],
            quote = random_quote[0],
            author = random_quote[1],
            completed = False
        )
        db.session.add(taskItem)
        db.session.commit()
        return redirect('/')
    else:
        tasklist = db.session.execute(db.select(Task).order_by(Task.deadline)).scalars()
        # random_quote = random.choice(all_quotes())
        return render_template('index.html', tasklist=tasklist)

@app.route('/completed', methods=['GET', 'POST'])
def completed():
    tasklist = db.session.execute(db.select(Task).where(Task.completed == False).order_by(Task.deadline)).scalars()
    if request.method == 'POST':
        marked_task = request.form['select']
        task = db.session.execute(db.select(Task).where(Task.id == marked_task)).scalar()
        task.completed = True
        db.session.commit()
        return redirect('/completed')
    else:
        taskdone = db.session.execute(db.select(Task).where(Task.completed == True).order_by(Task.deadline)).scalars()
        return render_template('completed.html', taskdone=taskdone, tasklist=tasklist)

