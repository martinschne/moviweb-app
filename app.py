import json
import logging
import os
from urllib.parse import urljoin, urlencode

import requests
from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_assets import Environment, Bundle

from config import Config
from data_manager.sqlite_data_manager import SQLiteDataManager
from project.data_models import db, Movie, User
from project.exceptions import DatabaseError, MovieNotFoundError, UserNotUniqueError
from utils.validation import get_valid_number_or_none, get_valid_url_or_none

app = Flask(__name__)
app.config.from_object(Config)

# Ensure the instance directory exists
if not os.path.exists('instance'):
    os.makedirs('instance')

assets = Environment(app)

css = Bundle("css/style.css", filters="rcssmin", output="dist/css/style.min.css")
js = Bundle("js/script.js", filters="rjsmin", output="dist/js/script.min.js")

assets.register("css_all", css)
assets.register("js_all", js)

db.init_app(app)
data_manager = SQLiteDataManager(db)

# Set up global logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("app")


@app.template_filter("pluralize")
def pluralize(count, word):
    """
    Pluralizes a given word based on the count.

    Args:
        count (int): The number of items.
        word (str): The singular form of the word to pluralize.

    Returns:
        str: The pluralized word if count is not 1, otherwise the singular word.
    """
    return word if count == 1 else word + 's'


@app.route('/')
def home():
    """
    Displays the homepage with the count of users and movies.

    Retrieves the total number of users and movies from the data manager and renders the home page.

    Returns:
        Response: The rendered HTML template for the homepage with users and movie counts.
    """
    users_count = data_manager.get_all_users_count()
    movies_count = data_manager.get_all_movies_count()
    return render_template("index.html", users_count=users_count, movies_count=movies_count)


@app.route("/users")
def list_users():
    """
    Lists all users in the database.

    Retrieves all users and renders the users list page.

    Returns:
        Response: The rendered HTML template showing the list of users.
    """
    users = data_manager.get_all_users()
    return render_template("content/users.html", users=users)


@app.route("/users/<int:user_id>")
def user_movies(user_id: int):
    """
    Displays a user's movie list.

    Args:
        user_id (int): The ID of the user whose movies are to be displayed.

    Returns:
        Response: The rendered HTML template showing the list of movies for the specified user.
    """
    movies = data_manager.get_user_movies(user_id)
    user = db.get_or_404(User, user_id, description="User not found!")
    # Note - add notes to the movies
    return render_template("content/movies.html", movies=movies, user=user)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    """
    Allows the creation of a new user.

    Handles both GET and POST requests. For GET, renders the user creation form. For POST, attempts to add a new user to the database.

    Returns:
        Response: The rendered HTML template for the user creation form, or redirects to the users list page on success.
    """
    if request.method == "POST":
        new_user_name = request.form.get("name").strip()
        if not new_user_name:
            flash("User's name cannot be empty.")
        else:
            try:
                data_manager.add_user(User(name=new_user_name))
            except UserNotUniqueError:
                flash("User already exists. Choose other name.")
                return render_template("forms/add_user.html")
            except DatabaseError as error:
                abort(500, description=str(error))

            return redirect(url_for("list_users"))

    return render_template("forms/add_user.html")


def _load_movie(title: str) -> Movie | None:
    """
    Loads movie information from the OMDB API.

    Args:
        title (str): The title of the movie to search for.

    Returns:
        Movie | None: A Movie object if found, otherwise None.
    """
    new_movie = None
    base_url = "https://www.omdbapi.com/"
    params = {"apikey": app.config["API_KEY"], "t": title, "type": "movie"}

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

            new_movie = Movie(name=new_title, director=new_director, year=new_year, rating=new_rating,
                              poster_url=new_poster_url)

        else:
            logger.warning(response_obj["Error"])
    else:
        logger.error("Error: Accessing movie data failed, please try again later.")

    return new_movie


