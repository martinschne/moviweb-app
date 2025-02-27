import logging

from app import app, db
from project.data_models import User, Movie, UserMovie

logger = logging.getLogger("setup")


# populate table with fake data
def populate_db():
    # create users
    martin = User(name="Martin")
    lucy = User(name="Lucy")
    db.session.add_all([martin, lucy])

    # create movies
    schindlers_list_movie = Movie(name="Schindler's list", director="Steven Spielberg", year=1993, rating=9.0)
    interstellar_movie = Movie(name="Interstellar", director="Christopher Nolan", year=2014, rating=8.7)
    gladiator_movie = Movie(name="Gladiator", director="Ridley Scott", year=2000, rating=8.5)
    matrix_movie = Movie(name="The Matrix", director="Lana & Lilly Wachowski", year=1999, rating=8.7)
    shawshank_redemption_movie = Movie(name="The Shawshank Redemption", director="Frank Darabont", year=1994, rating=9.3)
    whiplash_movie = Movie(name="Whiplash", director="Damien Chazelle", year=2014, rating=8.5)

    db.session.add_all([
        schindlers_list_movie,
        interstellar_movie,
        gladiator_movie,
        matrix_movie,
        shawshank_redemption_movie,
        whiplash_movie
    ])
    db.session.commit()

    # assign movies to the users
    db.session.add_all([
        UserMovie(user_id=martin.id, movie_id=schindlers_list_movie.id),
        UserMovie(user_id=martin.id, movie_id=interstellar_movie.id),
        UserMovie(user_id=martin.id, movie_id=gladiator_movie.id),
        UserMovie(user_id=lucy.id, movie_id=matrix_movie.id),
        UserMovie(user_id=lucy.id, movie_id=shawshank_redemption_movie.id),
        UserMovie(user_id=lucy.id, movie_id=whiplash_movie.id)
    ])
    db.session.commit()


def create_db():
    db.create_all()
    logger.info("Database created!")


if __name__ == "__main__":
    with app.app_context():
        create_db()
        populate_db()
