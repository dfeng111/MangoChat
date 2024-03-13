from flask import Flask, render_template, request, redirect, url_for
from Database.database_setup import db, User, Channel, UserChannel, Message, Friend, Block

app = Flask(__name__, static_url_path='/static')

# Configuration for SQLAlchemy
# *****************************
# PLACEHOLDER URI
# Make sure to change in future
#
# *****************************
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mango:COSC310=mcpw@127.0.0.1/mangochat'
# app.config['MYSQL_UNIX_SOCKET'] = 'TCP'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()

# Test users
users = {
    "john": "password",
    "alice": "123456",
    "bob": "qwerty"
}

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/index")
def index():
    return render_template("index.html", sample_text="Yo Country")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if username and password are valid
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Redirect to a success page
            return redirect(url_for("success", username=username))
        else:
            # Redirect back to login page with an error message
            return render_template("login.html", error="Invalid username or password")

    # For GET requests, just render the login page
    return render_template("login.html")

@app.route("/success/<username>")
def success(username):
    return f"Welcome back, {username}!"

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
