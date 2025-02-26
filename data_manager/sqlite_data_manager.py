import logging
from abc import ABC

from sqlalchemy.exc import SQLAlchemyError

from project.data_models import User, Movie
from data_manager.data_manager_interface import DataManagerInterface
from project.exceptions import MovieNotFoundError, DatabaseError

logger = logging.getLogger("sqlite_data_manager")

class SQLiteDataManager(DataManagerInterface, ABC):
    def __init__(self, db):
        """
        Initializes SQLiteDataManager with a pre-configured SQLAlchemy instance.
        Args:
            db: database instance to execute queries on
        """
        self.db = db

    def get_all_users(self):
        """
        Retrieves all users from the database.
        """
        users_query = self.db.session.query(User)
        return users_query.all()

    def get_all_users_count(self):
        """
        Retrieves the count of all users from the database.
        """
        return self.db.session.query(User).count()

    def get_all_movies_count(self):
        """
        Retrieves the count of all movies from the database.
        """
        return self.db.session.query(Movie).count()

    def get_user_movies(self, user_id: int):
        """
        Retrieves all user's movies.
        Args:
            user_id (int) search movies
        """
        movies_query = self.db.session.query(Movie).filter(Movie.user_id == user_id)
        return movies_query.all()

    def add_user(self, user: User):
        """
        Adds a new user to the database with error handling.
        """
        try:
            self.db.session.add(user)
            self.db.session.commit()
            logger.info("New user was added to the database.")
        except SQLAlchemyError as error:
            self.db.session.rollback()
            error_message = f"Database error: {str(error)}"
            logger.error(error_message)
            raise DatabaseError("Adding user failed.") from error

    def add_movie(self, movie: Movie):
        """Adds a new movie to the database."""
        try:
            self.db.session.add(movie)
            self.db.session.commit()
            logger.info("New movie was added to the database.")
        except SQLAlchemyError as error:
            self.db.session.rollback()
            error_message = f"Database error: {str(error)}"
            logger.error(error_message)
            raise DatabaseError("Adding movie failed.") from error

    def update_movie(self, movie: Movie):
        """Updates an existing movie, if found."""
        existing_movie = Movie.query.get(movie.id)
        existing_movie.name = movie.name
        existing_movie.director = movie.director
        existing_movie.year = movie.year
        existing_movie.rating = movie.rating
        existing_movie.user_id = movie.user_id
        try:
            self.db.session.commit()
            logger.info("Movie was updated.")
        except SQLAlchemyError as error:
            self.db.session.rollback()
            error_message = f"Database error: {str(error)}"
            logger.error(error_message)
            raise DatabaseError("Updating movie failed.") from error

    def delete_movie(self, movie_id: int):
        """Deletes a movie"""
        movie = Movie.query.get(movie_id)
        if movie:
            try:
                self.db.session.delete(movie)
                self.db.session.commit()
                logger.info("Movie was deleted.")
            except SQLAlchemyError as error:
                self.db.session.rollback()
                error_message = f"Database error: {str(error)}"
                logger.error(error_message)
                raise DatabaseError("Deleting movie failed.") from error

        else:
            error_message = f"Movie to delete with ID: {movie_id} not found."
            logger.error(error_message)
            raise MovieNotFoundError(error_message)
