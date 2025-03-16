import logging
from abc import ABC
from typing import List

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from data_manager.data_manager_interface import DataManagerInterface
from project.data_models import User, Movie, UserMovie
from project.exceptions import MovieNotFoundError, DatabaseError, UserNotUniqueError

logger = logging.getLogger("sqlite_data_manager")

class SQLiteDataManager(DataManagerInterface, ABC):
    def __init__(self, db):
        """
        Initializes SQLiteDataManager with a pre-configured SQLAlchemy instance.

        Args:
            db: SQLAlchemy database instance used to execute queries.
        """
        self.db = db

    def get_all_users(self) -> List[User]:
        """
        Retrieves all users from the database.

        Returns:
            List[User]: A list of all user objects retrieved from the database.
        """
        users_query = self.db.session.query(User)
        return users_query.all()

    def get_all_users_count(self) -> int:
        """
        Retrieves the count of all users from the database.

        Returns:
            int: The total number of users in the database.
        """
        return self.db.session.query(User).count()

    def get_all_movies_count(self) -> int:
        """
        Retrieves the count of all movies from the database.

        Returns:
            int: The total number of movies in the database.
        """
        return self.db.session.query(Movie).count()

    def get_user_movies(self, user_id: int) -> List[Movie]:
        """
        Retrieves all movies associated with a specific user.

        Args:
            user_id (int): The ID of the user whose movies are to be retrieved.

        Returns:
            List[Movie]: A list of movies associated with the user, with dynamically
                          attached user notes for each movie.
        """
        movies = self.db.session.execute(
            self.db.select(Movie).add_columns(UserMovie.user_note)
            .join(UserMovie)
            .filter(UserMovie.user_id == user_id)
        ).all()

        # Attach user_note dynamically
        for movie, user_note in movies:
            movie.user_note = user_note  # Add user_note to each Movie object

        # Extract only Movie objects (now modified with user_note)
        movies = [movie for movie, _ in movies]

        return movies

    def add_user(self, user: User):
        """
        Adds a new user to the database with error handling.

        Args:
            user (User): The user object to be added to the database.

        Raises:
            UserNotUniqueError: If the user already exists in the database.
            DatabaseError: If an error occurs while adding the user to the database.
        """
        try:
            self.db.session.add(user)
            self.db.session.commit()
            logger.info("New user was added to the database.")
        except IntegrityError as error:
            self.db.session.rollback()
            error_message = f"Integrity error: {str(error)}"
            logger.error(error_message)
            raise UserNotUniqueError("User already exists.") from error
        except SQLAlchemyError as error:
            self.db.session.rollback()
            error_message = f"Database error: {str(error)}"
            logger.error(error_message)
            raise DatabaseError("Adding user failed.") from error

    def add_movie(self, movie: Movie):
        """
        Adds a new movie to the database.

        Args:
            movie (Movie): The movie object to be added to the database.

        Raises:
            DatabaseError: If an error occurs while adding the movie to the database.
        """
        try:
            self.db.session.add(movie)
            self.db.session.commit()
            logger.info("New movie was added to the database.")
        except SQLAlchemyError as error:
            self.db.session.rollback()
            error_message = f"Database error: {str(error)}"
            logger.error(error_message)
            raise DatabaseError("Adding movie failed.") from error

    def add_movie_to_user(self, user_id: int, movie: Movie):
        """
        Assigns a movie to an existing user.

        Args:
            user_id (int): The ID of the user to assign the movie to.
            movie (Movie): The movie object to be assigned to the user.

        Raises:
            DatabaseError: If an error occurs while assigning the movie to the user.
        """
        try:
            new_user_movie = UserMovie(
                user_id=user_id,
                movie_id=movie.id
            )
            self.db.session.add(new_user_movie)
            self.db.session.commit()
            logger.info(f"Movie with ID: {movie.id} was assigned to user with ID: {user_id}.")
        except SQLAlchemyError as error:
            self.db.session.rollback()
            error_message = f"Database error: {str(error)}"
            logger.error(error_message)
            raise DatabaseError("Assigning movie to a user failed.") from error

    def update_movie(self, movie: Movie):
        """
        Updates an existing movie in the database.

        Args:
            movie (Movie): The movie object with updated details.

        Raises:
            DatabaseError: If an error occurs while updating the movie in the database.
        """
        try:
            stmt = update(Movie).where(Movie.id == movie.id).values(
                name=movie.name,
                director=movie.director,
                year=movie.year,
                rating=movie.rating,
                poster_url=movie.poster_url
            )
            self.db.session.execute(stmt)
            self.db.session.commit()
            logger.info("Movie was updated.")
        except SQLAlchemyError as error:
            self.db.session.rollback()
            error_message = f"Database error: {str(error)}"
            logger.error(error_message)
            raise DatabaseError("Updating movie failed.") from error

    def delete_movie(self, movie_id: int):
        """
        Deletes a movie from the database.

        Args:
            movie_id (int): The ID of the movie to be deleted.

        Raises:
            MovieNotFoundError: If the movie to delete is not found.
            DatabaseError: If an error occurs while deleting the movie from the database.
        """
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

    def get_movie_by_title(self, title: str) -> Movie | None:
        """
        Retrieves a movie by its title from the database.

        Args:
            title (str): The title of the movie to retrieve.

        Returns:
            Movie | None: The movie object if found, otherwise None.
        """
        movie = self.db.session.execute(
            self.db.select(Movie).filter(Movie.name.ilike(f"%{title}%"))
        ).scalars().first()

        return movie

    def add_user_movie_note(self, user_id: int, movie_id: int, user_note: str):
        """
        Adds a note for a specific user and movie in the database.

        Args:
            user_id (int): The ID of the user adding the note.
            movie_id (int): The ID of the movie for which the note is being added.
            user_note (str): The note to be added for the movie by the user.

        Raises:
            DatabaseError: If an error occurs while saving the note to the database.
        """
        try:
            user_movie = self.db.session.execute(
                self.db.select(UserMovie).filter(UserMovie.user_id == user_id, UserMovie.movie_id == movie_id)
            ).scalars().first()
            user_movie.user_note = user_note

            self.db.session.commit()
            logger.info(f"Note was saved for movie with ID: {movie_id} by user with ID: {user_id}.")
        except SQLAlchemyError as error:
            self.db.session.rollback()
            error_message = f"Database error: {str(error)}"
            logger.error(error_message)
            raise DatabaseError("Saving note failed.") from error
