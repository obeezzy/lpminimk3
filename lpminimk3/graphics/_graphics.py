import os
from ..colors import ColorPalette
from ._renderable import Renderable,\
                         RenderableColor,\
                         String,\
                         TextScroll,\
                         MovieRoll,\
                         Bitmap as _Bitmap,\
                         Movie as _Movie
from ._utils import ScrollDirection,\
                    FlipAxis,\
                    Framerate
from ._renderable import Frame  # noqa


class Text(Renderable):
    """
    Text renderable on the Launchpad's surface. The text
    rendered can be transformed by calling any of the
    transformation methods of this class.


    EXAMPLES
    Render text on Launchpad's surface:
        lp.grid.render(Text('A'))

    Print the text in the console:
        Text('A').print()

    Scroll text and render text on Launchpad's surface:
        lp.grid.render(Text(' Hello, world!').scroll())

    Scroll text and render text in the console:
        Text(' Hello, world!').print()

    Set the foreground color to "blue", rotate the text
    anticlockwise by 90 degrees, flip the text on its 'X'
    axis and scroll once:
        lp.grid.render(Text(' Hello, world!')
                       .fg_color.set('blue')
                       .rotate(-90)
                       .flip()
                       .scroll(count=1))
    """
    def __init__(self,
                 text='', *,
                 fg_color=ColorPalette.Red.SHADE_4,
                 bg_color=None):
        if isinstance(text, Text):
            text = text.text
            fg_color = text.fg_color
            bg_color = text.bg_color
        elif not isinstance(text, str):
            raise TypeError('Must be of type str.')

        self._text = text
        self._string = String(text,
                              fg_color=RenderableColor(self,
                                                       fg_color),
                              bg_color=RenderableColor(self,
                                                       bg_color))

    def __repr__(self):
        return f"Text('{self._text}')"

    def __str__(self):
        return self._text

    def __len__(self):
        return len(self._text)

    @Renderable.bits.getter
    def bits(self):
        """
        Text as bits (i.e. 0s and 1s).
        """
        return self._string.bits

    @Renderable.word_count.getter
    def word_count(self):
        """
        Number of (bit)words.
        """
        return self._string.word_count

    @property
    def fg_color(self):
        """
        Foreground color.
        """
        return self._string.fg_color

    @fg_color.setter
    def fg_color(self, color):
        self._string.fg_color = RenderableColor(self, color)

    @property
    def bg_color(self):
        """
        Background color.
        """
        return self._string.bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._string.bg_color = RenderableColor(self, color)

    def print(self, one='X', zero=' '):
        """
        Prints text to the screen as bits, used to give a preview of
        how text would be rendered on the Launchpad's surface.

        Keyword Args:
            one (str): Character to represent bit 1.
            zero (str): Character to represent bit 0.

        Returns:
            Text: `Text` reference.
        """
        self._string.print(one=one, zero=zero)

    def shift(self, count=1, *, circular=True):
        """
        Shifts text to the left if `count` is positive, or to the
        right if `count` is negative.

        Args:
            count (int): Number of times to shift.

        Keyword Args:
            circular (bool): If True, enable text wrapping; else
                diable text wrapping.

        Returns:
            Text: `Text` reference.

        Raises:
            ValueError: When invalid value is set.
        """
        if not isinstance(count, int):
            raise ValueError("'count' must be 'int'.")
        if count > 0:
            self._string.shift_right(count=count, circular=circular)
        elif count < 0:
            self._string.shift_left(count=int(abs(count)), circular=circular)
        return self

    def rotate(self, angle):
        """
        Rotates rendered text by `angle` degrees. All values
        must be a multiples of 90.

        Args:
            angle (int): Angle of rotation in degrees.
                A negative `angle` rotates Text in an anticlockwise
                direction; a positive `angle` clockwise.

        Returns:
            Text: `Text` reference.
        """
        self._string.rotate(angle)
        return self

    def scroll(self, *,
               period=.05,
               direction=ScrollDirection.LEFT,
               cycle_func=None,
               count=None,
               timeout=None):
        """
        Scrolls rendered text, shifting every `period` seconds in the
        `direction` direction; scrolls indefinitely if `count` is not
        set.

        Keyword Args:
            period (float): Delay before every text render call.
            direction (str): Direction of scroll, either left or right.
                (See :class:`ScrollDirection`.)
            cycle_func (callable): Function to be called right after
                text render call but before period delay. The function
                signature is:
                    cycle_func(fraction, launchpad)
                where `fraction` is the fraction of the scroll (ranging
                from 0 to 1) and `launchpad` is the Launchpad reference.
            count (int): Number of complete scrolls. Scrolls
                indefinitely if `count` and `timeout` are not set.
            timeout (float): Duration in seconds for scroll. Scrolls
                indefinitely if `count` and `timeout` are not set.
                If both `timeout` and `count` are set, the scroll will
                end depending on which value is reached first.

        Returns:
            Text: `Text` reference.

        Raises:
            ValueError: When invalid value is set.
        """
        if timeout and timeout <= period:
            raise ValueError("'timeout' must be greater than "
                             "or equal to the period.")
        if cycle_func and not callable(cycle_func):
            raise ValueError("'cycle_func' must be callable.")
        self._string.text_scroll = TextScroll(self._text,
                                              period,
                                              direction,
                                              cycle_func=cycle_func,
                                              timeout=timeout,
                                              count=count)
        return self

    def flip(self, axis=FlipAxis.X):
        """
        Flips text on `axis` axis.

        Args:
            axis (str): Axis to flip on (X, Y or both).
                (See :class:`FlipAxis`.)

        Returns:
            Text: `Text` reference.
        """
        self._string.flip_axis = axis
        return self

    def swap_colors(self):
        """
        Swaps foreground and background colors.

        Returns:
            Text: `Text` reference.
        """
        self._string.fg_color, self._string.bg_color = self._string.bg_color, self._string.fg_color  # noqa
        return self

    def render(self, matrix):
        """
        Renders text on matrix `matrix`. Used for internal purposes only.
        """
        self._string.render(matrix)


