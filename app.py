from flask import Flask, flash, redirect, url_for, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from urllib import request as urllib_request, parse as urllib_parse
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Database and secret key configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_ABITU")
app.config['SECRET_KEY'] = os.getenv("SECRET")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from forms import AssessmentForm  # Make sure this is correctly imported

def sendtelegram(params):
    url = os.getenv("TELEGRAM_URL") + urllib_parse.quote(params)
    content = urllib_request.urlopen(url).read()
    print(content)
    return content

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    product = db.Column(db.String())
    aplication = db.Column(db.String())
    happy = db.Column(db.String())
    overall = db.Column(db.String())
    time = db.Column(db.String())
    project = db.Column(db.String())
    services = db.Column(db.String())
    caption = db.Column(db.String())
    
    def __repr__(self):
        return f"Person('{self.id}', '{self.name}')"


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/clientform', methods=['GET', 'POST'])
def clientform():
    form = AssessmentForm()
    if form.validate_on_submit():
        wait = Person(
            name = form.name.data,  
            product =  form.product.data,   
            aplication = form.aplication.data,
            happy = form.happy.data,
            overall = form.overall.data,
            time = form.time.data,
            project = form.project.data,
            services = form.services.data,
            caption = form.caption.data
        )
        db.session.add(wait)
        db.session.commit()

        
        message = (
            f"New Client Submission:\n"
            f"Name: {wait.name}\n"
            f"Product: {wait.product}\n"
            f"Application: {wait.aplication}\n"
            f"Happy: {wait.happy}\n"
            f"Overall: {wait.overall}\n"
            f"Time: {wait.time}\n"
            f"Project: {wait.project}\n"
            f"Services: {wait.services}\n"
            f"Caption: {wait.caption}\n"
        )
        
        # Send the message to Telegram
        sendtelegram(message)
        # flash("Form submitted successfully")
        return redirect(url_for('submit'))
    
    print(form.errors)
    return render_template('form.html', form=form)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    return render_template('submit.html')


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
