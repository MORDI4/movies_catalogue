from flask import Flask, render_template

import tmdb_client

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("homepage.html", movies=tmdb_client.get_movie_info())

@app.context_processor
def utility_processor():
    def tmdb_image_url(path,size):
        return tmdb_client.get_poster_url(path,size)
    return {"tmdb_image_url": tmdb_image_url}

if __name__ == '__main__':
    app.run(debug=True)
