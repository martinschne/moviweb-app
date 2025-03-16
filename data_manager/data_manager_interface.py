from abc import ABC, abstractmethod
from typing import List

from project.data_models import User, Movie


class DataManagerInterface(ABC):
    """
    Abstract base class that defines the interface for managing users and movies.
    Concrete implementations must provide methods for accessing and modifying user
    and movie data in various storage formats.
    """

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """
        Retrieves all users.

        Returns:
            List[User]: A list of all user objects.
        """
        pass

    @abstractmethod
    def get_all_users_count(self) -> int:
        """
        Retrieves the total number of users.

        Returns:
            int: The count of all users.
        """
        pass

    @abstractmethod
    def get_all_movies_count(self) -> int:
        """
        Retrieves the total number of movies.

        Returns:
            int: The count of all movies.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id) -> List[Movie]:
        """
        Retrieves all movies associated with a specific user.

        Args:
            user_id (int): The ID of the user whose movies are to be retrieved.

        Returns:
            List[Movie]: A list of movies assignd to the user.
        """
        pass

    @abstractmethod
    def add_user(self, user: User):
        """
        Adds a new user to the system.

        Args:
            user (User): The user object to be added.
        """
        pass

    @abstractmethod
    def add_movie(self, movie: Movie):
        """
        Adds a new movie to the system.

        Args:
            movie (Movie): The movie object to be added.
        """
        pass

    @abstractmethod
    def add_movie_to_user(self, user_id: int, movie: Movie):
        """
        Assigns a movie to a specific user.

        Args:
            user_id (int): The ID of the user.
            movie (Movie): The movie object to be assigned to the user.
        """
        pass

    @abstractmethod
    def update_movie(self, movie: Movie):
        """
        Updates an existing movie in the system.

        Args:
            movie (Movie): The movie object with updated details.
        """

    pass

    @abstractmethod
    def delete_movie(self, movie_id: int):
        """
        Deletes a movie from the system.

        Args:
            movie_id (int): The ID of the movie to be deleted.
        """
        pass

    @abstractmethod
    def get_movie_by_title(self, title: str) -> Movie | None:
        """
        Retrieves a movie by its title.

        Args:
            title (str): The title of the movie to be retrieved.

        Returns:
            Movie | None: The movie object if found, otherwise None.
        """
        pass

    @abstractmethod
    def add_user_movie_note(self, user_id: int, movie_id: int, user_note: str):
        """
        Adds a note for a specific user and movie.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            user_note (str): The note to be added for the movie by the user.
        """
        pass
