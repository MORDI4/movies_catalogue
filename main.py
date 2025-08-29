from flask import Flask, render_template
from faker import Faker

f = Faker('pl_PL')

app = Flask(__name__)

@app.route('/')
def homepage():
    movies = []
    for i in range(8):
        movies.append(f.text(max_nb_chars=20).strip('.'))
    return render_template("homepage.html", movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
