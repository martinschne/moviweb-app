from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the database.

    The User model stores information about users, including their unique ID and name.
    It also establishes a relationship with the UserMovie model, representing the
    movies that a user has watched or interacted with.

    Attributes:
        id (int): The unique identifier for the user (Primary Key).
        name (str): The name of the user (must be unique).
        user_movies (list[UserMovie]): A list of movies associated with the user, stored in the UserMovie table.

    Methods:
        __str__(): Returns a string representation of the user, showing their name.
        __repr__(): Returns a detailed string representation of the user, including their ID and name.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_movies: Mapped[list["UserMovie"]] = relationship("UserMovie", back_populates="user",
                                                          cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"


class Movie(db.Model):
    """
    Represents a movie in the database.

    The Movie model stores information about movies, including their unique ID, name, director,
    release year, rating, and poster URL. It also establishes a relationship with the UserMovie model,
    representing the users who have watched or interacted with a particular movie.

    Attributes:
        id (int): The unique identifier for the movie (Primary Key).
        name (str): The name of the movie (must be unique).
        director (str): The director of the movie.
        year (int): The release year of the movie.
        rating (float): The rating of the movie (e.g., from IMDb).
        poster_url (str): The URL of the movie's poster.
        user_movies (list[UserMovie]): A list of users who have interacted with the movie, stored in the UserMovie table.

    Methods:
        __str__(): Returns a string representation of the movie, showing its name.
        __repr__(): Returns a detailed string representation of the movie, including its ID, name, director, year, and rating.
    """

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    director: Mapped[str] = mapped_column(nullable=True)
    year: Mapped[int] = mapped_column(nullable=True)
    rating: Mapped[float] = mapped_column(nullable=True)
    poster_url: Mapped[str] = mapped_column(nullable=True)
    user_movies: Mapped[list["UserMovie"]] = relationship("UserMovie", back_populates="movie",
                                                          cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Movie(id={self.id}, name={self.name}, director={self.director}, year={self.year}, rating={self.rating})"


class UserMovie(db.Model):
    """
    Represents the relationship between a user and a movie, including any additional data
    such as user-specific notes on the movie.

    The UserMovie model stores the connection between users and movies, along with an optional
    note that the user can add for each movie. This model establishes relationships with both
    the User and Movie models.

    Attributes:
        user_id (int): The ID of the user (Foreign Key to User).
        movie_id (int): The ID of the movie (Foreign Key to Movie).
        user_note (str): An optional note added by the user for the movie.
        user (User): The user associated with this entry.
        movie (Movie): The movie associated with this entry.

    Methods:
        __str__(): Returns a string representation of the relationship between the user and the movie.
        __repr__(): Returns a detailed string representation of the UserMovie relationship.
    """

    __tablename__ = "user_movies"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    user_note: Mapped[str] = mapped_column(String(120), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="user_movies")
    movie: Mapped["Movie"] = relationship("Movie", back_populates="user_movies")

    def __str__(self):
        return f"Movie: '{self.movie.name}' assigned to user: '{self.user.name}'"

    def __repr__(self):
        return f"UserMovie(id={self.id}, user_id={self.user_id}, movie_id={self.movie_id}, user_note={self.user_note})"
