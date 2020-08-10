from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username=StringField('username', validators=[DataRequired()])
    password=PasswordField('password', validators=[DataRequired()])

class EmailPasswordForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('password', validators=[DataRequired()])

class TodoForm(FlaskForm):
    title=StringField('title', validators=[DataRequired()])
    description=TextAreaField('description', validators=[DataRequired()])
    done=BooleanField('done')