import logging

from app import app, db
from project.data_models import User, Movie, UserMovie

logger = logging.getLogger("setup")


def populate_db():
    """ Populate database tables with mocked data from model instances. """
    # create users
    martin = User(name="Martin")
    lucy = User(name="Lucy")
    db.session.add_all([martin, lucy])

    # create movies
    schindlers_list_movie = Movie(name="Schindler's list", director="Steven Spielberg", year=1993, rating=9.0,
                                  poster_url="https://m.media-amazon.com/images/M/MV5BNjM1ZDQxYWUtMzQyZS00MTE1LWJmZGYtNGUyNTdlYjM3ZmVmXkEyXkFqcGc@._V1_SX300.jpg")

    interstellar_movie = Movie(name="Interstellar", director="Christopher Nolan", year=2014, rating=8.7,
                               poster_url="https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_SX300.jpg")

    gladiator_movie = Movie(name="Gladiator", director="Ridley Scott", year=2000, rating=8.5,
                            poster_url="https://m.media-amazon.com/images/M/MV5BYWQ4YmNjYjEtOWE1Zi00Y2U4LWI4NTAtMTU0MjkxNWQ1ZmJiXkEyXkFqcGc@._V1_SX300.jpg")

    matrix_movie = Movie(name="The Matrix", director="Lana & Lilly Wachowski", year=1999, rating=8.7,
                         poster_url="https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_SX300.jpg")

    shawshank_redemption_movie = Movie(name="The Shawshank Redemption", director="Frank Darabont", year=1994,
                                       rating=9.3,
                                       poster_url="https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_SX300.jpg")

    whiplash_movie = Movie(name="Whiplash", director="Damien Chazelle", year=2014, rating=8.5,
                           poster_url="https://m.media-amazon.com/images/M/MV5BMDFjOWFkYzktYzhhMC00NmYyLTkwY2EtYjViMDhmNzg0OGFkXkEyXkFqcGc@._V1_SX300.jpg")

    db.session.add_all(
        [schindlers_list_movie, interstellar_movie, gladiator_movie, matrix_movie, shawshank_redemption_movie,
         whiplash_movie])
    db.session.commit()

    # assign movies to the users
    db.session.add_all([UserMovie(user_id=martin.id, movie_id=schindlers_list_movie.id,
                                  user_note="Very sad movie, Worth to watch again."),
                        UserMovie(user_id=martin.id, movie_id=interstellar_movie.id,
                                  user_note="Super cool space animations!"),
                        UserMovie(user_id=martin.id, movie_id=gladiator_movie.id),
                        UserMovie(user_id=lucy.id, movie_id=matrix_movie.id, user_note="Are we living in The Matrix?"),
                        UserMovie(user_id=lucy.id, movie_id=shawshank_redemption_movie.id,
                                  user_note="Huh, Frank has made a great job on this one!"),
                        UserMovie(user_id=lucy.id, movie_id=whiplash_movie.id)])
    db.session.commit()


def create_db():
    """ Create tables in a database based on the data models. """
    db.create_all()
    logger.info("Database was created!")


if __name__ == "__main__":
    with app.app_context():
        create_db()
        populate = input("Press 'y' to populate the database with test data: ")
        if populate.lower() == "y":
            populate_db()
            logger.info("Database was populated with test data!")
