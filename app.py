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
        name = request.form.get("name")
        username = request.form.get("username").upper()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        
        # To keep track if any error
        valid = True

        # Ensure name was submitted
        if not name:
            valid = False
            flash("Please provide name.", "danger")

        # Ensure username was submitted
        if not username:
            valid = False          
            flash("Please provide username.", "danger")

        # Check if username already exists
        elif len(list(rows)) == 1:
            valid = False
            flash("Username already exists. Please choose a new one.", "danger")

        # Ensure password was submitted
        if not password or not confirmation:
            valid = False
            flash("Please provide password.", "danger")

        # Ensure passwards are matched
        if password != confirmation:
            valid = False
            flash("Passwords do not match. Please try again", "danger")

        # Check if no error
        if valid == True:
            # Hash the password
            hash = generate_password_hash(password)
        
            # Insert the new user into database
            db.execute("INSERT INTO users (name, username, hash) VALUES (?, ?, ?)", (name, username, hash))

            # Save (commit) the changes
            db.commit()
            
            # Register user
            flash("Succesfully registered. Welcome to the addi family!", "success")
            
            # Redirect user to login page
            return redirect("/login")

        else:
            # Stay on register page
            return redirect("/register")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Configure to use SQLite database
    db = get_db()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # To keep track if any error
        valid = True
    
        # Get data from the form
        username = request.form.get("username").upper()
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
            # username = username.upper()
            rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
            rows = list(rows)
            print(rows)

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
                valid = False
                flash("Incorrect. Please try again.", "danger")

        # Check if no error
        if valid == True:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            flash("Hello!", "success")
            return redirect("/")

        else:
            return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Keep track of workout completed"""

    # Configure to use SQLite database
    db = get_db()   

    # user submited a form via POST
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol")

        symbol = symbol.upper()

        # Ensure shares was submitted
        if not shares or not shares.isnumeric():
            return apology("must provide number of shares")

        # convert to integer for calculation e.g. <=0 and * price
        shares = int(shares)

    # user reached via GET
    else:
        return render_template("add.html")

@app.route("/")
@login_required
def viewlog():
    """View workout log"""

    # Configure to use SQLite database
    db = get_db()
    users = db.execute("SELECT * FROM users;")
    for user in users:
        print(user)
    return render_template("viewlog.html")



@app.route("/motivation")
def motivation():
    return render_template("motivation/html")



