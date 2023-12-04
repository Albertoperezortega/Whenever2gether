from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, FileField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, FileField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Register form
class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Event form
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=30)])
    description = TextAreaField('Description', validators=[DataRequired()])
    photo = FileField('Photo')
    time = DateTimeField('Time of the event', validators=[DataRequired()], format='%d/%m/%Y %H:%M',)
    submit = SubmitField('Create')
    
