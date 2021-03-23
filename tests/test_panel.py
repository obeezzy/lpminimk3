import unittest
from lpminimk3.__init__ import ButtonFace
from tests._vlpminimk3 import create_virtual_launchpad


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
                         9,
                         'Max X mismatch.')

    def test_max_y(self):
        self.lp.open()
        self.assertEqual(self.lp.panel.max_y,
                         9,
                         'Max Y mismatch.')

    def test_led_id_by_xy(self):
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

    def test_led_x_by_xy(self):
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

    def test_led_y_by_xy(self):
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

    def test_led_name_by_button_face(self):
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

    def test_led_color_by_xy(self):
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

    def test_led_id_by_button_name(self):
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

    def test_led_name_by_id(self):
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

    def test_led_reset(self):
        self.lp.open()
        self.lp.panel.led('up').color = 1
        self.lp.panel.led('up').reset()


if __name__ == '__main__':
    unittest.main()