@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id: int):
    """
    Allows a user to add a movie to their movie list.

    Handles both GET and POST requests. For GET, renders the movie search form. For POST, attempts to add a new movie to the user's list.

    Args:
        user_id (int): The ID of the user adding the movie.

    Returns:
        Response: The rendered HTML template for the movie addition form, or redirects to the user's movie list on success.
    """
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

        new_movie = Movie(name=movie_name, director=movie_director, year=movie_year, rating=movie_rating,
                          poster_url=movie_poster_url)

        try:
            user_movie_list = data_manager.get_user_movies(user_id)
            this_user_movie = next((movie for movie in user_movie_list if movie.name == movie_name), None)
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

    title = request.args.get("title")

    if title:
        try:
            fetched_movie = _load_movie(title)
        except requests.exceptions.ConnectionError as error:
            logger.error(f"Connection to omdb failed: {str(error)}")
            flash("Searching online failed, please retry later.")
            return render_template("forms/add_movie.html", user=user, movie=None)

        matching_movie = data_manager.get_movie_by_title(title) or fetched_movie
        if not matching_movie:
            flash(f"No movie found. Try a different search.")

        return render_template("forms/add_movie.html", user=user, movie=matching_movie)

    return render_template("forms/add_movie.html", user=user, movie=None)


@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id: int, movie_id: int):
    """
    Allows a user to update the details of a movie in their movie list.

    Args:
        user_id (int): The ID of the user updating the movie.
        movie_id (int): The ID of the movie being updated.

    Returns:
        Response: The rendered HTML template for updating the movie, or redirects to the user's movie list on success.
    """
    updated_movie = Movie.query.get_or_404(movie_id, description="Movie not found, unable to update.")
    movie_user = User.query.get_or_404(user_id, description="Associated user not found, unable to update the movie.")

    if request.method == "POST":
        # save the updated movie
        movie_name = request.form.get("name").strip()
        if not movie_name:
            flash("Movie name is required")
            return render_template("forms/update_movie.html", user_id=user_id, movie=updated_movie)

        movie_director = request.form.get("director").strip() or None
        movie_year = get_valid_number_or_none(request.form.get("year").strip(), int)
        movie_rating = get_valid_number_or_none(request.form.get("rating").strip(), float)
        movie_poster_url = get_valid_url_or_none(request.form.get("poster_url").strip())

        updated_movie = Movie(id=movie_id, name=movie_name, director=movie_director, year=movie_year,
                              rating=movie_rating, poster_url=movie_poster_url)

        try:
            data_manager.update_movie(updated_movie)
        except DatabaseError as error:
            abort(500, description=str(error))

        return redirect(url_for("user_movies", user_id=movie_user.id))

    return render_template("forms/update_movie.html", user_id=user_id, movie=updated_movie)


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>")
def delete_movie(user_id: int, movie_id: int):
    """
    Deletes a movie from the user's movie list.

    Args:
        user_id (int): The ID of the user whose movie list the movie is being removed from.
        movie_id (int): The ID of the movie to be deleted.

    Returns:
        Response: Redirects to the user's movie list after deletion.
    """
    try:
        data_manager.delete_movie(movie_id)
    except MovieNotFoundError as error:
        abort(404, description=str(error))
    except DatabaseError as error:
        abort(500, description=str(error))

    return redirect(url_for("user_movies", user_id=user_id))


@app.route("/users/<int:user_id>/add_note/<int:movie_id>", methods=["POST"])
def add_note(user_id: int, movie_id: int):
    """
    Adds a note to a specific movie in the user's movie list.

    Args:
        user_id (int): The ID of the user who owns the movie list.
        movie_id (int): The ID of the movie to which the note will be added.

    Returns:
        Response: JSON response indicating success or failure.
    """
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
    """
    Handles 404 errors (page not found).

    Args:
        error (Error): The error object containing the description of the error.

    Returns:
        Response: The rendered 404 error page.
    """
    error_title = "404 Page Not Found"
    return render_template('error.html', title=error_title, message=error.description), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Handles 500 errors (internal server error).

    Args:
        error (Error): The error object containing the description of the error.

    Returns:
        Response: The rendered 500 error page.
    """
    error_title = "500 Internal Server Error"
    return render_template('error.html', title=error_title, message=error.description), 500


if __name__ == "__main__":
    app.run()
