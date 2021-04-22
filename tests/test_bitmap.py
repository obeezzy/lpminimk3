import unittest
from lpminimk3.graphics import Bitmap
from lpminimk3.graphics.art import Bitmaps
from lpminimk3.colors import ColorPalette
from tests._vlpminimk3 import create_virtual_launchpad


class TestBitmap(unittest.TestCase):
    def setUp(self):
        self.lp = create_virtual_launchpad()
        self.lp.open()

    def tearDown(self):
        self.lp.close()

    def test_init(self):
        bitmap = Bitmap(Bitmaps.SMILEY)
        self.assertEqual(bitmap.word_count, 8, 'Word count mismatch.')
        self.assertListEqual([0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 1, 1, 1, 1, 0, 0,
                              0, 1, 1, 1, 1, 1, 1, 0,
                              0, 1, 1, 1, 1, 1, 1, 0,
                              0, 1, 1, 1, 1, 1, 1, 0,
                              0, 1, 1, 1, 1, 1, 1, 0,
                              0, 0, 1, 1, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(bitmap.bits),
                             'Bit mismatch.')

    def test_fg_color(self):
        bitmap = Bitmap(Bitmaps.SMILEY)
        self.assertIsNotNone(bitmap.fg_color, 'Text color is None.')
        bitmap.fg_color = 0
        bitmap.fg_color = ColorPalette.Red.SHADE_1
        bitmap.fg_color = ColorPalette.Orange.SHADE_1
        bitmap.fg_color = ColorPalette.Yellow.SHADE_1
        bitmap.fg_color = ColorPalette.Green.SHADE_1
        bitmap.fg_color = ColorPalette.Blue.SHADE_1
        bitmap.fg_color = ColorPalette.Violet.SHADE_1
        bitmap.fg_color = ColorPalette.White.SHADE_1
        bitmap.fg_color = 'r'
        bitmap.fg_color = 'o'
        bitmap.fg_color = 'y'
        bitmap.fg_color = 'g'
        bitmap.fg_color = 'b'
        bitmap.fg_color = 'v'
        bitmap.fg_color = 'w'
        bitmap.fg_color = 'r1'
        bitmap.fg_color = 'o1'
        bitmap.fg_color = 'y1'
        bitmap.fg_color = 'g1'
        bitmap.fg_color = 'b1'
        bitmap.fg_color = 'v1'
        bitmap.fg_color = 'w1'
        bitmap.fg_color = 'red'
        bitmap.fg_color = 'orange'
        bitmap.fg_color = 'yellow'
        bitmap.fg_color = 'green'
        bitmap.fg_color = 'blue'
        bitmap.fg_color = 'violet'
        bitmap.fg_color = 'white'
        bitmap.fg_color = 'red1'
        bitmap.fg_color = 'orange1'
        bitmap.fg_color = 'yellow1'
        bitmap.fg_color = 'green1'
        bitmap.fg_color = 'blue1'
        bitmap.fg_color = 'violet1'
        bitmap.fg_color = 'red0'
        bitmap.fg_color = 'orange0'
        bitmap.fg_color = 'yellow0'
        bitmap.fg_color = 'green0'
        bitmap.fg_color = 'blue0'
        bitmap.fg_color = 'violet0'
        bitmap.fg_color = 'white0'

        bitmap.fg_color.set(1)
        bitmap.fg_color.set(ColorPalette.Red.SHADE_1)
        bitmap.fg_color.set('red')
        self.assertIsNotNone(bitmap.fg_color.set('blue').fg_color,
                             'Unable to retrieve fg_color.')

        with self.assertRaises(ValueError):
            bitmap.fg_color = '1r'
        with self.assertRaises(ValueError):
            bitmap.fg_color = 're'
        with self.assertRaises(ValueError):
            bitmap.fg_color = 'gree3'
        with self.assertRaises(TypeError):
            bitmap.fg_color = (0, 0)
        with self.assertRaises(ValueError):
            bitmap.fg_color = 'blue-0'
        with self.assertRaises(ValueError):
            bitmap.fg_color = 'yellow-1'

    def test_bg_color(self):
        bitmap = Bitmap(Bitmaps.SMILEY)
        self.assertIsNotNone(bitmap.bg_color, 'Text color is None.')
        bitmap.bg_color = 0
        bitmap.bg_color = ColorPalette.Red.SHADE_1
        bitmap.bg_color = ColorPalette.Orange.SHADE_1
        bitmap.bg_color = ColorPalette.Yellow.SHADE_1
        bitmap.bg_color = ColorPalette.Green.SHADE_1
        bitmap.bg_color = ColorPalette.Blue.SHADE_1
        bitmap.bg_color = ColorPalette.Violet.SHADE_1
        bitmap.bg_color = ColorPalette.White.SHADE_1
        bitmap.bg_color = 'r'
        bitmap.bg_color = 'o'
        bitmap.bg_color = 'y'
        bitmap.bg_color = 'g'
        bitmap.bg_color = 'b'
        bitmap.bg_color = 'v'
        bitmap.bg_color = 'w'
        bitmap.bg_color = 'r1'
        bitmap.bg_color = 'o1'
        bitmap.bg_color = 'y1'
        bitmap.bg_color = 'g1'
        bitmap.bg_color = 'b1'
        bitmap.bg_color = 'v1'
        bitmap.bg_color = 'w1'
        bitmap.bg_color = 'red'
        bitmap.bg_color = 'orange'
        bitmap.bg_color = 'yellow'
        bitmap.bg_color = 'green'
        bitmap.bg_color = 'blue'
        bitmap.bg_color = 'violet'
        bitmap.bg_color = 'white'
        bitmap.bg_color = 'red1'
        bitmap.bg_color = 'orange1'
        bitmap.bg_color = 'yellow1'
        bitmap.bg_color = 'green1'
        bitmap.bg_color = 'blue1'
        bitmap.bg_color = 'violet1'
        bitmap.bg_color = 'red0'
        bitmap.bg_color = 'orange0'
        bitmap.bg_color = 'yellow0'
        bitmap.bg_color = 'green0'
        bitmap.bg_color = 'blue0'
        bitmap.bg_color = 'violet0'
        bitmap.bg_color = 'white0'

        bitmap.bg_color.set(1)
        bitmap.bg_color.set(ColorPalette.Red.SHADE_1)
        bitmap.bg_color.set('red')
        self.assertIsNotNone(bitmap.bg_color.set('blue').bg_color,
                             'Unable to retrieve bg_color.')

        with self.assertRaises(ValueError):
            bitmap.bg_color = '1r'
        with self.assertRaises(ValueError):
            bitmap.bg_color = 're'
        with self.assertRaises(ValueError):
            bitmap.bg_color = 'gree3'
        with self.assertRaises(TypeError):
            bitmap.bg_color = (0, 0)
        with self.assertRaises(ValueError):
            bitmap.bg_color = 'blue-0'
        with self.assertRaises(ValueError):
            bitmap.bg_color = 'yellow-1'

    def test_render(self):
        self.lp.grid.render(Bitmap(Bitmaps.SMILEY))

    def test_print(self):
        Bitmap(Bitmaps.SMILEY).print()

    def test_swap_colors(self):
        text = Bitmap(Bitmaps.SMILEY,
                      fg_color=ColorPalette.Red.SHADE_1,
                      bg_color=ColorPalette.White.SHADE_1)

        self.assertEqual(text.fg_color.color_id,
                         ColorPalette.Red.SHADE_1.color_id,
                         'Color mismatch.')
        self.assertEqual(text.bg_color.color_id,
                         ColorPalette.White.SHADE_1.color_id,
                         'Color mismatch.')

        text.swap_colors()

        self.assertEqual(text.fg_color.color_id,
                         ColorPalette.White.SHADE_1.color_id,
                         'Color mismatch.')
        self.assertEqual(text.bg_color.color_id,
                         ColorPalette.Red.SHADE_1.color_id,
                         'Color mismatch.')


if __name__ == '__main__':
    unittest.main()
