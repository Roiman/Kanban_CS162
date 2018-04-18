__author__ = 'roiman'

# the forms, connection to db, and the models
# are taken from the models file
from kanban_models import Task, User, LoginForm, EmailPasswordForm, session

from flask import Flask, render_template, request, redirect, url_for,  flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import os

# creating the app instance
app = Flask(__name__)

#defining the login manager and initiating with the app
login_manager = LoginManager()
login_manager.init_app(app)
# when trying to access pages with unauthorized user,
# redirects to the login page
login_manager.login_view = "login"


# making a secret key for logging in?
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# close connections to the database on teardown
@app.teardown_appcontext
def close_db(exception):
    session.close()

# a form to be used for logging users in. Could be moved somewhere else
@login_manager.user_loader
def get_user(user_id):
    #Given uid return the associated User object.
    return session.query(User).filter(User.id == str(user_id)).first()

# method/route for user creation
@app.route('/create', methods=["GET", "POST"])
def create_account():
    form = EmailPasswordForm()
    error = "Usernames and passwords must be at least 4 characters long"
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            password = form.password.data
        )
        session.add(user)
        session.commit()
        return redirect(url_for("index"))

    # TODO: show error message when fields are too short
    # TODO: show error message when username exists
    # TODO: make usernames not case sensitive.
    # --> Roiman and roiman are different users right now
    return render_template("create.html", form=form, error=error)


# method/route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = "Please Log In"
    if request.method == 'POST':
        username = request.form['username']
        pswd = request.form['password']
        user = session.query(User).filter_by(username=username, password=pswd).first()
        if user:
            login_user(get_user(user.id))
            return redirect(url_for('index'))
        error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


# adding login required since otherwise this page gives an error
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# the kanban board laoding
@app.route('/', methods=['GET'])
@login_required
def index():
	all_tasks = session.query(Task).filter_by(user_id=current_user.id).all()
	todos = session.query(Task).filter_by(statusID=0, user_id=current_user.id).all()
	doings = session.query(Task).filter_by(statusID=1, user_id=current_user.id).all()
	dones = session.query(Task).filter_by(statusID=2, user_id=current_user.id).all()

	return render_template('Kanban.html', todos=todos, doings=doings, dones=dones, all_tasks=all_tasks)


# adding a task
@app.route('/add', methods=['POST'])
def add():
	todo = Task(title=request.form['task_title'], text=request.form['task_description'], statusID=request.form['task_label'], user_id=current_user.id)
	session.add(todo)
	session.commit()

	return redirect(url_for('index'))


# upfating tasks directly
@app.route('/update', methods=['POST'])
def update():
	todo = session.query(Task).filter_by(id=int(request.form['task_name'])).first()
	todo.statusID=request.form['update_value']

	session.commit()
	
	return redirect(url_for('index'))

# the following methods are used to change task status
@app.route('/doing/<task_id>', methods=['GET','POST'])
def doing(task_id):
    task = session.query(Task).filter_by(id=task_id).first()
    task.statusID=1
    session.commit()
    
    return redirect(url_for('index'))

@app.route('/done/<task_id>', methods=['GET','POST'])
def done(task_id):
    task = session.query(Task).filter_by(id=task_id).first()
    task.statusID=2
    session.commit()
    
    return redirect(url_for('index'))

@app.route('/Delete_Task/<id>', methods=['GET','DELETE'])
def delete_task(id):
    task = session.query(Task).filter_by(id=id).first()
    session.delete(task)
    session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(debug=True)
