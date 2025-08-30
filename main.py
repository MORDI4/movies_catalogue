from flask import Flask, render_template, request

import tmdb_client

app = Flask(__name__)

@app.route('/')
def homepage():
    selected_list = request.args.get('list_type', 'popular')
    if not selected_list in tmdb_client.name_list:
        selected_list = 'popular'
    movies = tmdb_client.get_movies(num=8, list_name=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list, name_list=tmdb_client.name_list)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    return render_template("movie_details.html", movie = tmdb_client.get_movie_details(movie_id))

@app.context_processor
def utility_processor():
    def tmdb_image_url(path,size):
        return tmdb_client.get_poster_url(path,size)
    return {"tmdb_image_url": tmdb_image_url}

if __name__ == '__main__':
    app.run(debug=True)
