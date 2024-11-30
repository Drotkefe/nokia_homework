from project import Database_Handler, Actor, Movie
import unittest
from unittest.mock import patch
from io import StringIO
import re


class TestMovieDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database_Handler("mock.json")
        movies = [
            Movie(
                "Inception",
                "Christopher Nolan",
                2010,
                148,
                [Actor("Leonardo DiCaprio", 1974), Actor("Joseph Gordon-Levitt", 1981)],
            )
        ]
        self.database.movies = movies
        actors = [Actor("Leonardo DiCaprio", 1974), Actor("Joseph Gordon-Levitt", 1981)]
        self.database.actors = actors

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_movies(self, mock_stdout):
        self.database.list_movies()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Inception by Christopher Nolan in 2010, 02:28", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_movies_verbose(self, mock_stdout):
        self.database.list_movies(verbose=True)
        output = mock_stdout.getvalue().strip()
        self.assertIn("Inception by Christopher Nolan in 2010, 02:28", output)
        self.assertIn("Starring:", output)
        self.assertIn("- Leonardo DiCaprio at age 36", output)


if __name__ == "__main__":
    unittest.main()
