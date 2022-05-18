import unittest
from lpminimk3.graphics import Movie
from lpminimk3.graphics.art import Movies
from lpminimk3.colors import ColorPalette
from tests._vlpminimk3 import create_virtual_launchpad


class TestMovie(unittest.TestCase):
    def setUp(self):
        self.lp = create_virtual_launchpad()
        self.lp.open()

    def tearDown(self):
        self.lp.close()

    def test_init(self):
        movie = Movie(Movies.PING_PONG)
        self.assertEqual(movie.word_count, 8, 'Word count mismatch.')
        self.assertListEqual([1, 0, 0, 0, 0, 0, 0, 1,
                              1, 0, 0, 0, 0, 0, 0, 1,
                              1, 0, 0, 0, 0, 0, 0, 1,
                              1, 1, 1, 0, 0, 0, 0, 1,
                              1, 1, 1, 0, 0, 0, 0, 1,
                              1, 0, 0, 0, 0, 0, 0, 1,
                              1, 0, 0, 0, 0, 0, 0, 1,
                              1, 0, 0, 0, 0, 0, 0, 1],
                             list(movie.bits),
                             'Bit mismatch.')

    def test_fg_color(self):
        movie = Movie(Movies.PING_PONG)
        self.assertIsNotNone(movie.fg_color, 'Movie color is None.')
        movie.fg_color = 0
        movie.fg_color = ColorPalette.Red.SHADE_1
        movie.fg_color = ColorPalette.Orange.SHADE_1
        movie.fg_color = ColorPalette.Yellow.SHADE_1
        movie.fg_color = ColorPalette.Green.SHADE_1
        movie.fg_color = ColorPalette.Blue.SHADE_1
        movie.fg_color = ColorPalette.Violet.SHADE_1
        movie.fg_color = ColorPalette.White.SHADE_1
        movie.fg_color = 'r'
        movie.fg_color = 'o'
        movie.fg_color = 'y'
        movie.fg_color = 'g'
        movie.fg_color = 'b'
        movie.fg_color = 'v'
        movie.fg_color = 'w'
        movie.fg_color = 'r1'
        movie.fg_color = 'o1'
        movie.fg_color = 'y1'
        movie.fg_color = 'g1'
        movie.fg_color = 'b1'
        movie.fg_color = 'v1'
        movie.fg_color = 'w1'
        movie.fg_color = 'red'
        movie.fg_color = 'orange'
        movie.fg_color = 'yellow'
        movie.fg_color = 'green'
        movie.fg_color = 'blue'
        movie.fg_color = 'violet'
        movie.fg_color = 'white'
        movie.fg_color = 'red1'
        movie.fg_color = 'orange1'
        movie.fg_color = 'yellow1'
        movie.fg_color = 'green1'
        movie.fg_color = 'blue1'
        movie.fg_color = 'violet1'
        movie.fg_color = 'red0'
        movie.fg_color = 'orange0'
        movie.fg_color = 'yellow0'
        movie.fg_color = 'green0'
        movie.fg_color = 'blue0'
        movie.fg_color = 'violet0'
        movie.fg_color = 'white0'
        movie.fg_color = '#fff'
        movie.fg_color = '#ff0000'
        movie.fg_color = (0, 0, 255)

        movie.fg_color.set(1)
        movie.fg_color.set(ColorPalette.Red.SHADE_1)
        movie.fg_color.set('red')
        self.assertIsNotNone(movie.fg_color.set('blue').fg_color,
                             'Unable to retrieve fg_color.')

        with self.assertRaises(ValueError):
            movie.fg_color = '1r'
        with self.assertRaises(ValueError):
            movie.fg_color = 're'
        with self.assertRaises(ValueError):
            movie.fg_color = 'gree3'
        with self.assertRaises(ValueError):
            movie.fg_color = (0, 0)
        with self.assertRaises(ValueError):
            movie.fg_color = (-1, 0, -1)
        with self.assertRaises(ValueError):
            movie.fg_color = (257, 277, 99)
        with self.assertRaises(ValueError):
            movie.fg_color = '#ga1'
        with self.assertRaises(ValueError):
            movie.fg_color = 'blue-0'
        with self.assertRaises(ValueError):
            movie.fg_color = 'yellow-1'

    def test_bg_color(self):
        movie = Movie(Movies.PING_PONG)
        self.assertIsNotNone(movie.bg_color, 'Movie color is None.')
        movie.bg_color = 0
        movie.bg_color = ColorPalette.Red.SHADE_1
        movie.bg_color = ColorPalette.Orange.SHADE_1
        movie.bg_color = ColorPalette.Yellow.SHADE_1
        movie.bg_color = ColorPalette.Green.SHADE_1
        movie.bg_color = ColorPalette.Blue.SHADE_1
        movie.bg_color = ColorPalette.Violet.SHADE_1
        movie.bg_color = ColorPalette.White.SHADE_1
        movie.bg_color = 'r'
        movie.bg_color = 'o'
        movie.bg_color = 'y'
        movie.bg_color = 'g'
        movie.bg_color = 'b'
        movie.bg_color = 'v'
        movie.bg_color = 'w'
        movie.bg_color = 'r1'
        movie.bg_color = 'o1'
        movie.bg_color = 'y1'
        movie.bg_color = 'g1'
        movie.bg_color = 'b1'
        movie.bg_color = 'v1'
        movie.bg_color = 'w1'
        movie.bg_color = 'red'
        movie.bg_color = 'orange'
        movie.bg_color = 'yellow'
        movie.bg_color = 'green'
        movie.bg_color = 'blue'
        movie.bg_color = 'violet'
        movie.bg_color = 'white'
        movie.bg_color = 'red1'
        movie.bg_color = 'orange1'
        movie.bg_color = 'yellow1'
        movie.bg_color = 'green1'
        movie.bg_color = 'blue1'
        movie.bg_color = 'violet1'
        movie.bg_color = 'red0'
        movie.bg_color = 'orange0'
        movie.bg_color = 'yellow0'
        movie.bg_color = 'green0'
        movie.bg_color = 'blue0'
        movie.bg_color = 'violet0'
        movie.bg_color = 'white0'
        movie.fg_color = '#fff'
        movie.fg_color = '#ff0000'
        movie.fg_color = (0, 0, 255)

        movie.bg_color.set(1)
        movie.bg_color.set(ColorPalette.Red.SHADE_1)
        movie.bg_color.set('red')
        self.assertIsNotNone(movie.bg_color.set('blue').bg_color,
                             'Unable to retrieve bg_color.')

        with self.assertRaises(ValueError):
            movie.bg_color = '1r'
        with self.assertRaises(ValueError):
            movie.bg_color = 're'
        with self.assertRaises(ValueError):
            movie.bg_color = 'gree3'
        with self.assertRaises(ValueError):
            movie.bg_color = (0, 0)
        with self.assertRaises(ValueError):
            movie.bg_color = (-1, 0, -1)
        with self.assertRaises(ValueError):
            movie.bg_color = (257, 277, 99)
        with self.assertRaises(ValueError):
            movie.bg_color = '#ga1'
        with self.assertRaises(ValueError):
            movie.bg_color = 'blue-0'
        with self.assertRaises(ValueError):
            movie.bg_color = 'yellow-1'

    def test_render(self):
        self.lp.grid.render(Movie(Movies.PING_PONG))

    def test_print(self):
        Movie(Movies.PING_PONG).print()

    def test_swap_colors(self):
        movie = Movie(Movies.PING_PONG,
                      fg_color=ColorPalette.Red.SHADE_1,
                      bg_color=ColorPalette.White.SHADE_1)

        self.assertEqual(movie.fg_color.color_id,
                         ColorPalette.Red.SHADE_1.color_id,
                         'Color mismatch.')
        self.assertEqual(movie.bg_color.color_id,
                         ColorPalette.White.SHADE_1.color_id,
                         'Color mismatch.')

        movie.swap_colors()

        self.assertEqual(movie.fg_color.color_id,
                         ColorPalette.White.SHADE_1.color_id,
                         'Color mismatch.')
        self.assertEqual(movie.bg_color.color_id,
                         ColorPalette.Red.SHADE_1.color_id,
                         'Color mismatch.')


if __name__ == '__main__':
    unittest.main()
