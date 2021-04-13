from ._utils import Renderable,\
                    ScrollDirection,\
                    String as _String,\
                    TextColor as _TextColor,\
                    TextScroll as _TextScroll
from ..colors import ColorPalette as _ColorPalette


class Text(Renderable):
    def __init__(self,
                 text, *,
                 fg_color=_ColorPalette.Red.SHADE_4,
                 bg_color=None):
        if isinstance(text, Text):
            text = text.text
            fg_color = text.fg_color
            bg_color = text.bg_color
        elif not isinstance(text, str):
            raise TypeError('Must be of type str.')

        self._text = text
        self._string = _String(text,
                               fg_color=_TextColor(self,
                                                   fg_color),
                               bg_color=_TextColor(self,
                                                   bg_color))

    def __repr__(self):
        return f"Text('{self._text}')"

    def __str__(self):
        return self._text

    def __len__(self):
        return len(self._text)

    @Renderable.bits.getter
    def bits(self):
        return self._string.bits

    @Renderable.word_count.getter
    def word_count(self):
        return self._string.word_count

    @property
    def fg_color(self):
        return self._string.fg_color

    @fg_color.setter
    def fg_color(self, color):
        self._string.fg_color = _TextColor(self, color)

    @property
    def bg_color(self):
        return self._string.bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._string.bg_color = _TextColor(self, color)

    def render(self, matrix):
        self._string.render(matrix)

    def print(self):
        self._string.print()

    def shift_left(self, count=1, *, circular=True):
        count = 0 if not isinstance(count, int) or count < 0 else count
        self._string.shift_left(count=count, circular=circular)
        return self

    def shift_right(self, count=1, *, circular=True):
        count = 0 if not isinstance(count, int) or count < 0 else count
        self._string.shift_right(count=count, circular=circular)
        return self

    def rotate(self, angle):
        self._string.rotate(angle)
        return self

    def scroll(self, *,
               clock_rate=.05,
               direction=ScrollDirection.LTR,
               timeout=None):
        if timeout and timeout < clock_rate:
            raise ValueError("'timeout' must be greater than the clock rate.")
        self._string.text_scroll = _TextScroll(self._text,
                                               clock_rate,
                                               direction,
                                               timeout)
        return self
