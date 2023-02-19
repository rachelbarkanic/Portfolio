from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, StringField, SubmitField, TextAreaField, BooleanField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from models import User

class CreateUserForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('E-mail Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message= 'Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Create User')

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('This email is already being used')
    
    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('This username is already being used')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')