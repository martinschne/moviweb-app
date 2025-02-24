from abc import ABC
from logging import Logger

from sqlalchemy.exc import SQLAlchemyError

from data_models import User, Movie
from datamanager.data_manager_interface import DataManagerInterface


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

    def get_user_movies(self, user_id: int):
        """
        Retrieves all user's movies.
        Args:
            user_id (int) search movies
        """
        movies_query = self.db.session.query(Movie).filter(Movie.user_id == user_id)
        return movies_query.filter()

    def add_user(self, user: User):
        """
        Adds a new user to the database with error handling.
        """
        self.db.session.add(user)
        self.db.session.commit()

    def add_movie(self, movie: Movie):
        """Adds a new movie to the database."""
        self.db.session.add(movie)
        self.db.session.commit()

    def update_movie(self, movie: Movie):
        """Updates an existing movie, if found."""
        try:
            existing_movie = self.db.session.query(Movie).filter(Movie.id == movie.id).first()
            if existing_movie:
                existing_movie.name = movie.name
                existing_movie.director = movie.director
                existing_movie.year = movie.year
                existing_movie.rating = movie.rating
                existing_movie.user_id = movie.user_id
                self.db.session.commit()
            else:
                Logger.error("Updated movie not found")
        except SQLAlchemyError as error:
            Logger.error(f"Error updating a movie: {error}")

    def delete_movie(self, movie_id):
        """Deletes a movie"""
        try:
            movie = self.db.session.query(Movie).filter(Movie.id == movie_id)
            if movie:
                self.db.session.delete(movie)
                self.db.session.commit()
            else:
                Logger.error("Deleted movie not found")
        except SQLAlchemyError as error:
            self.db.session.rollback()
            Logger.error(f"Error deleting a movie: {error}")
