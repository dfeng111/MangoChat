from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static') 

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/index")
def index():
    return render_template("index.html", sample_text="Yo Country")
