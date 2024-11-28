import json
from datetime import datetime
import argparse
import re


class Actor:
    def __init__(self, name: str, birth_year: int):
        self.name = name
        self.birth_year = birth_year
        self.age = None

    def set_age(self, movie_year: int):
        self.age = movie_year - self.birth_year

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def print_actor_list(actor_list: list):
        for actor in actor_list:
            print(repr(actor))

    def __repr__(self):
        return f"\t\t - {self.name} at age {self.age}"

    def __eq__(self, other):
        return isinstance(other, Actor) and other.name == self.name

    def __hash__(self):
        return hash((self.name, self.birth_year))


class Movie:
    def __init__(
        self,
        title: str,
        director: Actor,
        release_year: int,
        length: int,
        actors: list[Actor],
    ):
        self.title = title
        self.director = director
        self.release_year = release_year
        self.length = length
        self.actors = actors

    def __convert_minutes_to_hhmm(self):
        hours = self.length // 60
        mins = self.length % 60
        return f"{hours:02}:{mins:02}"

    def __str__(self):
        return f"{self.title} by {str(self.director)} in {self.release_year}, {self.__convert_minutes_to_hhmm()}"

    def __repr__(self):
        return f"{self.title} by {str(self.director)} in {self.release_year}, {self.__convert_minutes_to_hhmm()}"

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
    filtered_movies = []

    def __init__(self, file_path):
        self.db_path = file_path

    def __decoder(self, data):
        for movie in data:
            starring = []
            for actor in movie["actors"]:
                new_actor = Actor(actor["name"], actor["birth_year"])
                new_actor.set_age(movie["release_year"])
                starring.append(new_actor)
                self.actors.add(new_actor)
            self.movies.add(
                Movie(
                    movie["title"],
                    Actor(movie["director"]["name"], movie["director"]["birth_year"]),
                    movie["release_year"],
                    movie["length"],
                    starring,
                )
            )

    def load_database(self):
        try:
            with open(self.db_path, "r") as file:
                data = json.load(file, parse_int=int)
        except:
            print("Failed to load the database")
            exit()
        self.__decoder(data)

    def __search_actor(self, name: str) -> Actor:
        for a in self.actors:
            if a.name == name:
                return a
        return None

    def __check_time_format(self, time: str):
        try:
            datetime.strptime(time, "%H:%M")
            return True
        except:
            return False

    def __save_to_database(self, new_movie):
        with open(self.db_path, "r+") as file:
            data = json.load(file)
            data.append(new_movie)
            file.seek(0)
            json.dump(data, file, indent=4)
            print("Failed to load the database")

    def add_movie(self):
        title = input("Title: ")
        director_input = input("Director: ")
        director = self.__search_actor(director_input)
        while director == None:
            print(f"We could not find '{director_input}', try again!")
            director_input = input("")
            director = self.__search_actor(director_input)
        release_year = input("Released in: ")
        while not release_year.isdigit():
            print("Bad input format (only numbers), try again!")
            release_year = input("Released in: ")
        length = input("Length: ")
        while not self.__check_time_format(length):
            print("Bad input format (hh:mm), try again!")
            length = input("Length: ")
        starring_list = []
        starring = input("Starring: ")
        while starring != "exit":
            result = self.__search_actor(starring)
            if result != None:
                starring_list.append(result)
            else:
                print("This actor is not in the database, try again!")
            starring = input("")
        new_movie = Movie(title, director, release_year, length, starring_list)
        self.movies.add(new_movie)
        self.__save_to_database(new_movie)

    def add_actor(self):
        name = input("Name: ")
        birth_year = input("Birth year: ")
        while not birth_year.isdigit():
            print("Bad input format (only numbers), try again!")
            birth_year = input("Birth year: ")
        self.actors.add(Actor(name, birth_year))

    def list_movies(
        self,
        verbose=False,
        title_regex=None,
        director_regex=None,
        actor_regex=None,
        order=None,
    ):
        self.filtered_movies = list(self.movies)
        if title_regex:
            self.filtered_movies = [
                movie
                for movie in self.filtered_movies
                if re.search(title_regex, movie.title, re.IGNORECASE)
            ]
        if director_regex:
            self.filtered_movies = [
                movie
                for movie in self.filtered_movies
                if re.search(director_regex, movie.director, re.IGNORECASE)
            ]
        if actor_regex:
            self.filtered_movies = [
                movie
                for movie in self.filtered_movies
                if any(
                    re.search(actor_regex, actor.name, re.IGNORECASE)
                    for actor in movie.actors
                )
            ]

        if order == "asc":
            self.filtered_movies.sort(key=lambda x: (x.length, x.title))
        elif order == "desc":
            self.filtered_movies.sort(key=lambda x: (-x.length, x.title))
        else:
            self.filtered_movies.sort(key=lambda x: x.title)

        if verbose:
            for movie in self.filtered_movies:
                print(movie)
                print("\t Starring:")
                Actor.print_actor_list(movie.actors)
        else:
            for movie in self.filtered_movies:
                print(movie)


if __name__ == "__main__":

    database = Database_Handler("movies.json")
    database.load_database()

    parser = argparse.ArgumentParser(description="Movie Database Program")
    parser.add_argument("command", choices=["l", "a"], help="Command to execute")
    parser.add_argument("-v", action="store_true", help="Verbose output")
    parser.add_argument("-t", help="Filter by title regex")
    parser.add_argument("-d", help="Filter by director regex")
    parser.add_argument("-a", help="Filter by actor regex")
    parser.add_argument("-la", action="store_true", help="Sort by length ascending")
    parser.add_argument("-ld", action="store_true", help="Sort by length descending")

    parser.add_argument("-p", action="store_true", help="Add new person")
    parser.add_argument("-m", action="store_true", help="Add new movie")

    # args = parser.parse_args()

    # if args.command == "l":
    #     if args.la and args.ld:
    #         print(
    #             "Error: Cannot use both -la and -ld switches together. Default order will be used"
    #         )
    #         database.list_movies(args.v, args.t, args.d, args.a)
    #     else:
    #         order = "asc" if args.la else "desc" if args.ld else None
    #         database.list_movies(args.v, args.t, args.d, args.a, order)

    # elif args.command == 'a':
    #     if args.p:
    #         pass
    database.list_movies(verbose=True)
    new_movie = Movie(
        "Nagy vadászat",
        "Kis Cica",
        2024,
        135,
        [Actor("kis Lajos", 1955), Actor("Nagy Laj", 1988), Actor("Nagy cica", 2005)],
    )
    a = dict(new_movie)
    print(a)

    database.add_movie()
    database.list_movies(verbose=True)
