from flask import Flask, render_template, request, flash, session, redirect, url_for, abort
from models import connect_to_db, db, User
from forms import CreateUserForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user

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

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('See ya later!')
    return redirect(url_for('homepage'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('You are logged in!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('welcome_user')
            
            return redirect(next)
    
    return render_template('login.html', form = form)




@app.route('/users', methods=['GET', 'POST'])
def create_user():
    '''Create a new user'''
    form = CreateUserForm()

    if form.validate_on_submit():
        user = User(username = form.username.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            email = form.email.data,
            password = form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')

        return redirect(url_for('login'))
        
    return render_template('register.html', form = form)


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