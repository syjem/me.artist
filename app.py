import re

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, request, session, url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# from models import db, Users

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

# Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}, Email: {self.email}>'

with app.app_context():
    # Call create_all to create the tables
    db.create_all()

# Set Flask app environment to development
app.debug = 'development'

# Enable debug mode
app.debug = True

current_date = datetime.now().date()

@app.context_processor
def inject_current_year():
    current_year = datetime.now().year
    return dict(current_year=current_year)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Initialize an empty list to store validation errors
        errors = []

        if not first_name:
            errors.append("Please enter your first name!")
        if len(first_name) < 2:
            errors.append("First name is too short!")
        if not last_name:
            errors.append("Please enter your last name!")
        if len(last_name) < 2:
            errors.append("Last name is too short!")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Please enter a valid email!")

        # Query the database to check if the email already exists
        user = Users.query.filter_by(email=email).first()
        if user:
            errors.append("You're using a registered email.")

        # Password validation regex pattern
        password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&_.,<>]{6,}$"
        if not password or not re.match(password_pattern, password):
            errors.append("Password need to be at least 6 characters, with a number and a special character.")
        
        if errors:
            # If there are any errors, flash them all at once as error messages
            for error in errors:
                flash(error, category='error')

            # Render the form template with error messages and retained form data
            return render_template("signup.html", first_name=first_name, 
                                    last_name=last_name, email=email
                                )
        else:
            # encrypt password
            hashed_password = generate_password_hash(password)

             # Create a new Users object and set its attributes
            new_user = Users(first_name=first_name, last_name=last_name, email=email, password=hashed_password)

            # Add the object to the session
            db.session.add(new_user)

            # Commit the session to persist the changes to the database
            db.session.commit()

            return redirect("/")


    return render_template("signup.html")

SERVICES = [
    "Weddings",
    "Portraits",
    "Families",
    "Graduations",
    "Birthdays",
    "Other Occasions"
]

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        date = request.form.get("date")
        service = request.form.get("select_services")

        # Initialize an empty list to store validation errors
        errors = []

        # form validation
        if not name:
             errors.append("Please enter a valid name!")
        elif len(name) < 3:
            errors.append("Name is too short!")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Please enter a valid email!")
        if not date:
           errors.append("Please select a valid date!")
        elif datetime.strptime(date, '%Y-%m-%d').date() < current_date:
            errors.append("Please select dates that are not prior to the current date.")
        if service not in SERVICES:
            errors.append("Please select a valid service!")

        if errors:
            # If there are any errors, flash them all at once as error messages
            for error in errors:
                flash(error, category='error')

            # Render the form template with error messages and retained form data
            return render_template("contact.html", services=SERVICES, 
                                    name=name, email=email, date=date,
                                    selected_service=service
                                )

        else:
            flash("You have booked successfully!", category='success')
    
    return render_template("contact.html", services=SERVICES)





if __name__ == '__main__':
    app.run()