import pytest
from sqlalchemy.exc import IntegrityError

from project.data_models import User, Movie, UserMovie
from tests.conftest import session


def test_saving_new_valid_user(session, test_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the id and name attributes are defined correctly
    """
    session.add(test_user)
    session.commit()

    # Verify user data stored in db
    db_user = session.get(User, test_user.id)
    assert db_user is not None
    assert db_user.name == "test_user"
    assert isinstance(db_user.id, int)


def test_saving_new_valid_movie(session, test_movie):
    """
    GIVEN a Movie model
    WHEN a new Movie is created
    THEN check the movies attributes are defined correctly
    """
    session.add(test_movie)
    session.commit()
    # Verify movie data stored in db
    saved_movie = session.get(Movie, test_movie.id)
    assert saved_movie.director == test_movie.director
    assert saved_movie.year == test_movie.year
    assert saved_movie.rating == test_movie.rating
    assert saved_movie.poster_url == test_movie.poster_url
    assert saved_movie.user_movies == []
    assert isinstance(saved_movie.id, int)


def test_saving_user_without_name(session, test_user):
    """
    GIVEN a User model with non-nullable 'name' attribute
    WHEN a new User is created without 'name' attribute provided
    THEN IntegrityError is raised
    """
    nameless_user = test_user
    del nameless_user.name

    session.add(nameless_user)

    with pytest.raises(IntegrityError):
        session.commit()


def test_saving_movie_without_name(session, test_movie):
    """
    GIVEN a Movie model with non-nullable 'name' attribute
    WHEN a new Movie is created without 'name' attribute provided
    THEN IntegrityError is raised
    """
    nameless_movie = test_movie
    del nameless_movie.name

    with pytest.raises(IntegrityError):
        session.add(nameless_movie)
        session.commit()


def test_saving_movie_only_with_name(session, test_movie):
    named_movie_without_details = Movie(name=test_movie.name)

    session.add(named_movie_without_details)
    session.commit()

    # Verify movie data stored in db
    saved_movie = session.get(Movie, named_movie_without_details.id)
    assert saved_movie.name == test_movie.name
    assert saved_movie.director is None
    assert saved_movie.year is None
    assert saved_movie.rating is None
    assert saved_movie.poster_url is None
    assert saved_movie.user_movies == []


def test_saving_users_with_same_name(session):
    user1 = User(name="test_user")
    user2 = User(name="test_user")

    session.add(user1)
    session.commit()

    session.add(user2)
    with pytest.raises(IntegrityError):
        session.commit()


def test_saving_user_with_distinct_names(session):
    user1_name = "first_test_user"
    user2_name = "second_test_user"

    user1 = User(name=user1_name)
    user2 = User(name=user2_name)

    session.add(user1)
    session.commit()

    session.add(user2)
    session.commit()

    first_saved_user = session.get(User, user1.id)
    second_saved_user = session.get(User, user2.id)

    assert first_saved_user is not None
    assert second_saved_user is not None
    assert first_saved_user.name == user1_name
    assert second_saved_user.name == user2.name


def test_deleting_movie(session, test_user, test_movie):
    user1 = test_user
    user2 = User(name="test_user2")
    movie = test_movie
    # prepare the db
    session.add(user1)
    session.add(user2)
    session.add(movie)
    session.commit()

    # assign movie to both users
    user_movie1 = UserMovie(user_id=user1.id, movie_id=movie.id)
    user_movie2 = UserMovie(user_id=user2.id, movie_id=movie.id)
    session.add_all([user_movie1, user_movie2])
    session.commit()

    user_movie_assignments_count = session.query(UserMovie).count()

    assert user_movie_assignments_count == 2

    # delete saved movie
    session.delete(movie)
    session.commit()

    saved_movie = session.get(Movie, movie.id)
    user_movie_assignments_count = session.query(UserMovie).count()

    assert saved_movie is None
    assert user_movie_assignments_count == 0