class Bitmap(Renderable):
    def __init__(self,
                 filename, *,
                 fg_color=None,
                 bg_color=None):
        if not isinstance(filename, str):
            raise TypeError('Must be of type str.')
        if not filename:
            raise ValueError('No filename set.')
        self._bitmap = _Bitmap(filename,
                               fg_color=RenderableColor(self,
                                                        fg_color),
                               bg_color=RenderableColor(self,
                                                        bg_color))

    def __repr__(self):
        return ("Bitmap("
                f"filename='{os.path.basename(self.filename)}')")

    def __str__(self):
        return repr(self)

    @Renderable.bits.getter
    def bits(self):
        return self._bitmap.bits

    @Renderable.word_count.getter
    def word_count(self):
        return self._bitmap.word_count

    @property
    def filename(self):
        return self._bitmap.filename

    @property
    def fg_color(self):
        return self._bitmap.fg_color

    @fg_color.setter
    def fg_color(self, color):
        self._bitmap.fg_color = RenderableColor(self, color)

    @property
    def bg_color(self):
        return self._bitmap.bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._bitmap.bg_color = RenderableColor(self, color)

    def render(self, matrix):
        self._bitmap.render(matrix)

    def print(self, *,
              one='X',
              zero=' '):
        self._bitmap.print(one=one, zero=zero)

    def swap_colors(self):
        self._bitmap.fg_color, self._bitmap.bg_color = self._bitmap.bg_color, self._bitmap.fg_color  # noqa
        return self


class Movie(Renderable):
    def __init__(self,
                 filename, *,
                 fg_color=None,
                 bg_color=None):
        if not isinstance(filename, str):
            raise TypeError('Must be of type str.')
        if not filename:
            raise ValueError('No filename set.')
        self._movie = _Movie(filename,
                             fg_color=RenderableColor(self,
                                                      fg_color),
                             bg_color=RenderableColor(self,
                                                      bg_color))

    def __repr__(self):
        return ("Movie("
                f"filename='{os.path.basename(self.filename)}')")

    def __str__(self):
        return repr(self)

    @Renderable.bits.getter
    def bits(self):
        return self._movie.bits

    @Renderable.word_count.getter
    def word_count(self):
        return self._movie.word_count

    @property
    def filename(self):
        return self._movie.filename

    @property
    def fg_color(self):
        return self._movie.fg_color

    @fg_color.setter
    def fg_color(self, color):
        self._movie.fg_color = RenderableColor(self, color)

    @property
    def bg_color(self):
        return self._movie.bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._movie.bg_color = RenderableColor(self, color)

    @property
    def framerate(self):
        return Framerate(self, self._movie)

    @property
    def frames(self):
        return self._movie.frames

    @property
    def first_frame(self):
        return self._movie.first_frame

    @property
    def last_frame(self):
        return self._movie.last_frame

    @property
    def position(self):
        return self._movie.position

    @position.setter
    def position(self, position):
        self._movie.position = position

    def render(self, matrix):
        self._movie.render(matrix)

    def play(self, *,
             count=None,
             cycle_func=None):
        if cycle_func and not callable(cycle_func):
            raise ValueError("'cycle_func' must be callable.")
        self._movie.roll = MovieRoll(self._movie,
                                     int(self.framerate),
                                     cycle_func=cycle_func,
                                     count=count)
        return self

    def skip(self, frame_count=1):
        return self._movie.skip(frame_count, ref=self)

    def print(self, *,
              one='X',
              zero=' '):
        self._movie.print(one=one, zero=zero)

    def swap_colors(self):
        self._movie.fg_color, self._movie.bg_color = self._movie.bg_color, self._movie.fg_color  # noqa
        return self
