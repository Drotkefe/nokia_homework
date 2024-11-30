import json
from datetime import datetime
import argparse
import re
import os


class Actor:
    def __init__(self, name: str, birth_year: int):
        self.name = name
        self.birth_year = birth_year

    @staticmethod
    def calculate_age(movie_year: int, birth_year: int):
        return movie_year - birth_year

    def __str__(self):
        return f"{self.name}"

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

    def convert_hhmm_to_minutes(self):
        hours, minutes = map(int, self.length.split(":"))
        return hours * 60 + minutes

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
        self.movies_json_path = file_path
        self.actors_json_path = "actors.json"

    def __decoder(self, movie_data, actor_data):
        for movie in movie_data:
            starring = []
            for actor in movie["actors"]:
                new_actor = Actor(actor["name"], actor["birth_year"])
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
        for actor in actor_data:
            self.actors.add(Actor(actor["name"], actor["birth_year"]))

    def serialize_movies_to_json(self):
        data = []
        for m in self.movies:
            new_movie_dict = {
                "title": m.title,
                "director": m.director.__dict__,
                "release_year": m.release_year,
                "length": m.length,
                "actors": [a.__dict__ for a in m.actors],
            }
            data.append(new_movie_dict)
        return data

    def load_database(self):
        try:
            with open(self.movies_json_path, "r") as file:
                data = json.load(file, parse_int=int)
        except:
            print("Failed to load the movie database")
            exit()

        try:
            with open("actors.json", "r") as file:
                actor_data = json.load(file, parse_int=int)
        except:
            actor_data = []
        self.__decoder(data, actor_data)

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
        new_movie = {
            "title": new_movie.title,
            "director": new_movie.director.__dict__,
            "release_year": new_movie.release_year,
            "length": new_movie.length,
            "actors": [actor.__dict__ for actor in new_movie.actors],
        }
        try:
            with open(self.movies_json_path, "r+") as file:
                data = json.load(file)
                data.append(new_movie)
                file.seek(0)
                json.dump(data, file, indent=4)
        except:
            print("Failed to save the new movie into the database")

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
        new_movie = Movie(title, director, int(release_year), length, starring_list)
        new_movie.length = new_movie.convert_hhmm_to_minutes()
        self.movies.add(new_movie)
        self.__save_to_database(new_movie)

    def __save_actor(self, new_actor: Actor):
        new_actor = new_actor.__dict__
        try:
            if os.path.exists(self.actors_json_path):
                with open(self.actors_json_path, "r+") as file:
                    data = json.load(file)
                    data.append(new_actor)
                    file.seek(0)
                    json.dump(data, file, indent=4)
            else:
                new_actor = [new_actor]
                with open(self.actors_json_path, "w") as file:
                    json.dump(new_actor, file, indent=4)
        except:
            print("Failed to save the new Actor into the database")

    def add_actor(self):
        name = input("Name: ")
        birth_year = input("Birth year: ")
        while not birth_year.isdigit():
            print("Bad input format (only numbers), try again!")
            birth_year = input("Birth year: ")
        self.__save_actor(Actor(name, int(birth_year)))

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
                for actor in movie.actors:
                    print(
                        f"\t\t - {actor.name} at age {Actor.calculate_age(movie.release_year,actor.birth_year)}"
                    )
        else:
            for movie in self.filtered_movies:
                print(movie)

    def __check_actor_is_director(self, actor):
        for movie in self.movies:
            if movie.director == actor:
                return True
        return False

    def __delete_actor_from_movies(self, actor) -> bool:
        if self.__check_actor_is_director(actor):
            print("This person cannot be deleted, because he/she is a Director")
            return False
        for movie in self.movies:
            try:
                movie.actors.remove(actor)
            except ValueError:
                continue
        return True

    def __delete_person_by_name_from_database(self, name):
        try:
            with open(self.actors_json_path, "r") as file:
                data = json.load(file)
                data = [person for person in data if person["name"] != name]
            with open(self.actors_json_path, "w") as file:
                json.dump(data, file, indent=4)

        except FileNotFoundError:
            print(f"The file {self.actors_json_path} or  does not exist.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file {self.actors_json_path}.")

        try:
            with open(self.movies_json_path, "w") as file:
                json.dump(self.serialize_movies_to_json(), file, indent=4)

        except FileNotFoundError:
            print(f"The file {self.movies_json_path} or  does not exist.")

    def delete_actor(self, name):
        actor = self.__search_actor(name)
        if actor == None:
            print(f"We could not find '{name}', try again!")
            return
        if self.__delete_actor_from_movies(actor):
            self.actors.remove(actor)
            self.__delete_person_by_name_from_database(actor.name)


if __name__ == "__main__":
    database = Database_Handler("movies.json")
    database.load_database()
    parser = argparse.ArgumentParser(description="Movie Database Program")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # Create parser for 'l'
    parser_l = subparsers.add_parser("l", help="List database")
    parser_l.add_argument("-v", action="store_true", help="Verbose output")
    parser_l.add_argument("-t", help="Filter by title regex")
    parser_l.add_argument("-d", help="Filter by director regex")
    parser_l.add_argument("-a", help="Filter by actor regex")
    parser_l.add_argument("-la", action="store_true", help="Sort by length ascending")
    parser_l.add_argument("-ld", action="store_true", help="Sort by length descending")

    # Create parser for 'a'
    parser_a = subparsers.add_parser("a", help="Add a person")
    parser_a.add_argument("-p", action="store_true", help="Add new person")
    parser_a.add_argument("-m", action="store_true", help="Add new movie")

    # Create parser for 'd'
    parser_d = subparsers.add_parser("d", help="Delete a person")
    parser_d.add_argument(
        "-p", "--person", type=str, help="Name of the person to delete", required=True
    )

    args = parser.parse_args()

    if args.command == "l":
        if args.la and args.ld:
            print(
                "Error: Cannot use both -la and -ld switches together. Default order will be used"
            )
            database.list_movies(args.v, args.t, args.d, args.a)
        else:
            order = "asc" if args.la else "desc" if args.ld else None
            database.list_movies(args.v, args.t, args.d, args.a, order)

    elif args.command == "a":
        if args.p:
            database.add_actor()
        if args.m:
            database.add_movie()

    elif args.command == "d":
        if args.person:
            database.delete_actor(args.person)
