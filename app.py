from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db, close_db
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Close database connection
@app.teardown_appcontext
def teardown_db(exception):
    close_db()


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Configure to use SQLite database
    db = get_db()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get data from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))

        # To keep track if any error
        valid = True

        # Ensure username was submitted
        if not username:
            valid = False
            flash("Please provide username.", "danger")

        # Ensure username length is greater than min requirement
        elif len(username) < 6:
            valid = False
            flash("Username must be at least 6 characters.", "danger")

        # Check if username already exists
        elif len(list(rows)) == 1:
            valid = False
            flash("Username already exists. Please choose a new one.", "danger")

        # Ensure password was submitted
        if not password or not confirmation:
            valid = False
            flash("Please provide password.", "danger")

        # Ensure password length is greater than min requirement
        elif len(password) < 8:
            valid = False
            flash("Password must be at least 8 characters.", "danger")

        # Ensure passwards are matched
        if password != confirmation:
            valid = False
            flash("Passwords do not match. Please try again", "danger")

        # Check if no error
        if valid == True:
            # Hash the password
            hash = generate_password_hash(password)

            # Insert the new user into database
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))

            # Save (commit) the changes
            db.commit()

            # Register user
            flash("Succesfully registered. Welcome to the addi family!", "success")

            # Redirect user to login page
            return redirect("/")

        else:
            # Stay on register page
            return redirect("/register")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
def login():
    """Sign user in"""

    # Configure to use SQLite database
    db = get_db()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # To keep track if any error
        valid = True

        # Get data from the form
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            valid = False
            flash("Please provide username.", "danger")

        # Ensure password was submitted
        if not password:
            valid = False
            flash("Please provide password.", "danger")

        # Query database for username
        else:
            rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
            rows = list(rows)

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
                valid = False
                flash("Incorrect. Please try again.", "danger")

        # Check if no error
        if valid == True:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            session["user_username"] = rows[0]['username']

            # Redirect user to workout calendar
            return redirect("/add")

        else:
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signin.html")


@app.route("/signout")
def logout():
    """Sign user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Keep track of workout completed"""

    # Configure to use SQLite database
    db = get_db()

    # user submited a form via POST
    if request.method == "POST":
        date = request.form.get("date")
        duration = request.form.get("duration")
        workout_type = request.form.get("workout_type")
        title = request.form.get("title")
        instructor = request.form.get("instructor")

        # Ensure date, duration and workout type were submitted
        if not date or not duration or not workout_type:
            flash("Please select date, workout duration and workout type.")

        else:
            # Insert the new workout into database
            db.execute("INSERT INTO workouts (user_id, date, duration, workout_type, title, instructor) VALUES (?, ?, ?, ?, ?, ?)", (session["user_id"], date, duration, workout_type, title, instructor))

            # Save (commit) the changes
            db.commit()

            # Success Message
            flash("Wonderful! Keep it rolling!", "success")

        # Redirect user to login page
        return redirect("/add")

    # user reached via GET
    else:
        # Query database for titles and instructors from workouts table with the user id
        db_titles = db.execute("SELECT title FROM workouts WHERE user_id = ? GROUP BY title ORDER BY COUNT (title) DESC", (session["user_id"],))
        db_instructors = db.execute("SELECT instructor FROM workouts WHERE user_id = ? GROUP BY instructor ORDER BY COUNT (instructor)", (session["user_id"],))

        db_titles = list(db_titles)
        db_instructors = list(db_instructors)

        titles = []
        instructors = []

        for title in db_titles:
            titles.append(title['title'])

        for instructor in db_instructors:
            instructors.append(instructor['instructor'])

        print(titles)
        print(instructors)

        return render_template("add.html", titles=titles, instructors=instructors)


@app.route("/log")
@app.route("/log/<int:year>")
@login_required
def log(year=None):
    """View workout log"""

    # Get current year
    if year is None:
        year = datetime.now().year

    print(year)
    # Configure to use SQLite database
    db = get_db()
    workouts = db.execute("SELECT * FROM workouts WHERE user_id = ? AND strftime('%Y', date) = ? ORDER BY date DESC", (session["user_id"], str(year)))
    return render_template("log.html", workouts=workouts, year=year)


@app.route("/calendar")
@login_required
def calendar():
    """View workout calendar"""

    # Configure to use SQLite database
    db = get_db()
    workouts = db.execute("SELECT * FROM workouts WHERE user_id = ? ORDER BY date DESC", (session["user_id"],))

    schedules = []

    for workout in workouts:
        date = workout['date']
        duration = str(workout['duration'])
        workoutType = workout['workout_type']
        title = workout['title']
        instructor = workout['instructor']

        # Change bgColor depending on workout type
        if workoutType == "Cardio":
            color = "#AC090A"
        elif workoutType == "Strength":
            color = "#408DCC"
        elif workoutType == "Flexibility":
            color = "#7d9999"
        else:
            color = "#04030F"

        # Add each workout into list of dictionary 'schedules'
        schedules.append({
                "title": duration + 'm ' + title,
                "body": workoutType + ' workout, ' + 'Instructor: ' + instructor,
                "category": 'allday',
                "start": date,
                "bgColor": color,
                "isReadOnly": True,
                "raw": {
                    "workoutType": workoutType
                }
            }
        )

    return render_template("calendar.html", schedules=schedules)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Update user profile"""

    # Configure to use SQLite database
    db = get_db()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get data from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not password or not confirmation:
            # Check if no change to username
            if not username or username == session['user_username']:
                flash("No update", "danger")

            else:
                # Query database for username
                rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))

                # Check if username length is greater than min requirement
                if len(username) < 6:
                    flash("Username must be at least 6 characters.", "danger")

                # Check if username already exists
                elif len(list(rows)) == 1:
                    flash("Username already exists. Please choose a new one.", "danger")

                else:
                    # Update username
                    db.execute("UPDATE users SET username = ? WHERE id = ?", (username, session["user_id"]))

                    # Save (commit) the changes
                    db.commit()

                    # Update user's name
                    flash("Username succesfully updated.", "success")

                    # Update session name
                    session['user_username'] = username

        # Update pwd
        elif not username or username == session['user_username']:

            # Ensure password length is greater than min requirement
            if len(password) < 8:
                flash("Password must be at least 8 characters.", "danger")

            # Ensure passwards are matched
            elif password != confirmation:
                flash("Passwords do not match. Please try again", "danger")

            else:
                # Hash the password
                hash = generate_password_hash(password)

                # update the user's database
                db.execute("UPDATE users SET hash = ? WHERE id = ?", (hash, session["user_id"]))

                # Save (commit) the changes
                db.commit()

                # Update user
                flash("Password succesfully updated.", "success")

        # Redirect user to profile page
        return redirect("/profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("profile.html")



