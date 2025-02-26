# setup.py
import logging

from app import app, db
from data_models import User, Movie

logger = logging.getLogger("setup")


# populate table with fake data
def populate_db():
    # create users
    martin = User(name="Martin")
    lucy = User(name="Lucy")
    db.session.add_all([martin, lucy])
    db.session.commit()  # commit users to get their ids

    # create movies
    db.session.add_all([
        Movie(name="Schindler's list", director="Steven Spielberg", year=1993, rating=9.0, user_id=martin.id),
        Movie(name="Interstellar", director="Christopher Nolan", year=2014, rating=8.7, user_id=martin.id),
        Movie(name="Gladiator", director="Ridley Scott", year=2000, rating=8.5, user_id=martin.id),

        Movie(name="The Matrix", director="Lana & Lilly Wachowski", year=1999, rating=8.7, user_id=lucy.id),
        Movie(name="The Shawshank Redemption", director="Frank Darabont", year=1994, rating=9.3, user_id=lucy.id),
        Movie(name="Whiplash", director="Damien Chazelle", year=2014, rating=8.5, user_id=lucy.id)
    ])

    db.session.commit()


def create_db():
    db.create_all()
    logger.info("Database created!")


if __name__ == "__main__":
    with app.app_context():
        create_db()
        populate_db()
