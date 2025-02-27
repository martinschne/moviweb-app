from project.data_models import User, Movie
from tests.conftest import session

# TODO: extract the test user to a fixture
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

# TODO: extract the test movie to a fixture
def test_new_movie(session, test_movie):
    """
    GIVEN a Movie model
    WHEN a new Movie is created
    THEN check the movies attributes are defined correctly
    """
    # Verify movie data stored in db
    db_movie = session.get(Movie, test_movie.id)
    assert db_movie.director == test_movie.director
    assert db_movie.year == test_movie.year
    assert db_movie.rating == test_movie.rating
    assert isinstance(db_movie.user_id, int)
    assert isinstance(db_movie.user, User)
    assert db_movie.user.id == test_movie.user_id
    assert db_movie.user.name == test_movie.user.name

# TODO: add more tests
#  (column constraints, model relationships, user deletion deletes his movies...)