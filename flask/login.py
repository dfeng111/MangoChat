from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Test users (PLACEHOLDER. Replace with SQL queries)
users = {
    "chris": "password",
    "hill": "123456"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        return f"Welcome back, {username}!"
    else:
        return "Invalid username or password. Please try again."

if __name__ == '__main__':
    app.run(debug=True)