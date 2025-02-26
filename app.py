import logging
import os

from flask import Flask, render_template, request, redirect, url_for, flash, abort

from project.data_models import db, Movie, User
from data_manager.sqlite_data_manager import SQLiteDataManager
from project.exceptions import DatabaseError, MovieNotFoundError

app = Flask(__name__)

# Set up global logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("app")

BASE_DIR = os.path.abspath(os.path.dirname("app"))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'moviweb_app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    user = User.query.get_or_404(user_id, description="User not found!")
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
            except DatabaseError as error:
                abort(500, description=str(error))

            return redirect(url_for("list_users"))

    return render_template("add_user.html")


@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id: int):
    if request.method == "POST":
        movie_name = request.form.get("name").strip()
        if not movie_name:
            flash("Movie name is required")
            return redirect(url_for("add_movie", user_id=user_id))

        movie_director = request.form.get("director").strip() or None
        year_form_value = request.form.get("year") or None
        rating_form_value = request.form.get("rating") or None

        try:
            movie_year = int(year_form_value) if year_form_value else None
        except ValueError:
            flash("Wrong year")
            return redirect(url_for("add_movie", user_id=user_id))

        try:
            movie_rating = float(rating_form_value) if rating_form_value else None
        except ValueError:
            flash("Wrong rating")
            return redirect(url_for("add_movie", user_id=user_id))

        new_movie = Movie(
            name=movie_name,
            director=movie_director,
            year=movie_year,
            rating=movie_rating,
            user_id=user_id
        )
        try:
            data_manager.add_movie(new_movie)
        except DatabaseError as error:
            abort(500, description=str(error))

        return redirect(url_for("user_movies", user_id=user_id))

    user = User.query.get_or_404(user_id, description="User not found!")
    return render_template("add_movie.html", user=user)


@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id: int, movie_id: int):
    updated_movie = Movie.query.get_or_404(movie_id, description="Movie not found, unable to update.")
    movie_user = User.query.get_or_404(user_id, description="Associated user not found, unable to update the movie.")

    if request.method == "POST":
        # save the updated movie
        new_name = request.form.get("name").strip()
        if not new_name:
            flash("Movie name is required")
            return redirect(url_for("update_movie", user_id=movie_user.id, movie_id=movie_id))

        updated_movie.name = new_name
        updated_movie.director = request.form.get("director").strip() or None

        year_form_value = request.form.get("year") or None
        rating_form_value = request.form.get("rating") or None
        user_id_form_value = request.form.get("user")

        try:
            new_year = int(year_form_value) if year_form_value else None
        except ValueError:
            flash("Wrong year")
            return redirect(url_for("update_movie", user_id=movie_user.id, movie_id=movie_id))

        try:
            new_rating = float(rating_form_value) if rating_form_value else None
        except ValueError:
            flash("Wrong rating")
            return redirect(url_for("update_movie", user_id=movie_user.id, movie_id=movie_id))

        try:
            new_user_id = int(user_id_form_value)
        except ValueError:
            flash("Wrong user")
            return redirect(url_for("update_movie", user_id=movie_user.id, movie_id=movie_id))

        updated_movie.year = new_year
        updated_movie.rating = new_rating
        updated_movie.user_id = new_user_id

        try:
            data_manager.update_movie(updated_movie)
        except DatabaseError as error:
            abort(500, description=str(error))

        return redirect(url_for("user_movies", user_id=movie_user.id))

    all_users = data_manager.get_all_users()
    return render_template("update_movie.html", movie=updated_movie, users=all_users)


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>")
def delete_movie(user_id: int, movie_id: int):
    try:
        data_manager.delete_movie(movie_id)
        user = User.query.get_or_404(user_id, description="Associated user not found, unable to delete the movie.")
    except MovieNotFoundError as error:
        abort(404, description=str(error))
    except DatabaseError as error:
        abort(500, description=str(error))

    if not user:
        return redirect(url_for("list_users"))

    return redirect(url_for("user_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        '404.html',
        message=error.description
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        '500.html',
        message=error.description
    ), 500


if __name__ == "__main__":
    app.run(debug=True)