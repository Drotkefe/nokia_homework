import json
from datetime import datetime


class Actor:
    def __init__(self, name: str, birth_year: int):
        self.name = name
        self.birth_year = birth_year

    @staticmethod
    def calculate_age(movie_year: int, birth_year: int):
        return movie_year - birth_year

    def __str__(self):
        return f"{self.name} at age {self.birth_year}"

    def __eq__(self, other):
        return (
            isinstance(other, Actor)
            and other.name == self.name
            and other.birth_year == self.birth_year
        )

    def __hash__(self):
        return hash((self.name, self.birth_year))


class Movie:
    def __init__(
        self,
        title: str,
        director: Actor,
        release_year: int,
        length: str,
        actors: list[Actor],
    ):
        self.title = title
        self.director = director
        self.release_year = release_year
        self.length = length
        self.actors = actors

    def __str__(self):
        return f"{self.title} by {self.director} in {self.year}, {self.length}"

    def __eq__(self, other):
        return (
            isinstance(other, Movie)
            and other.title == self.title
            and other.director == self.director
        )

    def __hash__(self):
        return hash((self.title, self.director))


class Database_Handler:
    actors = set()
    movies = set()

    def __decoder(self, data):
        for movie in data:
            starring = []
            for actor in movie["actors"]:
                starring.append(
                    Actor(
                        actor["name"],
                        Actor.calculate_age(movie["release_year"], actor["birth_year"]),
                    )
                )
                self.actors.add(Actor(actor["name"], actor["birth_year"]))
            self.movies.add(
                Movie(
                    movie["title"],
                    Actor(movie["director"]["name"], movie["director"]["birth_year"]),
                    movie["release_year"],
                    movie["length"],
                    starring,
                )
            )

    def load_database(file_path: str):
        try:
            with open(file_path, "r") as file:
                data = json.load(file, parse_int=int)
        except:
            print("Failed to load the database")
            exit()
        return data

    def add_movie(self, movie: Movie):
        self.movies.add(movie)

    def add_actor(self, actor: Actor):
        pass


if __name__ == "__main__":
    now = datetime.now()
    formatted_time = now.strftime("%H.%M")
    Database_Handler.load_database("movies.json")
