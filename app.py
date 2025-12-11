from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy()
db.init_app(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deadline = db.Column(db.String)
    tasktext = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        taskItem = Task(
            tasktext = request.form['task'],
            deadline = request.form['deadline'],
            completed = False
        )
        db.session.add(taskItem)
        db.session.commit()
        return redirect('/')
    else:
        tasklist = db.session.execute(db.select(Task).order_by(Task.deadline)).scalars()
        return render_template('index.html', tasklist=tasklist)

@app.route('/completed', methods=['GET', 'POST'])
def completed():
    if request.method == 'POST':
        marked_task = request.form['select']
        task = db.session.execute(db.select(Task).where(Task.id == marked_task)).scalar()
        task.completed = True
        db.session.commit()
        return redirect('/completed')
    else:
        taskdone = db.session.execute(db.select(Task).where(Task.completed == True).order_by(Task.deadline)).scalars()
        return render_template('completed.html', taskdone=taskdone)