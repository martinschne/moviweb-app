from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
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
    __tablename__ = "user_movies"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    review: Mapped[str] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="user_movies")
    movie: Mapped["Movie"] = relationship("Movie", back_populates="user_movies")

    def __str__(self):
        return f"Movie: '{self.movie.name}' assigned to user: '{self.user.name}'"

    def __repr__(self):
        return f"UserMovie(id={self.id}, user_id={self.user_id}, movie_id={self.movie_id}, rating={self.rating})"
