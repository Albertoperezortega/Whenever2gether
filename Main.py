from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, EventForm
from datetime import datetime
from flask_login import LoginManager, login_user, UserMixin, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

# Create a Flask application
app = Flask(__name__)

# Set the secret key for the application
SECRET_KEY = "sdasd213"
app.config['SECRET_KEY'] = SECRET_KEY

# Configure the database for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'

# Initialize SQLAlchemy Bcrypt (for encryption) and Login manager
db = SQLAlchemy(app)
encrypt = Bcrypt(app)
login_m = LoginManager(app)
login_m.login_view = 'login'

migrate = Migrate(app, db)

# Define the Person class for the database 
class Person(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    activities = db.relationship('Event', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', {self.email}', {self.profile_picture}')"

# Define the Event class for the database 
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_event = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

    def __repr__(self):
        return f"Events('{self.title}', {self.date_created}', {self.description}')"

# User loader function to allow log-in
@login_m.user_loader
def load_user(user_id):
    return Person.query.get(int(user_id))

# Home route
@app.route("/")
@app.route("/home")
def home():
    events = Event.query.all()
    return render_template("home.html", events=events, count=0)

# Profile route
@app.route("/profile")
@login_required
def profile():
    events = Event.query.filter_by(person_id=current_user.id).all()
    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_picture)
    return render_template("profile.html", title='Profile', profile_image=profile_image, events=events)

# Registration route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = encrypt.generate_password_hash(form.password.data).decode('utf-8')
        person = Person(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(person)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', reg_form=form)

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        user = Person.query.filter_by(email=log_form.email.data).first()
        if user and encrypt.check_password_hash(user.password, log_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Incorrect username/password', 'danger')
    return render_template("login.html", title='Login', log_form=log_form)

# Logout route
@app.route("/logout")
def logout():
    logout_user()
    return render_template("home.html", title='Home')

# New Event route
@app.route("/events/new", methods=['GET', 'POST'])
@login_required
def create_post():
    #creates
    new_post = EventForm()
    if new_post.validate_on_submit():
        event_created = Event(title=new_post.title.data, description=new_post.description.data,
                              event_image=new_post.photo.data, author=current_user, date_event=new_post.time.data)
        db.session.add(event_created)
        db.session.commit()
        flash(f'Event created successfully', 'success')
        return redirect(url_for('home'))
    return render_template('generate_event.html', title='New Event', event_form=new_post)

# Run the application if the script is executed directly
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
