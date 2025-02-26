import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from project.data_models import db


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
