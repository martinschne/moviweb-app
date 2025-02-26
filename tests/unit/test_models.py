from project.data_models import User, Movie
from tests.conftest import session


def test_new_user(session):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the id and name attributes are defined correctly
    """
    user_name = "Test User"

    user = User(name=user_name)
    session.add(user)
    session.commit()

    # Verify user data stored in db
    db_user = session.get(User, user.id)
    assert db_user is not None
    assert db_user.name == user_name
    assert isinstance(db_user.id, int)


def test_new_movie(session):
    """
    GIVEN a Movie model
    WHEN a new Movie is created
    THEN check the movies attributes are defined correctly
    """
    name = "Test Movie"
    director = "Test Director"
    year = 1980
    rating = 10
    user_id = 1

    movie = Movie(
        name=name,
        director=director,
        year=year,
        rating=rating,
        user_id=user_id
    )
    session.add(movie)
    session.commit()

    # Verify movie data stored in db
    db_movie = session.get(Movie, movie.id)
    assert db_movie.id == 1
    assert db_movie.director == director
    assert db_movie.year == year
    assert db_movie.rating == rating
    assert isinstance(db_movie.user_id, int)
    assert isinstance(db_movie.user, User)
