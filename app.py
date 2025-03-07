import json
import logging
import os
from urllib.parse import urljoin, urlencode

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify

from data_manager.sqlite_data_manager import SQLiteDataManager
from project.data_models import db, Movie, User
from project.exceptions import DatabaseError, MovieNotFoundError, UserNotUniqueError
from utils.validation import get_valid_number_or_none, get_valid_url_or_none

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

# Set up global logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("app")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Root directory
DB_PATH = os.path.join(BASE_DIR, "data", "moviweb_app.db")  # Correct database location

app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

data_manager = SQLiteDataManager(db)


@app.route('/')
def home():
    users_count = data_manager.get_all_users_count()
    movies_count = data_manager.get_all_movies_count()
    return render_template("index.html", users_count=users_count, movies_count=movies_count)


@app.route("/users")
def list_users():
    users = data_manager.get_all_users()
    return render_template("users.html", users=users)


@app.route("/users/<int:user_id>")
def user_movies(user_id: int):
    movies = data_manager.get_user_movies(user_id)
    user = db.get_or_404(User, user_id, description="User not found!")
    # Note - add notes to the movies
    return render_template("movies.html", movies=movies, user=user)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        new_user_name = request.form.get("name").strip()
        if not new_user_name:
            flash("User's name cannot be empty.")
        else:
            try:
                data_manager.add_user(User(name=new_user_name))
            except UserNotUniqueError:
                flash("User already exists. Choose other name.")
                return render_template("add_user.html")
            except DatabaseError as error:
                abort(500, description=str(error))

            return redirect(url_for("list_users"))

    return render_template("add_user.html")


def _load_movie(title: str) -> Movie | None:
    new_movie = None
    base_url = "https://www.omdbapi.com/"
    params = {"apikey": API_KEY, "t": title, "type": "movie"}

    response = requests.get(url=urljoin(base_url, "?" + urlencode(params)))
    response_obj = json.loads(response.text)

    if response.status_code == 200:
        movie_was_found = eval(response_obj["Response"])

        if movie_was_found:
            new_title = response_obj["Title"]
            new_director = response_obj["Director"]
            new_year = get_valid_number_or_none(response_obj["Year"], int)
            new_rating = get_valid_number_or_none(response_obj["imdbRating"], float)
            new_poster_url = get_valid_url_or_none(response_obj["Poster"])

            new_movie = Movie(
                name=new_title,
                director=new_director,
                year=new_year,
                rating=new_rating,
                poster_url=new_poster_url
            )

        else:
            logger.warning(response_obj["Error"])
    else:
        logger.error("Error: Accessing movie data failed, please try again later.")

    return new_movie


@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id: int):
    user = User.query.get_or_404(user_id, description="User not found!")

    if request.method == "POST":
        movie_name = request.form.get("name").strip()

        if not movie_name:
            flash("Movie name is required")
            return redirect(url_for("add_movie", user=user, movie=None))

        movie_director = request.form.get("director").strip() or None
        movie_year = get_valid_number_or_none(request.form.get("year").strip(), int)
        movie_rating = get_valid_number_or_none(request.form.get("rating").strip(), float)
        movie_poster_url = get_valid_url_or_none(request.form.get("poster_url").strip())

        new_movie = Movie(
            name=movie_name,
            director=movie_director,
            year=movie_year,
            rating=movie_rating,
            poster_url=movie_poster_url
        )

        try:
            user_movie_list = data_manager.get_user_movies(user_id)
            this_user_movie = next(
                (movie for movie in user_movie_list if movie.name == movie_name),
                None
            )
            added_movie = data_manager.get_movie_by_title(movie_name)

            if not added_movie:
                data_manager.add_movie(new_movie)
            else:
                new_movie = added_movie

            if not this_user_movie:
                data_manager.add_movie_to_user(user_id, new_movie)
            else:
                flash("Movie is already in users list.")
                return redirect(url_for("add_movie", user_id=user_id, movie=None))

        except DatabaseError as error:
            abort(500, description=str(error))

        return redirect(url_for("user_movies", user_id=user_id))

    # get (movie search)
    title = request.args.get("title")

    if title:
        try:
            fetched_movie = _load_movie(title)
        except requests.exceptions.ConnectionError as error:
            logger.error(f"Connection to omdb failed: {str(error)}")
            flash("Searching online failed, please retry later.")
            return render_template("add_movie.html", user=user, movie=None)

        matching_movie = data_manager.get_movie_by_title(title) or fetched_movie
        if not matching_movie:
            flash(f"No movie found. Try a different search.")

        return render_template("add_movie.html", user=user, movie=matching_movie)

    return render_template("add_movie.html", user=user, movie=None)


@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id: int, movie_id: int):
    updated_movie = Movie.query.get_or_404(movie_id, description="Movie not found, unable to update.")
    movie_user = User.query.get_or_404(user_id, description="Associated user not found, unable to update the movie.")

    if request.method == "POST":
        # save the updated movie
        movie_name = request.form.get("name").strip()
        if not movie_name:
            flash("Movie name is required")
            return render_template("update_movie.html", user_id=user_id, movie=updated_movie)

        movie_director = request.form.get("director").strip() or None
        movie_year = get_valid_number_or_none(request.form.get("year").strip(), int)
        movie_rating = get_valid_number_or_none(request.form.get("rating").strip(), float)
        movie_poster_url = get_valid_url_or_none(request.form.get("poster_url").strip())

        updated_movie = Movie(
            id=movie_id,
            name=movie_name,
            director=movie_director,
            year=movie_year,
            rating=movie_rating,
            poster_url=movie_poster_url
        )

        try:
            data_manager.update_movie(updated_movie)
        except DatabaseError as error:
            abort(500, description=str(error))

        return redirect(url_for("user_movies", user_id=movie_user.id))

    return render_template("update_movie.html", user_id=user_id, movie=updated_movie)


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>")
def delete_movie(user_id: int, movie_id: int):
    try:
        data_manager.delete_movie(movie_id)
    except MovieNotFoundError as error:
        abort(404, description=str(error))
    except DatabaseError as error:
        abort(500, description=str(error))

    return redirect(url_for("user_movies", user_id=user_id))


@app.route("/users/<int:user_id>/add_note/<int:movie_id>", methods=["POST"])
def add_note(user_id: int, movie_id: int):
    note = request.form.get("note").strip()

    if note == "":
        return jsonify(success=False, error="Note cannot be empty"), 400

    try:
        data_manager.add_user_movie_note(user_id, movie_id, note)
    except DatabaseError as error:
        abort(500, description=str(error))

    return jsonify(success=True, note=note), 200


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        'errors/404.html',
        message=error.description
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        'errors/500.html',
        message=error.description
    ), 500


if __name__ == "__main__":
    app.run(debug=True)