from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static') 

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
        username = request.form["logName"]
        password = request.form["logPassword"]

        # Check if username and password are valid
        if username in users and users[username] == password:
            # Redirect to a success page
            return redirect(url_for("success", username=username))
        else:
            # Redirect back to login page with an error message
            return render_template("login.html", error="Invalid username or password")

    # For GET requests, just render the login page
    return render_template("login.html", title="Login/Register")

@app.route("/register", methods=["POST"])
def register():
    pass

@app.route("/success/<username>")
def success(username):
    return f"Welcome back, {username}!"

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
