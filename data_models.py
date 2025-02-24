from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    movies: Mapped[list["Movie"]] = relationship(back_populates="users")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}"


class Movie:
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    director: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    rating: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="movies")


    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Movie(id={self.id}, name={self.name}, director={self.director}, year={self.year}, rating={self.rating}"
