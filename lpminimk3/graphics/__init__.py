from ._utils import String as _String,\
                     Renderable
from ..colors import ColorPalette as _ColorPalette


class Text(Renderable):
    def __init__(self, text, *,
                 fg_color=_ColorPalette.Red.SHADE_4,
                 bg_color=None):
        if not isinstance(text, str):
            raise TypeError('Must be of type str.')

        self._text = text
        self._string = _String(text,
                               fg_color=fg_color,
                               bg_color=bg_color)

    def __repr__(self):
        return f"Text('{self._text}')"

    def __str__(self):
        return self._text

    @Renderable.bits.getter
    def bits(self):
        return self._string.bits

    @Renderable.word_count.getter
    def word_count(self):
        return self._string.word_count

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
