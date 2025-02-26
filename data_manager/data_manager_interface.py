from abc import ABC, abstractmethod

from project.data_models import User, Movie


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def add_movie(self, movie: Movie):
        pass

    @abstractmethod
    def update_movie(self, movie: Movie):
        pass

    @abstractmethod
    def delete_movie(self, movie_id: int):
        pass
