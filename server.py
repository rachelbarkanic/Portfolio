from flask import Flask, render_template, request, flash, session, redirect, url_for
from models import connect_to_db, db, User
from forms import CreateUserForm
from flask_login import LoginManager

from jinja2 import StrictUndefined


login_manager = LoginManager()


app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def homepage():
    '''View home page'''
    create_user_form = CreateUserForm()

    return render_template('homepage.html', create_user_form = create_user_form)


@app.route('/users', methods=['GET', 'POST'])
def create_user():
    '''Create a new user'''
    username = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.get_user_by_email(email)

    if user:
        flash('Sorry, that email already exists. Try another.')
    else:
        user = User.create_user(username, first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in!')
    return redirect('/')


@app.route('/all_users')
def all_users():
    '''A page listing all users that have a profile on portfoliocraft'''
    return render_template('all_users.html')

@app.route('/resume/<user_id>')
def view_resume():
    '''View Resume for specific person'''
    # Need to make this so must be logged in to edit
    return render_template('resume.html')

@app.route('/projects')
def view_projects():
    '''View projects for specific person'''

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='localhost', port = 4321, debug=True)