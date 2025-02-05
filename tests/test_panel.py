import unittest
from lpminimk3.__init__ import (ButtonFace,
                                Panel,
                                ButtonEvent)
from lpminimk3.colors._colors import (ColorPalette,
                                      ColorShadeStore)
from lpminimk3.colors.web_color import WebColor
from lpminimk3.region import Labeled
from tests._vlpminimk3 import (VirtualMidiEvent,
                               create_virtual_launchpad)


class TestPanel(unittest.TestCase):
    def setUp(self):
        self.lp = create_virtual_launchpad()

    def tearDown(self):
        self.lp.close()

    def test_launchpad(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.launchpad,
                         self.lp,
                         'Launchpad mismatch.')

    def test_max_x(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.max_x,
                         8,
                         'Max X mismatch.')

    def test_max_y(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.max_y,
                         8,
                         'Max Y mismatch.')

    def test_width(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.width,
                         9,
                         'Width mismatch.')

    def test_height(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.height,
                         9,
                         'Height mismatch.')

    def test_eq(self):
        self.lp.open()

        another_lp = create_virtual_launchpad(client_id=99)
        another_lp.open()

        self.assertTrue(self.lp.panel == self.lp.panel,
                        'Panel mismatch.')
        self.assertTrue(self.lp.panel != another_lp.panel,
                        'Panel mismatch.')


