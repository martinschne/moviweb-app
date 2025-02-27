import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from project.data_models import db, User, Movie


@pytest.fixture(scope="session")
def engine():
    """Create a new database engine for testing."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def tables(engine):
    """Create all tables before tests run and drop them after."""
    db.metadata.create_all(engine)
    yield
    db.metadata.drop_all(engine)


@pytest.fixture
def session(engine, tables):
    """Creates a new database session for each test."""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()  # Rollback changes after test
    session.close()

@pytest.fixture
def test_user(session):
    """Creates a test user added to the test session."""
    user = User(name="test_user")
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def test_movie(session, test_user):
    """Creates a test movie connected to test user"""
    movie = Movie(
        name="test_movie",
        director="test_director",
        year="1990",
        rating="9.5",
        user_id=test_user.id
    )
    session.add(movie)
    session.commit()
    return movie
