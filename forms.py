from wtforms import DateField, Form, BooleanField, StringField, PasswordField, validators, SubmitField, SelectField, IntegerField,PasswordField, SearchField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
# from app import Person

class AssessmentForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    product = SelectField('tag', choices=[('Tag','Tag'),('Very Satisfied', 'Very Satisfied'), ('Satisfied','Satisfied'), ('Neutral','Neutral'), ('Unsatisfied','Unsatisfied'), ('Very Unsatisfied','Very Unsatisfied') ], default=None )
    aplication = SelectField('tag', choices=[('Tag','Tag'),('Exceeded expectations', 'Exceeded expectations'), ('Met expectations','Met expectations'), ('Fell short of expectations','Fell short of expectations') ], default=None )
    happy = SelectField('tag', choices=[('Tag','Tag'),('Very Satisfied', 'Very Satisfied'), ('Satisfied','Satisfied'), ('Neutral','Neutral'), ('Unsatisfied','Unsatisfied'), ('Very Unsatisfied','Very Unsatisfied') ], default=None )
    overall = SelectField('tag', choices=[('Tag','Tag'),('Very Satisfied', 'Very Satisfied'), ('Satisfied','Satisfied'), ('Neutral','Neutral'), ('Unsatisfied','Unsatisfied'), ('Very Unsatisfied','Very Unsatisfied') ], default=None )
    time = SelectField('tag', choices=[('Tag','Tag'),('Yes', 'Yes'), ('No','No'), ('Needed More Time','Needed More Time')], default=None )
    project = SelectField('tag', choices=[('Tag','Tag'),('Very Satisfied', 'Very Satisfied'), ('Satisfied','Satisfied'), ('Neutral','Neutral'), ('Unsatisfied','Unsatisfied'), ('Very Unsatisfied','Very Unsatisfied') ], default=None )
    services = SelectField('tag', choices=[('Tag','Tag'),('Yes', 'Yes'), ('No','No'), ('Needed More Time','Needed More Time')], default=None )
    caption = StringField('caption', validators=[DataRequired()])
    
   
    submit = SubmitField('submit')
    