class TestLed(unittest.TestCase):
    def setUp(self):
        self.lp = create_virtual_launchpad()

    def tearDown(self):
        self.lp.close()

    def test_panel_led(self):
        self.lp.open()

        another_lp = create_virtual_launchpad(client_id=99)
        another_lp.open()

        self.assertTrue(self.lp.panel.led(0, 0) == self.lp.panel.led(0, 0),
                        'LED mismatch.')
        self.assertTrue(self.lp.panel.led(0, 0) != another_lp.panel.led(0, 0),
                        'LED mismatch.')

        self.assertTrue(self.lp.panel.led(0, 0, layout=Panel.CUSTOM) == self.lp.panel.led(0, 0),  # noqa
                        'LED mismatch.')
        self.assertTrue(self.lp.panel.led(0, 0) != another_lp.panel.led(0, 0, layout=Panel.CUSTOM),  # noqa
                        'LED mismatch.')

    def test_panel_grid_led(self):
        self.lp.open()

        another_lp = create_virtual_launchpad(client_id=99)
        another_lp.open()

        self.assertTrue(self.lp.panel.led(0, 1) == self.lp.grid.led(0, 0),
                        'LED mismatch.')
        self.assertTrue(self.lp.panel.led(0, 1) != another_lp.grid.led(0, 0),
                        'LED mismatch.')
        self.assertTrue(self.lp.panel.led(0, 1) == self.lp.grid.led(0, 0, layout=Panel.CUSTOM),  # noqa
                        'LED mismatch.')
        self.assertTrue(self.lp.panel.led(0, 1) != another_lp.grid.led(0, 0, layout=Panel.CUSTOM),  # noqa
                        'LED mismatch.')

    def test_set_by_index(self):
        self.lp.open()
        for color_index in range(128):
            self.lp.panel.led('up').color = color_index

        with self.assertRaises(ValueError):
            self.lp.panel.led('up').color = -1
        with self.assertRaises(ValueError):
            self.lp.panel.led('up').color = 128

    def test_set_by_led_range(self):
        self.lp.open()
        for led in self.lp.panel.led_range():
            for color_index in range(128):
                led.color = color_index

    def test_set_by_shade(self):
        self.lp.open()

        self.assertEqual(len(ColorShadeStore.COLOR_GROUPS),
                         len(ColorShadeStore.COLOR_GROUP_SYMBOLS),
                         'Color group to color group symbol mismatch.')

        self.lp.panel.led('up').color = ColorPalette.Red.SHADE_1
        self.lp.panel.led('up').color = ColorPalette.Orange.SHADE_1
        self.lp.panel.led('up').color = ColorPalette.Yellow.SHADE_1
        self.lp.panel.led('up').color = ColorPalette.Green.SHADE_1
        self.lp.panel.led('up').color = ColorPalette.Blue.SHADE_1
        self.lp.panel.led('up').color = ColorPalette.Violet.SHADE_1
        self.lp.panel.led('up').color = ColorPalette.White.SHADE_1
        self.lp.panel.led('up').color = 'r'
        self.lp.panel.led('up').color = 'o'
        self.lp.panel.led('up').color = 'y'
        self.lp.panel.led('up').color = 'g'
        self.lp.panel.led('up').color = 'b'
        self.lp.panel.led('up').color = 'v'
        self.lp.panel.led('up').color = 'w'
        self.lp.panel.led('up').color = 'r1'
        self.lp.panel.led('up').color = 'o1'
        self.lp.panel.led('up').color = 'y1'
        self.lp.panel.led('up').color = 'g1'
        self.lp.panel.led('up').color = 'b1'
        self.lp.panel.led('up').color = 'v1'
        self.lp.panel.led('up').color = 'w1'
        self.lp.panel.led('up').color = 'red'
        self.lp.panel.led('up').color = 'orange'
        self.lp.panel.led('up').color = 'yellow'
        self.lp.panel.led('up').color = 'green'
        self.lp.panel.led('up').color = 'blue'
        self.lp.panel.led('up').color = 'violet'
        self.lp.panel.led('up').color = 'white'
        self.lp.panel.led('up').color = 'red1'
        self.lp.panel.led('up').color = 'orange1'
        self.lp.panel.led('up').color = 'yellow1'
        self.lp.panel.led('up').color = 'green1'
        self.lp.panel.led('up').color = 'blue1'
        self.lp.panel.led('up').color = 'violet1'
        self.lp.panel.led('up').color = 'red0'
        self.lp.panel.led('up').color = 'orange0'
        self.lp.panel.led('up').color = 'yellow0'
        self.lp.panel.led('up').color = 'green0'
        self.lp.panel.led('up').color = 'blue0'
        self.lp.panel.led('up').color = 'violet0'
        self.lp.panel.led('up').color = 'white0'
        self.lp.panel.led('up').color = '#fff'
        self.lp.panel.led('up').color = '#ff0000'
        self.lp.panel.led('up').color = (0, 0, 255)
        self.lp.grid.led('0x0').color = WebColor("amethyst")

        with self.assertRaises(ValueError):
            self.lp.panel.led('up').color = '1r'
        with self.assertRaises(ValueError):
            self.lp.panel.led('up').color = 're'
        with self.assertRaises(ValueError):
            self.lp.panel.led('up').color = 'gree3'
        with self.assertRaises(ValueError):
            self.lp.panel.led('up').color = (0, 0)
        with self.assertRaises(ValueError):
            self.lp.grid.led('0x0').color = (-1, 0, -1)
        with self.assertRaises(ValueError):
            self.lp.grid.led('0x0').color = (257, 277, 99)
        with self.assertRaises(ValueError):
            self.lp.grid.led('0x0').color = '#ga1'
        with self.assertRaises(ValueError):
            self.lp.panel.led('up').color = 'blue-0'
        with self.assertRaises(ValueError):
            self.lp.panel.led('up').color = 'yellow-1'

    def test_reset(self):
        self.lp.open()
        self.lp.panel.led('up').color = 1
        self.lp.panel.led('up').reset()

    def test_led_range(self):
        self.lp.open()
        for led in self.lp.panel.led_range():
            for color_index in range(128):
                led.color = color_index

    def test_led_range_labeled_region(self):
        self.lp.open()
        for led in self.lp.panel.led_range(region=Labeled()):
            for color_index in range(128):
                led.color = color_index

    def test_labeled_region_button_names(self):
        self.assertCountEqual(['up',
                               'down',
                               'left',
                               'right',
                               'session',
                               'drums',
                               'keys',
                               'user',
                               'logo',
                               'scene_launch_1',
                               'scene_launch_2',
                               'scene_launch_3',
                               'scene_launch_4',
                               'scene_launch_5',
                               'scene_launch_6',
                               'scene_launch_7',
                               'stop_solo_mute'],
                              Labeled().button_names,
                              'Button name mismatch.')

    def test_id_by_xy(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.led(0, 0).id, 1, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 0).id, 2, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 0).id, 3, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 0).id, 4, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 0).id, 5, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 0).id, 6, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 0).id, 7, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 0).id, 8, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 0).id, 9, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 1).id, 10, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 1).id, 11, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 1).id, 12, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 1).id, 13, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 1).id, 14, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 1).id, 15, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 1).id, 16, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 1).id, 17, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 1).id, 18, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 2).id, 19, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 2).id, 20, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 2).id, 21, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 2).id, 22, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 2).id, 23, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 2).id, 24, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 2).id, 25, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 2).id, 26, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 2).id, 27, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 3).id, 28, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 3).id, 29, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 3).id, 30, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 3).id, 31, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 3).id, 32, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 3).id, 33, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 3).id, 34, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 3).id, 35, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 3).id, 36, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 4).id, 37, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 4).id, 38, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 4).id, 39, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 4).id, 40, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 4).id, 41, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 4).id, 42, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 4).id, 43, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 4).id, 44, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 4).id, 45, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 5).id, 46, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 5).id, 47, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 5).id, 48, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 5).id, 49, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 5).id, 50, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 5).id, 51, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 5).id, 52, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 5).id, 53, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 5).id, 54, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 6).id, 55, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 6).id, 56, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 6).id, 57, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 6).id, 58, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 6).id, 59, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 6).id, 60, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 6).id, 61, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 6).id, 62, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 6).id, 63, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 7).id, 64, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 7).id, 65, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 7).id, 66, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 7).id, 67, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 7).id, 68, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 7).id, 69, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 7).id, 70, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 7).id, 71, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 7).id, 72, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 8).id, 73, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 8).id, 74, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 8).id, 75, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 8).id, 76, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 8).id, 77, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 8).id, 78, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 8).id, 79, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 8).id, 80, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 8).id, 81, 'ID mismatch.')  # noqa

    def test_x_by_xy(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.led(0, 0).x, 0, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 0).x, 1, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 0).x, 2, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 0).x, 3, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 0).x, 4, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 0).x, 5, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 0).x, 6, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 0).x, 7, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 0).x, 8, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 1).x, 0, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 1).x, 1, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 1).x, 2, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 1).x, 3, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 1).x, 4, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 1).x, 5, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 1).x, 6, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 1).x, 7, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 1).x, 8, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 2).x, 0, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 2).x, 1, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 2).x, 2, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 2).x, 3, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 2).x, 4, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 2).x, 5, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 2).x, 6, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 2).x, 7, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 2).x, 8, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 3).x, 0, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 3).x, 1, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 3).x, 2, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 3).x, 3, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 3).x, 4, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 3).x, 5, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 3).x, 6, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 3).x, 7, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 3).x, 8, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 4).x, 0, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 4).x, 1, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 4).x, 2, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 4).x, 3, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 4).x, 4, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 4).x, 5, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 4).x, 6, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 4).x, 7, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 4).x, 8, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 5).x, 0, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 5).x, 1, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 5).x, 2, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 5).x, 3, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 5).x, 4, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 5).x, 5, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 5).x, 6, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 5).x, 7, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 5).x, 8, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 6).x, 0, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 6).x, 1, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 6).x, 2, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 6).x, 3, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 6).x, 4, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 6).x, 5, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 6).x, 6, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 6).x, 7, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 6).x, 8, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 7).x, 0, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 7).x, 1, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 7).x, 2, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 7).x, 3, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 7).x, 4, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 7).x, 5, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 7).x, 6, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 7).x, 7, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 7).x, 8, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 8).x, 0, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 8).x, 1, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 8).x, 2, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 8).x, 3, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 8).x, 4, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 8).x, 5, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 8).x, 6, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 8).x, 7, 'X mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 8).x, 8, 'X mismatch.')  # noqa

    def test_y_by_xy(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.led(0, 0).y, 0, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 0).y, 0, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 0).y, 0, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 0).y, 0, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 0).y, 0, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 0).y, 0, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 0).y, 0, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 0).y, 0, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 0).y, 0, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 1).y, 1, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 1).y, 1, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 1).y, 1, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 1).y, 1, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 1).y, 1, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 1).y, 1, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 1).y, 1, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 1).y, 1, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 1).y, 1, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 2).y, 2, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 2).y, 2, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 2).y, 2, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 2).y, 2, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 2).y, 2, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 2).y, 2, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 2).y, 2, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 2).y, 2, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 2).y, 2, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 3).y, 3, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 3).y, 3, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 3).y, 3, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 3).y, 3, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 3).y, 3, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 3).y, 3, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 3).y, 3, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 3).y, 3, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 3).y, 3, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 4).y, 4, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 4).y, 4, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 4).y, 4, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 4).y, 4, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 4).y, 4, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 4).y, 4, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 4).y, 4, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 4).y, 4, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 4).y, 4, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 5).y, 5, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 5).y, 5, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 5).y, 5, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 5).y, 5, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 5).y, 5, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 5).y, 5, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 5).y, 5, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 5).y, 5, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 5).y, 5, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 6).y, 6, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 6).y, 6, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 6).y, 6, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 6).y, 6, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 6).y, 6, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 6).y, 6, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 6).y, 6, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 6).y, 6, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 6).y, 6, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 7).y, 7, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 7).y, 7, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 7).y, 7, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 7).y, 7, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 7).y, 7, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 7).y, 7, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 7).y, 7, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 7).y, 7, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 7).y, 7, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 8).y, 8, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 8).y, 8, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 8).y, 8, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 8).y, 8, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 8).y, 8, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 8).y, 8, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 8).y, 8, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 8).y, 8, 'Y mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 8).y, 8, 'Y mismatch.')  # noqa

    def test_name_by_button_face(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.led(0, 0).name, ButtonFace.UP, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 0).name, ButtonFace.DOWN, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 0).name, ButtonFace.LEFT, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 0).name, ButtonFace.RIGHT, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 0).name, ButtonFace.SESSION, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 0).name, ButtonFace.DRUMS, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 0).name, ButtonFace.KEYS, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 0).name, ButtonFace.USER, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 0).name, ButtonFace.LOGO, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 1).name, '0x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 1).name, '1x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 1).name, '2x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 1).name, '3x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 1).name, '4x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 1).name, '5x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 1).name, '6x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 1).name, '7x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 1).name, ButtonFace.SCENE_LAUNCH_1, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 2).name, '0x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 2).name, '1x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 2).name, '2x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 2).name, '3x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 2).name, '4x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 2).name, '5x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 2).name, '6x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 2).name, '7x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 2).name, ButtonFace.SCENE_LAUNCH_2, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 3).name, '0x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 3).name, '1x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 3).name, '2x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 3).name, '3x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 3).name, '4x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 3).name, '5x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 3).name, '6x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 3).name, '7x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 3).name, ButtonFace.SCENE_LAUNCH_3, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 4).name, '0x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 4).name, '1x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 4).name, '2x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 4).name, '3x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 4).name, '4x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 4).name, '5x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 4).name, '6x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 4).name, '7x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 4).name, ButtonFace.SCENE_LAUNCH_4, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 5).name, '0x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 5).name, '1x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 5).name, '2x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 5).name, '3x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 5).name, '4x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 5).name, '5x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 5).name, '6x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 5).name, '7x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 5).name, ButtonFace.SCENE_LAUNCH_5, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 6).name, '0x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 6).name, '1x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 6).name, '2x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 6).name, '3x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 6).name, '4x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 6).name, '5x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 6).name, '6x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 6).name, '7x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 6).name, ButtonFace.SCENE_LAUNCH_6, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 7).name, '0x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 7).name, '1x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 7).name, '2x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 7).name, '3x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 7).name, '4x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 7).name, '5x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 7).name, '6x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 7).name, '7x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 7).name, ButtonFace.SCENE_LAUNCH_7, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 8).name, '0x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 8).name, '1x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 8).name, '2x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 8).name, '3x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 8).name, '4x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 8).name, '5x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 8).name, '6x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 8).name, '7x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 8).name, ButtonFace.STOP_SOLO_MUTE, 'Name mismatch.')  # noqa

    def test_color_by_xy(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.led(0, 0).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 0).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 0).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 0).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 0).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 0).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 0).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 0).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 0).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 1).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 1).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 1).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 1).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 1).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 1).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 1).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 1).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 1).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 2).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 2).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 2).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 2).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 2).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 2).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 2).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 2).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 2).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 3).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 3).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 3).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 3).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 3).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 3).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 3).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 3).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 3).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 4).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 4).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 4).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 4).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 4).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 4).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 4).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 4).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 4).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 5).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 5).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 5).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 5).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 5).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 5).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 5).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 5).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 5).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 6).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 6).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 6).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 6).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 6).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 6).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 6).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 6).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 6).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 7).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 7).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 7).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 7).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 7).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 7).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 7).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 7).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 7).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 8).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 8).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 8).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 8).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 8).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 8).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 8).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 8).color, None, 'Color mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 8).color, None, 'Color mismatch.')  # noqa

    def test_id_by_button_name(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.led('up').id, 1, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('down').id, 2, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('left').id, 3, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('right').id, 4, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('session').id, 5, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('drums').id, 6, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('keys').id, 7, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('user').id, 8, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('logo').id, 9, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('0x0').id, 10, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('1x0').id, 11, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('2x0').id, 12, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('3x0').id, 13, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('4x0').id, 14, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('5x0').id, 15, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('6x0').id, 16, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('7x0').id, 17, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('scene_launch_1').id, 18, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('0x1').id, 19, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('1x1').id, 20, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('2x1').id, 21, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('3x1').id, 22, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('4x1').id, 23, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('5x1').id, 24, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('6x1').id, 25, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('7x1').id, 26, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('scene_launch_2').id, 27, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('0x2').id, 28, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('1x2').id, 29, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('2x2').id, 30, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('3x2').id, 31, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('4x2').id, 32, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('5x2').id, 33, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('6x2').id, 34, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('7x2').id, 35, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('scene_launch_3').id, 36, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('0x3').id, 37, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('1x3').id, 38, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('2x3').id, 39, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('3x3').id, 40, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('4x3').id, 41, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('5x3').id, 42, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('6x3').id, 43, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('7x3').id, 44, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('scene_launch_4').id, 45, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('0x4').id, 46, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('1x4').id, 47, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('2x4').id, 48, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('3x4').id, 49, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('4x4').id, 50, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('5x4').id, 51, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('6x4').id, 52, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('7x4').id, 53, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('scene_launch_5').id, 54, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('0x5').id, 55, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('1x5').id, 56, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('2x5').id, 57, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('3x5').id, 58, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('4x5').id, 59, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('5x5').id, 60, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('6x5').id, 61, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('7x5').id, 62, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('scene_launch_6').id, 63, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('0x6').id, 64, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('1x6').id, 65, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('2x6').id, 66, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('3x6').id, 67, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('4x6').id, 68, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('5x6').id, 69, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('6x6').id, 70, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('7x6').id, 71, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('scene_launch_7').id, 72, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('0x7').id, 73, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('1x7').id, 74, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('2x7').id, 75, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('3x7').id, 76, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('4x7').id, 77, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('5x7').id, 78, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('6x7').id, 79, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('7x7').id, 80, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('stop_solo_mute').id, 81, 'ID mismatch.')  # noqa

        self.assertEqual(self.lp.panel.led('stop').id, 81, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('solo').id, 81, 'ID mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led('mute').id, 81, 'ID mismatch.')  # noqa

        with self.assertRaises(ValueError):
            self.lp.panel.led('')
        with self.assertRaises(ValueError):
            self.lp.panel.led('s')

    def test_name_by_id(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.led(0).name, ButtonFace.UP, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1).name, ButtonFace.DOWN, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2).name, ButtonFace.LEFT, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3).name, ButtonFace.RIGHT, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4).name, ButtonFace.SESSION, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5).name, ButtonFace.DRUMS, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6).name, ButtonFace.KEYS, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7).name, ButtonFace.USER, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8).name, ButtonFace.LOGO, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(9).name, '0x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(10).name, '1x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(11).name, '2x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(12).name, '3x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(13).name, '4x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(14).name, '5x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(15).name, '6x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(16).name, '7x0', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(17).name, ButtonFace.SCENE_LAUNCH_1, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(18).name, '0x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(19).name, '1x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(20).name, '2x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(21).name, '3x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(22).name, '4x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(23).name, '5x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(24).name, '6x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(25).name, '7x1', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(26).name, ButtonFace.SCENE_LAUNCH_2, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(27).name, '0x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(28).name, '1x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(29).name, '2x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(30).name, '3x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(31).name, '4x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(32).name, '5x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(33).name, '6x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(34).name, '7x2', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(35).name, ButtonFace.SCENE_LAUNCH_3, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(36).name, '0x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(37).name, '1x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(38).name, '2x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(39).name, '3x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(40).name, '4x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(41).name, '5x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(42).name, '6x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(43).name, '7x3', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(44).name, ButtonFace.SCENE_LAUNCH_4, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(45).name, '0x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(46).name, '1x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(47).name, '2x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(48).name, '3x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(49).name, '4x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(50).name, '5x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(51).name, '6x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(52).name, '7x4', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(53).name, ButtonFace.SCENE_LAUNCH_5, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(54).name, '0x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(55).name, '1x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(56).name, '2x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(57).name, '3x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(58).name, '4x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(59).name, '5x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(60).name, '6x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(61).name, '7x5', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(62).name, ButtonFace.SCENE_LAUNCH_6, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(63).name, '0x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(64).name, '1x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(65).name, '2x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(66).name, '3x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(67).name, '4x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(68).name, '5x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(69).name, '6x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(70).name, '7x6', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(71).name, ButtonFace.SCENE_LAUNCH_7, 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(72).name, '0x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(73).name, '1x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(74).name, '2x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(75).name, '3x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(76).name, '4x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(77).name, '5x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(78).name, '6x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(79).name, '7x7', 'Name mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(80).name, ButtonFace.STOP_SOLO_MUTE, 'Name mismatch.')  # noqa

    def test_midi_value_prog_layout(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.led(0, 0).midi_value, 0x5b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 0).midi_value, 0x5c, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 0).midi_value, 0x5d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 0).midi_value, 0x5e, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 0).midi_value, 0x5f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 0).midi_value, 0x60, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 0).midi_value, 0x61, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 0).midi_value, 0x62, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 0).midi_value, 0x63, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 1).midi_value, 0x51, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 1).midi_value, 0x52, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 1).midi_value, 0x53, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 1).midi_value, 0x54, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 1).midi_value, 0x55, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 1).midi_value, 0x56, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 1).midi_value, 0x57, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 1).midi_value, 0x58, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 1).midi_value, 0x59, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 2).midi_value, 0x47, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 2).midi_value, 0x48, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 2).midi_value, 0x49, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 2).midi_value, 0x4a, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 2).midi_value, 0x4b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 2).midi_value, 0x4c, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 2).midi_value, 0x4d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 2).midi_value, 0x4e, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 2).midi_value, 0x4f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 3).midi_value, 0x3d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 3).midi_value, 0x3e, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 3).midi_value, 0x3f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 3).midi_value, 0x40, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 3).midi_value, 0x41, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 3).midi_value, 0x42, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 3).midi_value, 0x43, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 3).midi_value, 0x44, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 3).midi_value, 0x45, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 4).midi_value, 0x33, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 4).midi_value, 0x34, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 4).midi_value, 0x35, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 4).midi_value, 0x36, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 4).midi_value, 0x37, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 4).midi_value, 0x38, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 4).midi_value, 0x39, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 4).midi_value, 0x3a, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 4).midi_value, 0x3b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 5).midi_value, 0x29, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 5).midi_value, 0x2a, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 5).midi_value, 0x2b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 5).midi_value, 0x2c, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 5).midi_value, 0x2d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 5).midi_value, 0x2e, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 5).midi_value, 0x2f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 5).midi_value, 0x30, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 5).midi_value, 0x31, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 6).midi_value, 0x1f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 6).midi_value, 0x20, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 6).midi_value, 0x21, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 6).midi_value, 0x22, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 6).midi_value, 0x23, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 6).midi_value, 0x24, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 6).midi_value, 0x25, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 6).midi_value, 0x26, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 6).midi_value, 0x27, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 7).midi_value, 0x15, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 7).midi_value, 0x16, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 7).midi_value, 0x17, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 7).midi_value, 0x18, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 7).midi_value, 0x19, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 7).midi_value, 0x1a, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 7).midi_value, 0x1b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 7).midi_value, 0x1c, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 7).midi_value, 0x1d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 8).midi_value, 0x0b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 8).midi_value, 0x0c, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 8).midi_value, 0x0d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 8).midi_value, 0x0e, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 8).midi_value, 0x0f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 8).midi_value, 0x10, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 8).midi_value, 0x11, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 8).midi_value, 0x12, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 8).midi_value, 0x13, 'MIDI value mismatch.')  # noqa

    def test_midi_value_custom_layout(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.led(0, 0, layout=Panel.CUSTOM).midi_value, 0x5b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 0, layout=Panel.CUSTOM).midi_value, 0x5c, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 0, layout=Panel.CUSTOM).midi_value, 0x5d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 0, layout=Panel.CUSTOM).midi_value, 0x5e, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 0, layout=Panel.CUSTOM).midi_value, 0x5f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 0, layout=Panel.CUSTOM).midi_value, 0x60, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 0, layout=Panel.CUSTOM).midi_value, 0x61, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 0, layout=Panel.CUSTOM).midi_value, 0x62, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 0, layout=Panel.CUSTOM).midi_value, 0x63, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 1, layout=Panel.CUSTOM).midi_value, 0x40, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 1, layout=Panel.CUSTOM).midi_value, 0x41, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 1, layout=Panel.CUSTOM).midi_value, 0x42, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 1, layout=Panel.CUSTOM).midi_value, 0x43, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 1, layout=Panel.CUSTOM).midi_value, 0x60, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 1, layout=Panel.CUSTOM).midi_value, 0x61, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 1, layout=Panel.CUSTOM).midi_value, 0x62, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 1, layout=Panel.CUSTOM).midi_value, 0x63, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 1, layout=Panel.CUSTOM).midi_value, 0x59, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 2, layout=Panel.CUSTOM).midi_value, 0x3c, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 2, layout=Panel.CUSTOM).midi_value, 0x3d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 2, layout=Panel.CUSTOM).midi_value, 0x3e, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 2, layout=Panel.CUSTOM).midi_value, 0x3f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 2, layout=Panel.CUSTOM).midi_value, 0x5c, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 2, layout=Panel.CUSTOM).midi_value, 0x5d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 2, layout=Panel.CUSTOM).midi_value, 0x5e, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 2, layout=Panel.CUSTOM).midi_value, 0x5f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 2, layout=Panel.CUSTOM).midi_value, 0x4f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 3, layout=Panel.CUSTOM).midi_value, 0x38, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 3, layout=Panel.CUSTOM).midi_value, 0x39, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 3, layout=Panel.CUSTOM).midi_value, 0x3a, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 3, layout=Panel.CUSTOM).midi_value, 0x3b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 3, layout=Panel.CUSTOM).midi_value, 0x58, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 3, layout=Panel.CUSTOM).midi_value, 0x59, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 3, layout=Panel.CUSTOM).midi_value, 0x5a, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 3, layout=Panel.CUSTOM).midi_value, 0x5b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 3, layout=Panel.CUSTOM).midi_value, 0x45, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 4, layout=Panel.CUSTOM).midi_value, 0x34, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 4, layout=Panel.CUSTOM).midi_value, 0x35, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 4, layout=Panel.CUSTOM).midi_value, 0x36, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 4, layout=Panel.CUSTOM).midi_value, 0x37, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 4, layout=Panel.CUSTOM).midi_value, 0x54, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 4, layout=Panel.CUSTOM).midi_value, 0x55, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 4, layout=Panel.CUSTOM).midi_value, 0x56, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 4, layout=Panel.CUSTOM).midi_value, 0x57, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 4, layout=Panel.CUSTOM).midi_value, 0x3b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 5, layout=Panel.CUSTOM).midi_value, 0x30, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 5, layout=Panel.CUSTOM).midi_value, 0x31, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 5, layout=Panel.CUSTOM).midi_value, 0x32, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 5, layout=Panel.CUSTOM).midi_value, 0x33, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 5, layout=Panel.CUSTOM).midi_value, 0x50, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 5, layout=Panel.CUSTOM).midi_value, 0x51, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 5, layout=Panel.CUSTOM).midi_value, 0x52, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 5, layout=Panel.CUSTOM).midi_value, 0x53, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 5, layout=Panel.CUSTOM).midi_value, 0x31, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 6, layout=Panel.CUSTOM).midi_value, 0x2c, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 6, layout=Panel.CUSTOM).midi_value, 0x2d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 6, layout=Panel.CUSTOM).midi_value, 0x2e, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 6, layout=Panel.CUSTOM).midi_value, 0x2f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 6, layout=Panel.CUSTOM).midi_value, 0x4c, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 6, layout=Panel.CUSTOM).midi_value, 0x4d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 6, layout=Panel.CUSTOM).midi_value, 0x4e, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 6, layout=Panel.CUSTOM).midi_value, 0x4f, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 6, layout=Panel.CUSTOM).midi_value, 0x27, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 7, layout=Panel.CUSTOM).midi_value, 0x28, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 7, layout=Panel.CUSTOM).midi_value, 0x29, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 7, layout=Panel.CUSTOM).midi_value, 0x2a, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 7, layout=Panel.CUSTOM).midi_value, 0x2b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 7, layout=Panel.CUSTOM).midi_value, 0x48, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 7, layout=Panel.CUSTOM).midi_value, 0x49, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 7, layout=Panel.CUSTOM).midi_value, 0x4a, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 7, layout=Panel.CUSTOM).midi_value, 0x4b, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 7, layout=Panel.CUSTOM).midi_value, 0x1d, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(0, 8, layout=Panel.CUSTOM).midi_value, 0x24, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(1, 8, layout=Panel.CUSTOM).midi_value, 0x25, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(2, 8, layout=Panel.CUSTOM).midi_value, 0x26, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(3, 8, layout=Panel.CUSTOM).midi_value, 0x27, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(4, 8, layout=Panel.CUSTOM).midi_value, 0x44, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(5, 8, layout=Panel.CUSTOM).midi_value, 0x45, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(6, 8, layout=Panel.CUSTOM).midi_value, 0x46, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(7, 8, layout=Panel.CUSTOM).midi_value, 0x47, 'MIDI value mismatch.')  # noqa
        self.assertEqual(self.lp.panel.led(8, 8, layout=Panel.CUSTOM).midi_value, 0x13, 'MIDI value mismatch.')  # noqa


