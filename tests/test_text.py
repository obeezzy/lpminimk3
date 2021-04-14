import unittest
from lpminimk3.graphics import Text
from lpminimk3.colors import ColorPalette
from tests._vlpminimk3 import create_virtual_launchpad


class TestText(unittest.TestCase):
    def setUp(self):
        self.lp = create_virtual_launchpad()
        self.lp.open()

    def tearDown(self):
        self.lp.close()

    def test_init(self):
        text = Text()
        self.assertEqual(str(text), '', 'Text mismatch.')
        self.assertEqual(len(text), 0, 'Text length mismatch.')
        self.assertEqual(text.word_count, 8, 'Word count mismatch.')
        self.assertListEqual([0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('')
        self.assertEqual(str(text), '', 'Text mismatch.')
        self.assertEqual(len(text), 0, 'Text length mismatch.')
        self.assertEqual(text.word_count, 8, 'Word count mismatch.')
        self.assertListEqual([0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A')
        self.assertEqual(str(text), 'A', 'Text mismatch.')
        self.assertEqual(len(text), 1, 'Text length mismatch.')
        self.assertEqual(text.word_count, 8, 'Word count mismatch.')
        self.assertListEqual([0, 0, 1, 1, 0, 0, 0, 0,
                              0, 1, 1, 1, 1, 0, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 1, 1, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('Apple')
        self.assertEqual(str(text), 'Apple', 'Text mismatch.')
        self.assertEqual(len(text), 5, 'Text length mismatch.')
        self.assertEqual(text.word_count, 8, 'Word count mismatch.')
        self.assertListEqual([0, 0, 1, 1, 0, 0, 0, 0,
                              0, 1, 1, 1, 1, 0, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 1, 1, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')

    def test_fg_color(self):
        text = Text('A')
        self.assertIsNotNone(text.fg_color, 'Text color is None.')
        text.fg_color = 0
        text.fg_color = ColorPalette.Red.SHADE_1
        text.fg_color = ColorPalette.Orange.SHADE_1
        text.fg_color = ColorPalette.Yellow.SHADE_1
        text.fg_color = ColorPalette.Green.SHADE_1
        text.fg_color = ColorPalette.Blue.SHADE_1
        text.fg_color = ColorPalette.Violet.SHADE_1
        text.fg_color = ColorPalette.White.SHADE_1
        text.fg_color = 'r'
        text.fg_color = 'o'
        text.fg_color = 'y'
        text.fg_color = 'g'
        text.fg_color = 'b'
        text.fg_color = 'v'
        text.fg_color = 'w'
        text.fg_color = 'r1'
        text.fg_color = 'o1'
        text.fg_color = 'y1'
        text.fg_color = 'g1'
        text.fg_color = 'b1'
        text.fg_color = 'v1'
        text.fg_color = 'w1'
        text.fg_color = 'red'
        text.fg_color = 'orange'
        text.fg_color = 'yellow'
        text.fg_color = 'green'
        text.fg_color = 'blue'
        text.fg_color = 'violet'
        text.fg_color = 'white'
        text.fg_color = 'red1'
        text.fg_color = 'orange1'
        text.fg_color = 'yellow1'
        text.fg_color = 'green1'
        text.fg_color = 'blue1'
        text.fg_color = 'violet1'
        text.fg_color = 'red0'
        text.fg_color = 'orange0'
        text.fg_color = 'yellow0'
        text.fg_color = 'green0'
        text.fg_color = 'blue0'
        text.fg_color = 'violet0'
        text.fg_color = 'white0'

        with self.assertRaises(ValueError):
            text.fg_color = '1r'
        with self.assertRaises(ValueError):
            text.fg_color = 're'
        with self.assertRaises(ValueError):
            text.fg_color = 'gree3'
        with self.assertRaises(TypeError):
            text.fg_color = (0, 0)
        with self.assertRaises(ValueError):
            text.fg_color = 'blue-0'
        with self.assertRaises(ValueError):
            text.fg_color = 'yellow-1'

    def test_bg_color(self):
        text = Text('A')
        self.assertIsNotNone(text.bg_color, 'Text color is None.')
        text.bg_color = 0
        text.bg_color = ColorPalette.Red.SHADE_1
        text.bg_color = ColorPalette.Orange.SHADE_1
        text.bg_color = ColorPalette.Yellow.SHADE_1
        text.bg_color = ColorPalette.Green.SHADE_1
        text.bg_color = ColorPalette.Blue.SHADE_1
        text.bg_color = ColorPalette.Violet.SHADE_1
        text.bg_color = ColorPalette.White.SHADE_1
        text.bg_color = 'r'
        text.bg_color = 'o'
        text.bg_color = 'y'
        text.bg_color = 'g'
        text.bg_color = 'b'
        text.bg_color = 'v'
        text.bg_color = 'w'
        text.bg_color = 'r1'
        text.bg_color = 'o1'
        text.bg_color = 'y1'
        text.bg_color = 'g1'
        text.bg_color = 'b1'
        text.bg_color = 'v1'
        text.bg_color = 'w1'
        text.bg_color = 'red'
        text.bg_color = 'orange'
        text.bg_color = 'yellow'
        text.bg_color = 'green'
        text.bg_color = 'blue'
        text.bg_color = 'violet'
        text.bg_color = 'white'
        text.bg_color = 'red1'
        text.bg_color = 'orange1'
        text.bg_color = 'yellow1'
        text.bg_color = 'green1'
        text.bg_color = 'blue1'
        text.bg_color = 'violet1'
        text.bg_color = 'red0'
        text.bg_color = 'orange0'
        text.bg_color = 'yellow0'
        text.bg_color = 'green0'
        text.bg_color = 'blue0'
        text.bg_color = 'violet0'
        text.bg_color = 'white0'

        with self.assertRaises(ValueError):
            text.bg_color = '1r'
        with self.assertRaises(ValueError):
            text.bg_color = 're'
        with self.assertRaises(ValueError):
            text.bg_color = 'gree3'
        with self.assertRaises(TypeError):
            text.bg_color = (0, 0)
        with self.assertRaises(ValueError):
            text.bg_color = 'blue-0'
        with self.assertRaises(ValueError):
            text.bg_color = 'yellow-1'

    def test_shift_left_character(self):
        text = Text('A').shift(-1)
        self.assertListEqual([0, 1, 1, 0, 0, 0, 0, 0,
                              1, 1, 1, 1, 0, 0, 0, 0,
                              1, 0, 0, 1, 1, 0, 0, 1,
                              1, 0, 0, 1, 1, 0, 0, 1,
                              1, 1, 1, 1, 1, 0, 0, 1,
                              1, 0, 0, 1, 1, 0, 0, 1,
                              1, 0, 0, 1, 1, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text.shift(-1)
        self.assertListEqual([1, 1, 0, 0, 0, 0, 0, 0,
                              1, 1, 1, 0, 0, 0, 0, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              1, 1, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').shift(-1).shift(-1)
        self.assertListEqual([1, 1, 0, 0, 0, 0, 0, 0,
                              1, 1, 1, 0, 0, 0, 0, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              1, 1, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').shift(-2)
        self.assertListEqual([1, 1, 0, 0, 0, 0, 0, 0,
                              1, 1, 1, 0, 0, 0, 0, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              1, 1, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').shift(-2, circular=True)
        self.assertListEqual([1, 1, 0, 0, 0, 0, 0, 0,
                              1, 1, 1, 0, 0, 0, 0, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              1, 1, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').shift(-2, circular=False)
        self.assertListEqual([1, 1, 0, 0, 0, 0, 0, 0,
                              1, 1, 1, 0, 0, 0, 0, 0,
                              0, 0, 1, 1, 0, 0, 0, 0,
                              0, 0, 1, 1, 0, 0, 0, 0,
                              1, 1, 1, 1, 0, 0, 0, 0,
                              0, 0, 1, 1, 0, 0, 0, 0,
                              0, 0, 1, 1, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')

    def test_shift_left_string(self):
        text = Text('Apple').shift(-1)
        self.assertListEqual([0, 1, 1, 0, 0, 0, 0, 0,
                              1, 1, 1, 1, 0, 0, 0, 0,
                              1, 0, 0, 1, 1, 0, 0, 1,
                              1, 0, 0, 1, 1, 0, 0, 0,
                              1, 1, 1, 1, 1, 0, 0, 0,
                              1, 0, 0, 1, 1, 0, 0, 0,
                              1, 0, 0, 1, 1, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 1],
                             list(text.bits),
                             'Text mismatch.')
        text.shift(-1)
        self.assertListEqual([1, 1, 0, 0, 0, 0, 0, 0,
                              1, 1, 1, 0, 0, 0, 0, 0,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 0, 1,
                              1, 1, 1, 1, 0, 0, 0, 1,
                              0, 0, 1, 1, 0, 0, 0, 1,
                              0, 0, 1, 1, 0, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 1, 1],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('Apple').shift(-1).shift(-1)
        self.assertListEqual([1, 1, 0, 0, 0, 0, 0, 0,
                              1, 1, 1, 0, 0, 0, 0, 0,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 0, 1,
                              1, 1, 1, 1, 0, 0, 0, 1,
                              0, 0, 1, 1, 0, 0, 0, 1,
                              0, 0, 1, 1, 0, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 1, 1],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('Apple').shift(-2)
        self.assertListEqual([1, 1, 0, 0, 0, 0, 0, 0,
                              1, 1, 1, 0, 0, 0, 0, 0,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 0, 1,
                              1, 1, 1, 1, 0, 0, 0, 1,
                              0, 0, 1, 1, 0, 0, 0, 1,
                              0, 0, 1, 1, 0, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 1, 1],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('Apple').shift(-7 * len('Apple'), circular=True)
        self.assertListEqual([0, 0, 0, 0, 0, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 1, 1,
                              1, 1, 0, 0, 0, 1, 1, 0,
                              0, 1, 1, 0, 0, 1, 1, 0,
                              1, 1, 1, 0, 0, 1, 1, 1,
                              0, 0, 0, 0, 0, 1, 1, 0,
                              1, 1, 0, 0, 0, 1, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('Apple').shift(-7 * len('Apple'), circular=False)
        self.assertListEqual([0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              1, 1, 0, 0, 0, 0, 0, 0,
                              0, 1, 1, 0, 0, 0, 0, 0,
                              1, 1, 1, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              1, 1, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')

    def test_shift_right_character(self):
        text = Text('A').shift()
        self.assertListEqual([0, 0, 0, 1, 1, 0, 0, 0,
                              0, 0, 1, 1, 1, 1, 0, 0,
                              0, 1, 1, 0, 0, 1, 1, 0,
                              0, 1, 1, 0, 0, 1, 1, 0,
                              0, 1, 1, 1, 1, 1, 1, 0,
                              0, 1, 1, 0, 0, 1, 1, 0,
                              0, 1, 1, 0, 0, 1, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text.shift(1)
        self.assertListEqual([0, 0, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 1, 1, 1, 1, 0,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 1, 1, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').shift(1).shift(1)
        self.assertListEqual([0, 0, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 1, 1, 1, 1, 0,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 1, 1, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').shift(2)
        self.assertListEqual([0, 0, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 1, 1, 1, 1, 0,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 1, 1, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').shift(3, circular=True)
        self.assertListEqual([0, 0, 0, 0, 0, 1, 1, 0,
                              1, 0, 0, 0, 1, 1, 1, 1,
                              1, 0, 0, 1, 1, 0, 0, 1,
                              1, 0, 0, 1, 1, 0, 0, 1,
                              1, 0, 0, 1, 1, 1, 1, 1,
                              1, 0, 0, 1, 1, 0, 0, 1,
                              0, 0, 0, 1, 1, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').shift(3, circular=False)
        self.assertListEqual([0, 0, 0, 0, 0, 1, 1, 0,
                              0, 0, 0, 0, 1, 1, 1, 1,
                              0, 0, 0, 1, 1, 0, 0, 1,
                              0, 0, 0, 1, 1, 0, 0, 1,
                              0, 0, 0, 1, 1, 1, 1, 1,
                              0, 0, 0, 1, 1, 0, 0, 1,
                              0, 0, 0, 1, 1, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')

    def test_shift_right_string(self):
        text = Text('Avenger').shift()
        self.assertListEqual([0, 0, 0, 1, 1, 0, 0, 0,
                              0, 0, 1, 1, 1, 1, 0, 0,
                              0, 1, 1, 0, 0, 1, 1, 0,
                              0, 1, 1, 0, 0, 1, 1, 0,
                              0, 1, 1, 1, 1, 1, 1, 0,
                              0, 1, 1, 0, 0, 1, 1, 0,
                              0, 1, 1, 0, 0, 1, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text.shift(1)
        self.assertListEqual([0, 0, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 1, 1, 1, 1, 0,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              1, 0, 1, 1, 0, 0, 1, 1,
                              1, 0, 1, 1, 1, 1, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('Avenger').shift().shift()
        self.assertListEqual([0, 0, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 1, 1, 1, 1, 0,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              1, 0, 1, 1, 0, 0, 1, 1,
                              1, 0, 1, 1, 1, 1, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('Avenger').shift(2)
        self.assertListEqual([0, 0, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 1, 1, 1, 1, 0,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              1, 0, 1, 1, 0, 0, 1, 1,
                              1, 0, 1, 1, 1, 1, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 1, 1, 0, 0, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('Avenger').shift(len('Avenger'), circular=True)  # noqa
        self.assertListEqual([0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              1, 0, 1, 1, 1, 0, 0, 1,
                              1, 0, 1, 0, 1, 1, 0, 1,
                              1, 1, 0, 0, 1, 1, 0, 1,
                              1, 1, 0, 0, 0, 0, 0, 1,
                              1, 1, 1, 0, 0, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('Avenger').shift(len('Avenger'), circular=False)  # noqa
        self.assertListEqual([0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 0, 1,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')

    def test_scroll(self):
        text = Text('Apple').scroll(count=1, period=.0001)
        self.lp.grid.render(text)
        self.assertListEqual([0, 0, 1, 1, 0, 0, 0, 0,
                              0, 1, 1, 1, 1, 0, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 1, 1, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')

    def test_rotate(self):
        text = Text('A').rotate(0)
        self.assertListEqual([0, 0, 1, 1, 0, 0, 0, 0,
                              0, 1, 1, 1, 1, 0, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 1, 1, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').rotate(90)
        self.assertListEqual([0, 0, 1, 1, 0, 0, 0, 0,
                              0, 1, 1, 1, 1, 0, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 1, 1, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').rotate(180)
        self.assertListEqual([0, 0, 1, 1, 0, 0, 0, 0,
                              0, 1, 1, 1, 1, 0, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 1, 1, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')
        text = Text('A').rotate(270)
        self.assertListEqual([0, 0, 1, 1, 0, 0, 0, 0,
                              0, 1, 1, 1, 1, 0, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 1, 1, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              1, 1, 0, 0, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0],
                             list(text.bits),
                             'Text mismatch.')

    def test_render(self):
        self.lp.grid.render(Text('Apple'))
        self.lp.grid.render(Text('Apple').scroll(count=1, period=.0001))


class TestTextWhiteBox(unittest.TestCase):
    def test_shift_left_carry(self):
        text = Text('A').shift(-1)
        self.assertEqual(text._string.character_to_render.carry,
                         0b01111100, 'Carry mismatch.')

    def test_shift_right_carry(self):
        text = Text('A').shift(3)
        self.assertEqual(text._string.character_to_render.carry,
                         0b00111110, 'Carry mismatch.')


if __name__ == '__main__':
    unittest.main()
