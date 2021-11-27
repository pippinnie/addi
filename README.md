# addi
#### Video Demo:  https://youtu.be/zOwhlnBi2oY

### Description:

addi is a simple workout tracker website based on Flask that lets each member simply records workouts completed by specifying type of workout, date, time duration and optional details such as title and instructor. Members can view the added/recorded workouts in a monthly workout calendar as well as a more detailed yearly workout log which comes with a search function.

## File walk-through:

**app.py**
This is the main file that is written in Python. It has imports, main configuration and all the routes of the website that allows users to

 - register - let the user create an account to enjoy the functionalities of the website requiring min 6 characters for username and min 8 characters for password
 - sign-in - let the user who already has an account signing in
 - sign-out - after signed in, let the user choose to log out
 - add a workout - keep track of a new workout completed with required details on date, time duration in minutes and type of workout as well as optional details such as workout title and instructor
 - view a workout calendar - a monthly calendar with recorded workouts, each titling with time duration and workout title, different colors for different types of workout. Can click on each workout to see full name of workout type and instructor. Calendar header to switch to previous month or next month and come back to the current month
 - view a workout log - a detailed yearly log with all details sorting by workout date by descending order (newest to oldest). Can search with text to filter rows in the log table. Log header to switch to previous year or next year and come back to the current year
 - view and update profile - let the user change username and/or password

**helpers.py**
There is implementation of helper functions which are `apology` and `login_required`.

**db.py**
This contains configuration for connection with SQlite3 database.

**addi.db**
The main database of the website in SQlite3. It has two tables:

 - **users** - containing user ID, username and hashed password for registered users.
 - **workouts** - containing user ID, workout type, date, duration, title and instructor for recorded workouts.

**requirements.txt**
This file prescribes the packages on which this website depends.

**/templates**
In this path, there are HTML forms for the routes mainly styled with Bootstrap. addi's workout calendar were completed with much help from TUI calendar. Favicon was used to create the brand logo and Font Awesome was used for icons on the website.
Besides the main layout file, there is additional layout file `2col_layout` which is used for register and sign-in pages.

**/static**
Besides CSS, icons and images, this path contains two JavaScript files:

 - **app.js** - to get default today's date for the add workout form, search box for workout log, and other styles of the web site.
 - **calendar.js** - to display workout calendar with the recorded schedules

## Reference:
Some basic functionalities of the website started from the distribution code and my own implementation of CS50x 2021 problem set 9 Finance. Additional functionalities are referred from other resources found on the internet.