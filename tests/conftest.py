import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from project.data_models import db, User, Movie


@pytest.fixture(scope="session")
def session():
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    db.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def test_user():
    """Creates a test user added to the test session."""
    return User(name="test_user")


@pytest.fixture
def test_movie():
    """Creates a test movie connected to test user"""
    return Movie(
        name="test_movie",
        director="test_director",
        year=1990,
        rating=9.5,
        poster_url="https://example.com"
    )
