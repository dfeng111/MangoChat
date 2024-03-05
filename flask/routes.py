from flask import render_template
from flask import Flask

app = Flask(__name__)

# Sample data for demonstration
posts = [
    {
        'author': 'Chris',
        'title': 'Blog Post 1',
        'content': 'Coding is fun.',
        'date_posted': 'March 04, 2024'
    },
    {
        'author': 'Chris',
        'title': 'Blog Post 2',
        'content': 'Coding is not fun.',
        'date_posted': 'March 05, 2024'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)