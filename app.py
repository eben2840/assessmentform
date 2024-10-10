from flask import Flask, flash, redirect, url_for, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date
from urllib import request as urllib_request, parse as urllib_parse
from dotenv import load_dotenv
load_dotenv()
from flask_login import UserMixin, login_user, current_user, logout_user, login_required, LoginManager
from datetime import datetime
import qrcode
import os
app = Flask(__name__)

# Database and secret key configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_ABITU")
app.config['SECRET_KEY'] = os.getenv("SECRET")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# from forms import AssessmentForm, RegistrationForm, LoginForm 
from forms import *

def sendtelegram(params):
    url = os.getenv("TELEGRAM_URL") + urllib_parse.quote(params)
    content = urllib_request.urlopen(url).read()
    print(content)
    return content

class Person(db.Model):
    __tablename__ = 'person'
    __table_args__ = {'extend_existing': True}
    
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
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
class CheckIn(db.Model):
    __tablename__ = 'checkin'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime, nullable=True)

    # Create a backref to access user from check-in
    user = db.relationship('User', backref='checkins')


# CheckIn model
class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime, nullable=True)

    # Relationship to the User model
    user = db.relationship('User', backref='checkins')
    
    
    

# Route to create an account
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Route to log in
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html')

# Dashboard where users can generate QR codes
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

# Route to generate a QR code
# @app.route("/generate_qr")
# @login_required
# def generate_qr():
#     user = current_user
#     qr_code_data = url_for('scan_qr', user_id=user.id, _external=True)
#     img = qrcode.make(qr_code_data)
    
#     # Save the QR code image
#     qr_code_path = f'static/qr_codes/{user.username}_qr.png'
#     os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
#     img.save(qr_code_path)

#     return render_template('generate_qr.html', qr_code_path=qr_code_path)
@app.route("/generate_qr")
@login_required
def generate_qr():
    user = current_user
    today = date.today()

    # Generate QR code data for check-in
    check_in_data = url_for('scan_qr', user_id=user.id, action='checkin', date=today, _external=True)
    check_in_img = qrcode.make(check_in_data)

    # Generate QR code data for check-out
    check_out_data = url_for('scan_qr', user_id=user.id, action='checkout', date=today, _external=True)
    check_out_img = qrcode.make(check_out_data)
    
    # Save the check-in QR code image
    check_in_qr_path = f'static/qr_codes/{user.username}_checkin_{today}.png'
    os.makedirs(os.path.dirname(check_in_qr_path), exist_ok=True)
    check_in_img.save(check_in_qr_path)

    # Save the check-out QR code image
    check_out_qr_path = f'static/qr_codes/{user.username}_checkout_{today}.png'
    os.makedirs(os.path.dirname(check_out_qr_path), exist_ok=True)
    check_out_img.save(check_out_qr_path)

    return render_template('generate_qr.html', check_in_qr_path=check_in_qr_path, check_out_qr_path=check_out_qr_path)

# @app.route("/generate_qr")
# @login_required
# def generate_qr():
#     user = current_user
#     today = date.today()

#     # Generate QR code data for check-in
#     check_in_data = url_for('scan_qr', user_id=user.id, action='checkin', date=today, _external=True)
#     check_in_img = qrcode.make(check_in_data)

#     # Generate QR code data for check-out
#     check_out_data = url_for('scan_qr', user_id=user.id, action='checkout', date=today, _external=True)
#     check_out_img = qrcode.make(check_out_data)
    
#     # Save the check-in QR code image
#     check_in_qr_path = f'static/qr_codes/{user.username}_checkin_{today}.png'
#     os.makedirs(os.path.dirname(check_in_qr_path), exist_ok=True)
#     check_in_img.save(check_in_qr_path)

#     # Save the check-out QR code image
#     check_out_qr_path = f'static/qr_codes/{user.username}_checkout_{today}.png'
#     os.makedirs(os.path.dirname(check_out_qr_path), exist_ok=True)
#     check_out_img.save(check_out_qr_path)

#     return render_template('generate_qr.html', check_in_qr_path=check_in_qr_path, check_out_qr_path=check_out_qr_path)



@app.route("/qrscanner", methods=['GET'])
@login_required
def qr_scanner():
    # if not current_user.is_admin:  # Ensure only admin can access
    #     flash("You are not authorized to access this page.", "danger")
    #     return redirect(url_for('dashboard'))

    return render_template('qr_scanner.html')



@app.route("/scan/<int:user_id>/<action>/<date>", methods=['GET', 'POST'])
def scan_qr(user_id, action, date):
    staff = User.query.get(user_id)

    if not staff:
        flash("Staff member not found!", "danger")
        return redirect(url_for('dashboard'))

    # Convert date string from URL to datetime object
    try:
        scanned_date = datetime.strptime(date, '%Y-%m-%d').date()  # Convert the string to a date object
    except ValueError:
        flash("Invalid date format!", "danger")
        return redirect(url_for('dashboard'))

    today = datetime.today().date()  # Get today's date

    if scanned_date != today:
        flash("This QR code is not valid for today!", "danger")
        return redirect(url_for('dashboard'))

    if action == 'checkin':
        # Check if the staff has already checked in today
        check_in = CheckIn.query.filter_by(user_id=user_id, check_out_time=None).first()
        if check_in:
            flash(f'{staff.username} has already checked in!', 'danger')
        else:
            new_check_in = CheckIn(user_id=user_id, check_in_time=datetime.utcnow())
            db.session.add(new_check_in)
            db.session.commit()
            flash(f'{staff.username} has checked in at {new_check_in.check_in_time}', 'success')

    elif action == 'checkout':
        # Check if the staff has an active check-in to check out from
        check_in = CheckIn.query.filter_by(user_id=user_id, check_out_time=None).first()
        if check_in:
            check_in.check_out_time = datetime.utcnow()
            db.session.commit()
            flash(f'{staff.username} has checked out at {check_in.check_out_time}', 'success')
        else:
            flash(f'{staff.username} has not checked in yet!', 'danger')

    return render_template('scan.html', staff=staff)


@app.route("/checkin_history", methods=['GET', 'POST'])
@login_required
def checkin_history():
    selected_date = request.form.get('date') if request.method == 'POST' else datetime.utcnow().date()

    # Join the User model to ensure the user attribute is accessible
    checkins = CheckIn.query.join(User).filter(db.func.date(CheckIn.check_in_time) == selected_date).all()

    return render_template('checkin_history.html', checkins=checkins, selected_date=selected_date)

# Route to scan the QR code and register check-in/check-out
# @app.route("/scan/<int:user_id>", methods=['GET', 'POST'])
# def scan_qr(user_id):
#     staff = User.query.get(user_id)

#     if not staff:
#         flash("Staff member not found!", "danger")
#         return redirect(url_for('dashboard'))

#     # Check if the staff member has an active check-in
#     check_in = CheckIn.query.filter_by(user_id=user_id, check_out_time=None).first()

#     if check_in:
#         # Log the check-out time
#         check_in.check_out_time = datetime.utcnow()
#         db.session.commit()
#         flash(f'{staff.username} has checked out at {check_in.check_out_time}', 'success')
#     else:
#         # Log a new check-in time
#         new_check_in = CheckIn(user_id=user_id, check_in_time=datetime.utcnow())
#         db.session.add(new_check_in)
#         db.session.commit()
#         flash(f'{staff.username} has checked in at {new_check_in.check_in_time}', 'success')

#     return render_template('scan.html', staff=staff)

# Route to log out
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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
