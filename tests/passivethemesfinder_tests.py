from unittest import TestCase

from vane.passivethemesfinder import PassiveThemesFinder
from vane.theme import Theme

from os.path import join, dirname


class TestPassiveThemesFinder(TestCase):

    def setUp(self):
        self.themes_finder = PassiveThemesFinder()

    def test_contains_theme_url_return_false_if_not_valid_theme_url(self):
        url = "https://www.url.com/path/to/page/"

        self.assertFalse(self.themes_finder._contains_theme_url(url))

    def test_contains_theme_url_return_true_if_theme_url_in_string(self):
        url = "A string with a theme url. http://static.blog.playstation.com/wp-content/themes/twenty11/ie8.css?m=1480446942"

        self.assertTrue(self.themes_finder._contains_theme_url(url))

    def test_contains_theme_url_return_true_if_vip_theme_url_in_string(self):
        url = "A string with a vip theme url https://s0.wp.com/wp-content/themes/vip/fortune/static/js/html5shiv.min.js " \
              "and random characters at the end."

        self.assertTrue(self.themes_finder._contains_theme_url(url))

    def test_contains_theme_url_return_true_if_theme_url_is_relative(self):
        relative_url = "this is the theme url: /wp-content/themes/my-theme/style.css"

        self.assertTrue(self.themes_finder._contains_theme_url(relative_url))

    def test_get_theme_url_from_string_remove_beginning_of_string_not_part_of_the_url(self):
        string = 'beginning of string ... http://static.blog.playstation.com/wp-content/themes/twenty11'

        self.assertEqual(self.themes_finder._get_theme_url_from_string(string),
                         "http://static.blog.playstation.com/wp-content/themes/twenty11")

    def test_get_theme_url_from_string_remove_part_after_theme_name(self):
        url = "http://static.blog.playstation.com/wp-content/themes/twenty11/ie8.css?m=1480446942"

        self.assertEqual(self.themes_finder._get_theme_url_from_string(url),
                         "http://static.blog.playstation.com/wp-content/themes/twenty11")

    def test_get_theme_url_from_string_return_return_relative_url(self):
        relative_url = "this is the theme url: /wp-content/themes/my-theme/style.css"

        self.assertEqual(self.themes_finder._get_theme_url_from_string(relative_url), "/wp-content/themes/my-theme")

    def test_list_themes_find_themes_in_page_source(self):
        sample_page0 = join(dirname(__file__), "samples/playstation.html")
        sample_page1 = join(dirname(__file__), "samples/delvelabs.html")

        themes0 = self.themes_finder.list_themes(sample_page0)
        themes1 = self.themes_finder.list_themes(sample_page1)

        self.assertIn("twenty11", (theme.name for theme in themes0))
        self.assertIn("kratos", (theme.name for theme in themes0))
        self.assertEqual(len(themes0), 2)

        self.assertIn("delvelabs", (theme.name for theme in themes1))
        self.assertEqual(len(themes1), 1)

    def test_list_themes_find_theme_in_comments_with_theme_url(self):
        sample_page = join(dirname(__file__), "samples/comment.html")

        themes = self.themes_finder.list_themes(sample_page)

        self.assertIn("twenty11", (theme.name for theme in themes))