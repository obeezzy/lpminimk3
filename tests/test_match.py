import unittest
from lpminimk3.__init__ import ButtonEvent
from lpminimk3.match import ButtonMatch
from tests._vlpminimk3 import create_virtual_launchpad


class TestButtonMatch(unittest.TestCase):
    def setUp(self):
        self.lp = create_virtual_launchpad()

    def tearDown(self):
        self.lp.close()

    def test_panel_contains_match_press(self):
        self.lp.open()
        match = ButtonMatch(self.lp.panel.buttons('up'), ButtonEvent.PRESS)
        self.assertTrue(match.contains([0xb0, 0x5b, 0x7f]), 'No button matched.')  # noqa

        match = ButtonMatch(self.lp.panel.buttons('up', 'down', 'left'), ButtonEvent.PRESS)  # noqa
        self.assertTrue(match.contains([0xb0, 0x5b, 0x7f]), 'No button matched.')  # noqa
        self.assertTrue(match.contains([0xb0, 0x5c, 0x7f]), 'No button matched.')  # noqa
        self.assertTrue(match.contains([0xb0, 0x5d, 0x7f]), 'No button matched.')  # noqa

        self.assertFalse(match.contains([0xb0, 0x5d, 0x0]), 'Button matched, though it shouldn\'t.')  # noqa
        self.assertFalse(match.contains([0xb0, 0x5e, 0x7f]), 'Button matched, though it shouldn\'t.')  # noqa

    def test_panel_contains_match_release(self):
        self.lp.open()
        match = ButtonMatch(self.lp.panel.buttons('up'), ButtonEvent.RELEASE)
        self.assertTrue(match.contains([0xb0, 0x5b, 0x0]), 'No button matched.')  # noqa

        match = ButtonMatch(self.lp.panel.buttons('up', 'down', 'left'), ButtonEvent.RELEASE)  # noqa
        self.assertTrue(match.contains([0xb0, 0x5b, 0x0]), 'No button matched.')  # noqa
        self.assertTrue(match.contains([0xb0, 0x5c, 0x0]), 'No button matched.')  # noqa
        self.assertTrue(match.contains([0xb0, 0x5d, 0x0]), 'No button matched.')  # noqa

        self.assertFalse(match.contains([0xb0, 0x5d, 0x7f]), 'Button matched, though it shouldn\'t.')  # noqa
        self.assertFalse(match.contains([0xb0, 0x5e, 0x0]), 'Button matched, though it shouldn\'t.')  # noqa

    def test_grid_contains_match_press(self):
        self.lp.open()
        match = ButtonMatch(self.lp.grid.buttons('0x0'), ButtonEvent.PRESS)
        self.assertTrue(match.contains([0x90, 0x51, 0x7f]), 'No button matched.')  # noqa

        match = ButtonMatch(self.lp.panel.buttons('0x0', '1x0', '2x0'), ButtonEvent.PRESS)  # noqa
        self.assertTrue(match.contains([0x90, 0x51, 0x7f]), 'No button matched.')  # noqa
        self.assertTrue(match.contains([0x90, 0x52, 0x7f]), 'No button matched.')  # noqa
        self.assertTrue(match.contains([0x90, 0x53, 0x7f]), 'No button matched.')  # noqa

        self.assertFalse(match.contains([0x90, 0x53, 0x0]), 'Button matched, though it shouldn\'t.')  # noqa
        self.assertFalse(match.contains([0x90, 0x54, 0x7f]), 'Button matched, though it shouldn\'t.')  # noqa

    def test_grid_contains_match_release(self):
        self.lp.open()
        match = ButtonMatch(self.lp.grid.buttons('0x0'), ButtonEvent.RELEASE)
        self.assertTrue(match.contains([0x90, 0x51, 0x0]), 'No button matched.')  # noqa

        match = ButtonMatch(self.lp.panel.buttons('0x0', '1x0', '2x0'), ButtonEvent.RELEASE)  # noqa
        self.assertTrue(match.contains([0x90, 0x51, 0x0]), 'No button matched.')  # noqa
        self.assertTrue(match.contains([0x90, 0x52, 0x0]), 'No button matched.')  # noqa
        self.assertTrue(match.contains([0x90, 0x53, 0x0]), 'No button matched.')  # noqa

        self.assertFalse(match.contains([0x90, 0x53, 0x7f]), 'Button matched, though it shouldn\'t.')  # noqa
        self.assertFalse(match.contains([0x90, 0x54, 0x0]), 'Button matched, though it shouldn\'t.')  # noqa
