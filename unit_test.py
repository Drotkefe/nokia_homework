from project import Database_Handler, Actor, Movie
import unittest
from unittest.mock import patch
from io import StringIO


class TestMovieDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database_Handler("mock.json")
        movies = [
            Movie(
                "Inception",
                Actor("Christopher Nolan", 1970),
                2010,
                148,
                [Actor("Leonardo DiCaprio", 1974), Actor("Joseph Gordon-Levitt", 1981)],
            ),
            Movie(
                "Pulp Fiction",
                Actor("Quentin Tarantino", 1963),
                1994,
                154,
                [Actor("John Travolta", 1954), Actor("Samuel L. Jackson", 1948)],
            ),
        ]
        self.database.movies = movies
        actors = [
            Actor("Leonardo DiCaprio", 1974),
            Actor("Joseph Gordon-Levitt", 1981),
            Actor("Christopher Nolan", 1970),
        ]
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

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_movies_title_regex(self, mock_stdout):
        self.database.list_movies(verbose=False, title_regex="Pulp .*")
        output = mock_stdout.getvalue().strip()
        self.assertEqual("Pulp Fiction by Quentin Tarantino in 1994, 02:34", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_movies_director_regex(self, mock_stdout):
        self.database.list_movies(verbose=False, director_regex=r"Tarantino")
        output = mock_stdout.getvalue().strip()
        self.assertEqual("Pulp Fiction by Quentin Tarantino in 1994, 02:34", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_movies_actor_regex(self, mock_stdout):
        self.database.list_movies(verbose=True, actor_regex=r"DiCaprio")
        output = mock_stdout.getvalue().strip()
        self.assertIn("Inception by Christopher Nolan in 2010, 02:28", output)
        self.assertIn("Starring:", output)
        self.assertIn("- Leonardo DiCaprio at age 36", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_movies_multiple_regex(self, mock_stdout):
        self.database.list_movies(
            verbose=False,
            title_regex=r"Incep",
            director_regex="Christopher .*",
            actor_regex=r"DiCaprio",
        )
        output = mock_stdout.getvalue().strip()
        self.assertEqual("Inception by Christopher Nolan in 2010, 02:28", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_movies_regex_fail(self, mock_stdout):
        self.database.list_movies(verbose=True, title_regex="58$fs}d*.$f[dsf$")
        output = mock_stdout.getvalue().strip()
        self.assertEqual("Non valid regex pattern", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_movies_order_by_asc(self, mock_stdout):
        self.database.list_movies(order="asc")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(
            "Inception by Christopher Nolan in 2010, 02:28\nPulp Fiction by Quentin Tarantino in 1994, 02:34",
            output,
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_movies_order_by_desc(self, mock_stdout):
        self.database.list_movies(order="desc")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(
            "Pulp Fiction by Quentin Tarantino in 1994, 02:34\nInception by Christopher Nolan in 2010, 02:28",
            output,
        )


if __name__ == "__main__":
    unittest.main()