class TestButtonGroup(unittest.TestCase):
    def setUp(self):
        self.lp = create_virtual_launchpad()

    def tearDown(self):
        self.lp.close()

    def test_names_by_name(self):
        self.lp.open()
        self.assertCountEqual(['up'],
                              self.lp.panel.buttons('up').names,
                              'Button name mismatch.')
        self.assertCountEqual(['down'],
                              self.lp.panel.buttons('down').names,
                              'Button name mismatch.')
        self.assertCountEqual(['left'],
                              self.lp.panel.buttons('left').names,
                              'Button name mismatch.')
        self.assertCountEqual(['right'],
                              self.lp.panel.buttons('right').names,
                              'Button name mismatch.')
        self.assertCountEqual(['session'],
                              self.lp.panel.buttons('session').names,
                              'Button name mismatch.')
        self.assertCountEqual(['drums'],
                              self.lp.panel.buttons('drums').names,
                              'Button name mismatch.')
        self.assertCountEqual(['keys'],
                              self.lp.panel.buttons('keys').names,
                              'Button name mismatch.')
        self.assertCountEqual(['user'],
                              self.lp.panel.buttons('user').names,
                              'Button name mismatch.')
        self.assertCountEqual(['logo'],
                              self.lp.panel.buttons('logo').names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x0'],
                              self.lp.panel.buttons('0x0').names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x0'],
                              self.lp.panel.buttons('1x0').names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x0'],
                              self.lp.panel.buttons('2x0').names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x0'],
                              self.lp.panel.buttons('3x0').names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x0'],
                              self.lp.panel.buttons('4x0').names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x0'],
                              self.lp.panel.buttons('5x0').names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x0'],
                              self.lp.panel.buttons('6x0').names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x0'],
                              self.lp.panel.buttons('7x0').names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_1'],
                              self.lp.panel.buttons('scene_launch_1').names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x1'],
                              self.lp.panel.buttons('0x1').names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x1'],
                              self.lp.panel.buttons('1x1').names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x1'],
                              self.lp.panel.buttons('2x1').names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x1'],
                              self.lp.panel.buttons('3x1').names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x1'],
                              self.lp.panel.buttons('4x1').names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x1'],
                              self.lp.panel.buttons('5x1').names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x1'],
                              self.lp.panel.buttons('6x1').names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x1'],
                              self.lp.panel.buttons('7x1').names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_2'],
                              self.lp.panel.buttons('scene_launch_2').names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x2'],
                              self.lp.panel.buttons('0x2').names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x2'],
                              self.lp.panel.buttons('1x2').names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x2'],
                              self.lp.panel.buttons('2x2').names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x2'],
                              self.lp.panel.buttons('3x2').names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x2'],
                              self.lp.panel.buttons('4x2').names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x2'],
                              self.lp.panel.buttons('5x2').names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x2'],
                              self.lp.panel.buttons('6x2').names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x2'],
                              self.lp.panel.buttons('7x2').names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_3'],
                              self.lp.panel.buttons('scene_launch_3').names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x3'],
                              self.lp.panel.buttons('0x3').names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x3'],
                              self.lp.panel.buttons('1x3').names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x3'],
                              self.lp.panel.buttons('2x3').names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x3'],
                              self.lp.panel.buttons('3x3').names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x3'],
                              self.lp.panel.buttons('4x3').names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x3'],
                              self.lp.panel.buttons('5x3').names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x3'],
                              self.lp.panel.buttons('6x3').names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x3'],
                              self.lp.panel.buttons('7x3').names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_4'],
                              self.lp.panel.buttons('scene_launch_4').names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x4'],
                              self.lp.panel.buttons('0x4').names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x4'],
                              self.lp.panel.buttons('1x4').names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x4'],
                              self.lp.panel.buttons('2x4').names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x4'],
                              self.lp.panel.buttons('3x4').names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x4'],
                              self.lp.panel.buttons('4x4').names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x4'],
                              self.lp.panel.buttons('5x4').names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x4'],
                              self.lp.panel.buttons('6x4').names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x4'],
                              self.lp.panel.buttons('7x4').names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_5'],
                              self.lp.panel.buttons('scene_launch_5').names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x5'],
                              self.lp.panel.buttons('0x5').names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x5'],
                              self.lp.panel.buttons('1x5').names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x5'],
                              self.lp.panel.buttons('2x5').names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x5'],
                              self.lp.panel.buttons('3x5').names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x5'],
                              self.lp.panel.buttons('4x5').names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x5'],
                              self.lp.panel.buttons('5x5').names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x5'],
                              self.lp.panel.buttons('6x5').names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x5'],
                              self.lp.panel.buttons('7x5').names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_6'],
                              self.lp.panel.buttons('scene_launch_6').names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x6'],
                              self.lp.panel.buttons('0x6').names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x6'],
                              self.lp.panel.buttons('1x6').names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x6'],
                              self.lp.panel.buttons('2x6').names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x6'],
                              self.lp.panel.buttons('3x6').names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x6'],
                              self.lp.panel.buttons('4x6').names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x6'],
                              self.lp.panel.buttons('5x6').names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x6'],
                              self.lp.panel.buttons('6x6').names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x6'],
                              self.lp.panel.buttons('7x6').names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_7'],
                              self.lp.panel.buttons('scene_launch_7').names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x7'],
                              self.lp.panel.buttons('0x7').names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x7'],
                              self.lp.panel.buttons('1x7').names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x7'],
                              self.lp.panel.buttons('2x7').names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x7'],
                              self.lp.panel.buttons('3x7').names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x7'],
                              self.lp.panel.buttons('4x7').names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x7'],
                              self.lp.panel.buttons('5x7').names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x7'],
                              self.lp.panel.buttons('6x7').names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x7'],
                              self.lp.panel.buttons('7x7').names,
                              'Button name mismatch.')
        self.assertCountEqual(['stop_solo_mute'],
                              self.lp.panel.buttons('stop_solo_mute').names,
                              'Button name mismatch.')

        self.assertCountEqual(['up', '7x7', 'stop_solo_mute'],
                              self.lp.panel.buttons('up', '7x7', 'stop_solo_mute').names,  # noqa
                              'Button name mismatch.')
        self.assertCountEqual(['up'],
                              self.lp.panel.buttons('up', 'up', 'up').names,  # noqa
                              'Button name mismatch.')

        self.assertCountEqual(['up', 'down', 'left', 'right', 'session', 'drums', 'keys', 'user', 'logo',  # noqa
                               '0x0', '1x0', '2x0', '3x0', '4x0', '5x0', '6x0', '7x0', 'scene_launch_1',  # noqa
                               '0x1', '1x1', '2x1', '3x1', '4x1', '5x1', '6x1', '7x1', 'scene_launch_2',  # noqa
                               '0x2', '1x2', '2x2', '3x2', '4x2', '5x2', '6x2', '7x2', 'scene_launch_3',  # noqa
                               '0x3', '1x3', '2x3', '3x3', '4x3', '5x3', '6x3', '7x3', 'scene_launch_4',  # noqa
                               '0x4', '1x4', '2x4', '3x4', '4x4', '5x4', '6x4', '7x4', 'scene_launch_5',  # noqa
                               '0x5', '1x5', '2x5', '3x5', '4x5', '5x5', '6x5', '7x5', 'scene_launch_6',  # noqa
                               '0x6', '1x6', '2x6', '3x6', '4x6', '5x6', '6x6', '7x6', 'scene_launch_7',  # noqa
                               '0x7', '1x7', '2x7', '3x7', '4x7', '5x7', '6x7', '7x7', 'stop_solo_mute'],  # noqa
                              self.lp.panel.buttons().names,
                              'Button name mismatch.')

        with self.assertRaises(ValueError):
            self.lp.panel.buttons(None).names
        with self.assertRaises(ValueError):
            self.lp.panel.buttons('').names

    def test_names_by_id(self):
        self.lp.open()
        self.assertCountEqual(['up'],
                              self.lp.panel.buttons(0).names,
                              'Button name mismatch.')
        self.assertCountEqual(['down'],
                              self.lp.panel.buttons(1).names,
                              'Button name mismatch.')
        self.assertCountEqual(['left'],
                              self.lp.panel.buttons(2).names,
                              'Button name mismatch.')
        self.assertCountEqual(['right'],
                              self.lp.panel.buttons(3).names,
                              'Button name mismatch.')
        self.assertCountEqual(['session'],
                              self.lp.panel.buttons(4).names,
                              'Button name mismatch.')
        self.assertCountEqual(['drums'],
                              self.lp.panel.buttons(5).names,
                              'Button name mismatch.')
        self.assertCountEqual(['keys'],
                              self.lp.panel.buttons(6).names,
                              'Button name mismatch.')
        self.assertCountEqual(['user'],
                              self.lp.panel.buttons(7).names,
                              'Button name mismatch.')
        self.assertCountEqual(['logo'],
                              self.lp.panel.buttons(8).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x0'],
                              self.lp.panel.buttons(9).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x0'],
                              self.lp.panel.buttons(10).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x0'],
                              self.lp.panel.buttons(11).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x0'],
                              self.lp.panel.buttons(12).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x0'],
                              self.lp.panel.buttons(13).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x0'],
                              self.lp.panel.buttons(14).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x0'],
                              self.lp.panel.buttons(15).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x0'],
                              self.lp.panel.buttons(16).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_1'],
                              self.lp.panel.buttons(17).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x1'],
                              self.lp.panel.buttons(18).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x1'],
                              self.lp.panel.buttons(19).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x1'],
                              self.lp.panel.buttons(20).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x1'],
                              self.lp.panel.buttons(21).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x1'],
                              self.lp.panel.buttons(22).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x1'],
                              self.lp.panel.buttons(23).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x1'],
                              self.lp.panel.buttons(24).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x1'],
                              self.lp.panel.buttons(25).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_2'],
                              self.lp.panel.buttons(26).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x2'],
                              self.lp.panel.buttons(27).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x2'],
                              self.lp.panel.buttons(28).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x2'],
                              self.lp.panel.buttons(29).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x2'],
                              self.lp.panel.buttons(30).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x2'],
                              self.lp.panel.buttons(31).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x2'],
                              self.lp.panel.buttons(32).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x2'],
                              self.lp.panel.buttons(33).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x2'],
                              self.lp.panel.buttons(34).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_3'],
                              self.lp.panel.buttons(35).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x3'],
                              self.lp.panel.buttons(36).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x3'],
                              self.lp.panel.buttons(37).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x3'],
                              self.lp.panel.buttons(38).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x3'],
                              self.lp.panel.buttons(39).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x3'],
                              self.lp.panel.buttons(40).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x3'],
                              self.lp.panel.buttons(41).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x3'],
                              self.lp.panel.buttons(42).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x3'],
                              self.lp.panel.buttons(43).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_4'],
                              self.lp.panel.buttons(44).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x4'],
                              self.lp.panel.buttons(45).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x4'],
                              self.lp.panel.buttons(46).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x4'],
                              self.lp.panel.buttons(47).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x4'],
                              self.lp.panel.buttons(48).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x4'],
                              self.lp.panel.buttons(49).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x4'],
                              self.lp.panel.buttons(50).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x4'],
                              self.lp.panel.buttons(51).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x4'],
                              self.lp.panel.buttons(52).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_5'],
                              self.lp.panel.buttons(53).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x5'],
                              self.lp.panel.buttons(54).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x5'],
                              self.lp.panel.buttons(55).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x5'],
                              self.lp.panel.buttons(56).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x5'],
                              self.lp.panel.buttons(57).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x5'],
                              self.lp.panel.buttons(58).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x5'],
                              self.lp.panel.buttons(59).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x5'],
                              self.lp.panel.buttons(60).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x5'],
                              self.lp.panel.buttons(61).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_6'],
                              self.lp.panel.buttons(62).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x6'],
                              self.lp.panel.buttons(63).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x6'],
                              self.lp.panel.buttons(64).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x6'],
                              self.lp.panel.buttons(65).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x6'],
                              self.lp.panel.buttons(66).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x6'],
                              self.lp.panel.buttons(67).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x6'],
                              self.lp.panel.buttons(68).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x6'],
                              self.lp.panel.buttons(69).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x6'],
                              self.lp.panel.buttons(70).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_7'],
                              self.lp.panel.buttons(71).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x7'],
                              self.lp.panel.buttons(72).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x7'],
                              self.lp.panel.buttons(73).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x7'],
                              self.lp.panel.buttons(74).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x7'],
                              self.lp.panel.buttons(75).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x7'],
                              self.lp.panel.buttons(76).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x7'],
                              self.lp.panel.buttons(77).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x7'],
                              self.lp.panel.buttons(78).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x7'],
                              self.lp.panel.buttons(79).names,
                              'Button name mismatch.')
        self.assertCountEqual(['stop_solo_mute'],
                              self.lp.panel.buttons(80).names,
                              'Button name mismatch.')

        self.assertCountEqual(['up', '7x7', 'stop_solo_mute'],
                              self.lp.panel.buttons(0, 79, 80).names,
                              'Button name mismatch.')
        self.assertCountEqual(['up'],
                              self.lp.panel.buttons(0, 0, 0).names,
                              'Button name mismatch.')

    def test_names_by_xy(self):
        self.lp.open()
        self.assertCountEqual(['up'],
                              self.lp.panel.buttons((0, 0)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['down'],
                              self.lp.panel.buttons((1, 0)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['left'],
                              self.lp.panel.buttons((2, 0)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['right'],
                              self.lp.panel.buttons((3, 0)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['session'],
                              self.lp.panel.buttons((4, 0)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['drums'],
                              self.lp.panel.buttons((5, 0)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['keys'],
                              self.lp.panel.buttons((6, 0)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['user'],
                              self.lp.panel.buttons((7, 0)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['logo'],
                              self.lp.panel.buttons((8, 0)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x0'],
                              self.lp.panel.buttons((0, 1)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x0'],
                              self.lp.panel.buttons((1, 1)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x0'],
                              self.lp.panel.buttons((2, 1)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x0'],
                              self.lp.panel.buttons((3, 1)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x0'],
                              self.lp.panel.buttons((4, 1)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x0'],
                              self.lp.panel.buttons((5, 1)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x0'],
                              self.lp.panel.buttons((6, 1)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x0'],
                              self.lp.panel.buttons((7, 1)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_1'],
                              self.lp.panel.buttons((8, 1)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x1'],
                              self.lp.panel.buttons((0, 2)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x1'],
                              self.lp.panel.buttons((1, 2)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x1'],
                              self.lp.panel.buttons((2, 2)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x1'],
                              self.lp.panel.buttons((3, 2)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x1'],
                              self.lp.panel.buttons((4, 2)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x1'],
                              self.lp.panel.buttons((5, 2)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x1'],
                              self.lp.panel.buttons((6, 2)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x1'],
                              self.lp.panel.buttons((7, 2)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_2'],
                              self.lp.panel.buttons((8, 2)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x2'],
                              self.lp.panel.buttons((0, 3)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x2'],
                              self.lp.panel.buttons((1, 3)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x2'],
                              self.lp.panel.buttons((2, 3)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x2'],
                              self.lp.panel.buttons((3, 3)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x2'],
                              self.lp.panel.buttons((4, 3)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x2'],
                              self.lp.panel.buttons((5, 3)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x2'],
                              self.lp.panel.buttons((6, 3)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x2'],
                              self.lp.panel.buttons((7, 3)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_3'],
                              self.lp.panel.buttons((8, 3)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x3'],
                              self.lp.panel.buttons((0, 4)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x3'],
                              self.lp.panel.buttons((1, 4)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x3'],
                              self.lp.panel.buttons((2, 4)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x3'],
                              self.lp.panel.buttons((3, 4)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x3'],
                              self.lp.panel.buttons((4, 4)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x3'],
                              self.lp.panel.buttons((5, 4)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x3'],
                              self.lp.panel.buttons((6, 4)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x3'],
                              self.lp.panel.buttons((7, 4)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_4'],
                              self.lp.panel.buttons((8, 4)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x4'],
                              self.lp.panel.buttons((0, 5)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x4'],
                              self.lp.panel.buttons((1, 5)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x4'],
                              self.lp.panel.buttons((2, 5)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x4'],
                              self.lp.panel.buttons((3, 5)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x4'],
                              self.lp.panel.buttons((4, 5)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x4'],
                              self.lp.panel.buttons((5, 5)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x4'],
                              self.lp.panel.buttons((6, 5)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x4'],
                              self.lp.panel.buttons((7, 5)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_5'],
                              self.lp.panel.buttons((8, 5)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x5'],
                              self.lp.panel.buttons((0, 6)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x5'],
                              self.lp.panel.buttons((1, 6)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x5'],
                              self.lp.panel.buttons((2, 6)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x5'],
                              self.lp.panel.buttons((3, 6)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x5'],
                              self.lp.panel.buttons((4, 6)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x5'],
                              self.lp.panel.buttons((5, 6)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x5'],
                              self.lp.panel.buttons((6, 6)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x5'],
                              self.lp.panel.buttons((7, 6)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_6'],
                              self.lp.panel.buttons((8, 6)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x6'],
                              self.lp.panel.buttons((0, 7)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x6'],
                              self.lp.panel.buttons((1, 7)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x6'],
                              self.lp.panel.buttons((2, 7)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x6'],
                              self.lp.panel.buttons((3, 7)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x6'],
                              self.lp.panel.buttons((4, 7)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x6'],
                              self.lp.panel.buttons((5, 7)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x6'],
                              self.lp.panel.buttons((6, 7)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x6'],
                              self.lp.panel.buttons((7, 7)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['scene_launch_7'],
                              self.lp.panel.buttons((8, 7)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['0x7'],
                              self.lp.panel.buttons((0, 8)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['1x7'],
                              self.lp.panel.buttons((1, 8)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['2x7'],
                              self.lp.panel.buttons((2, 8)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['3x7'],
                              self.lp.panel.buttons((3, 8)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['4x7'],
                              self.lp.panel.buttons((4, 8)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['5x7'],
                              self.lp.panel.buttons((5, 8)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['6x7'],
                              self.lp.panel.buttons((6, 8)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['7x7'],
                              self.lp.panel.buttons((7, 8)).names,
                              'Button name mismatch.')
        self.assertCountEqual(['stop_solo_mute'],
                              self.lp.panel.buttons((8, 8)).names,
                              'Button name mismatch.')

        self.assertCountEqual(['up', '7x7', 'stop_solo_mute'],
                              self.lp.panel.buttons((0, 0), (7, 8), (8, 8)).names,  # noqa
                              'Button name mismatch.')
        self.assertCountEqual(['up'],
                              self.lp.panel.buttons((0, 0), (0, 0), (0, 0)).names,  # noqa
                              'Button name mismatch.')

    def test_prog_layout_poll_event(self):
        self.lp.open()
        self.lp.will_return(midi_event=VirtualMidiEvent([0xb0, 0x5b, 0x7f]))  # noqa
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event().message,
                         VirtualMidiEvent([0xb0, 0x5b, 0x7f]).message,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event().button.name,  # noqa
                         'up',
                         'Button name mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event().type,  # noqa
                         ButtonEvent.PRESS,
                         'Event type mismatch.')

        self.lp.will_return(midi_event=VirtualMidiEvent([0xb0, 0x5b, 0x0]))  # noqa
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event().message,
                         VirtualMidiEvent([0xb0, 0x5b, 0x0]).message,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event().button.name,  # noqa
                         'up',
                         'Button name mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event().type,  # noqa
                         ButtonEvent.RELEASE,
                         'Event type mismatch.')

    def test_prog_layout_poll_event_with_input_string(self):
        self.lp.open()
        self.lp.will_return(midi_event=VirtualMidiEvent([0xb0, 0x5b, 0x7f]))  # noqa
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press').message,  # noqa
                         VirtualMidiEvent([0xb0, 0x5b, 0x7f]).message,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press').button.name,  # noqa
                         'up',
                         'Button name mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press').type,  # noqa
                         ButtonEvent.PRESS,
                         'Event type mismatch.')

        self.lp.will_return(midi_event=VirtualMidiEvent([0xb0, 0x5b, 0x0]))  # noqa
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='release').message,  # noqa
                         VirtualMidiEvent([0xb0, 0x5b, 0x0]).message,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='release').button.name,  # noqa
                         'up',
                         'Button name mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='release').type,  # noqa
                         ButtonEvent.RELEASE,
                         'Event type mismatch.')

        self.lp.will_return(midi_event=VirtualMidiEvent([0xb0, 0x5b, 0x7f]))  # noqa
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press_release').message,  # noqa
                         VirtualMidiEvent([0xb0, 0x5b, 0x7f]).message,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press_release').button.name,  # noqa
                         'up',
                         'Button name mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press_release').type,  # noqa
                         ButtonEvent.PRESS,
                         'Event type mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='PRESS').type,  # noqa
                         ButtonEvent.PRESS,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press|release').type,  # noqa
                         ButtonEvent.PRESS,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='PRESS_RELEASE').type,  # noqa
                         ButtonEvent.PRESS,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='PRESS|RELEASE').type,  # noqa
                         ButtonEvent.PRESS,
                         'MIDI message mismatch.')

        self.lp.will_return(midi_event=VirtualMidiEvent([0xb0, 0x5b, 0x0]))  # noqa
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press_release').message,  # noqa
                         VirtualMidiEvent([0xb0, 0x5b, 0x0]).message,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press_release').button.name,  # noqa
                         'up',
                         'Button name mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press_release').type,  # noqa
                         ButtonEvent.RELEASE,
                         'Event type mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='RELEASE').type,  # noqa
                         ButtonEvent.RELEASE,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='press|release').type,  # noqa
                         ButtonEvent.RELEASE,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='PRESS_RELEASE').type,  # noqa
                         ButtonEvent.RELEASE,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='PRESS|RELEASE').type,  # noqa
                         ButtonEvent.RELEASE,
                         'MIDI message mismatch.')

        with self.assertRaises(ValueError):
            self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='pr').message,  # noqa
                             VirtualMidiEvent([0xb0, 0x5b, 0x0]).message,
                             'MIDI message mismatch.')
        with self.assertRaises(ValueError):
            self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='rel').message,  # noqa
                             VirtualMidiEvent([0xb0, 0x5b, 0x0]).message,
                             'MIDI message mismatch.')

        with self.assertRaises(ValueError):
            self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='pr').message,  # noqa
                             VirtualMidiEvent([0xb0, 0x5b, 0x7f]).message,
                             'MIDI message mismatch.')
        with self.assertRaises(ValueError):
            self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type='rel').message,  # noqa
                             VirtualMidiEvent([0xb0, 0x5b, 0x7f]).message,
                             'MIDI message mismatch.')

    def test_prog_layout_poll_event_with_button_event_constants(self):
        self.lp.open()
        self.lp.will_return(midi_event=VirtualMidiEvent([0xb0, 0x5b, 0x7f]))  # noqa
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.PRESS).message,  # noqa
                         VirtualMidiEvent([0xb0, 0x5b, 0x7f]).message,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.PRESS).button.name,  # noqa
                         'up',
                         'Button name mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.PRESS).type,  # noqa
                         ButtonEvent.PRESS,
                         'Event type mismatch.')
        self.lp.will_return(midi_event=VirtualMidiEvent([0xb0, 0x5b, 0x0]))  # noqa
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.RELEASE).message,  # noqa
                         VirtualMidiEvent([0xb0, 0x5b, 0x0]).message,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.RELEASE).button.name,  # noqa
                         'up',
                         'Button name mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.RELEASE).type,  # noqa
                         ButtonEvent.RELEASE,
                         'Event type mismatch.')

        self.lp.will_return(midi_event=VirtualMidiEvent([0xb0, 0x5b, 0x7f]))  # noqa
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.PRESS_RELEASE).message,  # noqa
                         VirtualMidiEvent([0xb0, 0x5b, 0x7f]).message,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.PRESS_RELEASE).button.name,  # noqa
                         'up',
                         'Button name mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.PRESS_RELEASE).type,  # noqa
                         ButtonEvent.PRESS,
                         'Event type mismatch.')

        self.lp.will_return(midi_event=VirtualMidiEvent([0xb0, 0x5b, 0x0]))  # noqa
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.PRESS_RELEASE).message,  # noqa
                         VirtualMidiEvent([0xb0, 0x5b, 0x0]).message,
                         'MIDI message mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.PRESS_RELEASE).button.name,  # noqa
                         'up',
                         'Button name mismatch.')
        self.assertEqual(self.lp.panel.buttons('up').poll_for_event(type=ButtonEvent.PRESS_RELEASE).type,  # noqa
                         ButtonEvent.RELEASE,
                         'Event type mismatch.')


if __name__ == '__main__':
    unittest.main()
