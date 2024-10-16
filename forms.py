from wtforms import DateField, Form, BooleanField, StringField, PasswordField, validators, SubmitField, SelectField, IntegerField,PasswordField, SearchField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange


class AssessmentForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    product = SelectField('tag', choices=[('Tag','Tag'),('Very Satisfied', 'Very Satisfied'), ('Satisfied','Satisfied'), ('Neutral','Neutral'), ('Unsatisfied','Unsatisfied'), ('Very Unsatisfied','Very Unsatisfied') ], default=None )
    aplication = SelectField('tag', choices=[('Tag','Tag'),('Exceeded expectations', 'Exceeded expectations'), ('Met expectations','Met expectations'), ('Fell short of expectations','Fell short of expectations') ], default=None )
    happy = SelectField('tag', choices=[('Tag','Tag'),('Web/App Developement', 'Web/App Developement'), ('Graphic Design','Graphic Design'), ('Digital Marketing','Digital Marketing'), ('All The Above','All The Above')], default=None )
    overall = SelectField('tag', choices=[('Tag','Tag'),('Very Satisfied', 'Very Satisfied'), ('Satisfied','Satisfied'), ('Neutral','Neutral'), ('Unsatisfied','Unsatisfied'), ('Very Unsatisfied','Very Unsatisfied') ], default=None )
    time = SelectField('tag', choices=[('Tag','Tag'),('Yes', 'Yes'), ('No','No'), ('Needed More Time','Needed More Time')], default=None )
    project = SelectField('tag', choices=[('Tag','Tag'),('Very Satisfied', 'Very Satisfied'), ('Satisfied','Satisfied'), ('Neutral','Neutral'), ('Unsatisfied','Unsatisfied'), ('Very Unsatisfied','Very Unsatisfied') ], default=None )
    services = SelectField('tag', choices=[('Tag','Tag'),('Yes', 'Yes'), ('No','No'), ('Maybe', 'Maybe')], default=None )
    caption = StringField('caption', validators=[DataRequired()])
    
   
    submit = SubmitField('submit')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    