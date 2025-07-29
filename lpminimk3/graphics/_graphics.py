"""Graphics API.
"""
import os
import time
from ..colors import ColorPalette
from ..utils import Mode
from ._renderable import (Renderable,
                          RenderableColor,
                          String,
                          TextScroll,
                          MovieRoll,
                          Bitmap as _Bitmap,
                          Movie as _Movie)
from ._utils import (ScrollDirection,
                     FlipAxis,
                     Framerate)
from ._renderable import Frame  # noqa


class Text(Renderable):
    """Text renderable on the Launchpad's surface. The text
    rendered can be transformed by calling any of the
    transformation methods of this class.

    Examples
    --------
    Render text on Launchpad's surface:
        >>> lp.grid.render(Text('A'))

    Print the text in the console:
        >>> Text('A').print()

    Scroll text and render text on Launchpad's surface:
        >>> lp.grid.render(Text(' Hello, world!').scroll())

    Scroll text and render text in the console:
        >>> Text(' Hello, world!').print()

    Set the foreground color to "blue", rotate the text
    anticlockwise by 90 degrees, flip the text on its 'X'
    axis and scroll once:
        >>> lp.grid.render(Text(' Hello, world!')
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
        """Text as bits (i.e. 0s and 1s).
        """
        return self._string.bits

    @Renderable.word_count.getter
    def word_count(self):
        """Number of (bit)words.
        """
        return self._string.word_count

    @property
    def fg_color(self):
        """Foreground color.
        """
        return self._string.fg_color

    @fg_color.setter
    def fg_color(self, color):
        self._string.fg_color = RenderableColor(self, color)

    @property
    def bg_color(self):
        """Background color.
        """
        return self._string.bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._string.bg_color = RenderableColor(self, color)

    def print(self, one='X', zero=' '):
        """Prints text to the screen as bits, used to give a preview of
        how text would be rendered on the Launchpad's surface.

        Parameters
        ----------
        one : str
            Character to represent bit 1.
        zero : str
            Character to represent bit 0.

        Returns
        -------
        Text
            `Text` reference.
        """
        self._string.print(one=one, zero=zero)

    def shift(self, count=1, *, circular=True):
        """Shifts text to the left if `count` is positive, or to the
        right if `count` is negative.

        Parameters
        ----------
        count : int
            Number of times to shift.
        circular : bool
            If True, enable text wrapping; else diable text wrapping.

        Returns
        -------
        Text
            `Text` reference.

        Raises
        ------
        ValueError
            When invalid value is set.
        """
        if not isinstance(count, int):
            raise ValueError("'count' must be 'int'.")
        if count > 0:
            self._string.shift_right(count=count, circular=circular)
        elif count < 0:
            self._string.shift_left(count=int(abs(count)), circular=circular)
        return self

    def rotate(self, angle):
        """Rotates rendered text by `angle` degrees. All values
        must be a multiples of 90.

        Parameters
        ----------
        angle : int
            Angle of rotation in degrees. A negative `angle`
            rotates Text in an anticlockwise direction; a
            positive `angle` clockwise.

        Returns
        -------
        Text
            `Text` reference.
        """
        self._string.rotate(angle)
        return self

    def scroll(self, *,
               period=.05,
               direction=ScrollDirection.LEFT,
               cycle_func=None,
               count=1,
               timeout=None):
        """Scrolls rendered text, shifting every `period` seconds in the
        `direction` direction.

        Parameters
        ----------
        period : float
            Delay before every text render call.
        direction : str
            Direction of scroll, either left or right.
                (See :class:`ScrollDirection`.)
        cycle_func : callable
            Function to be called right after text render call but
            before period delay. The function signature is:
                    cycle_func(fraction, launchpad)
            where `fraction` is the fraction of the scroll (ranging
            from 0 to 1) and `launchpad` is the Launchpad reference.
        count : int
            Number of complete scrolls. Scrolls indefinitely if
            `count` is set to -1.
        timeout : float
            Duration in seconds for scroll. Scrolls indefinitely if
            `count` is set to -1 and `timeout` is not set. If both
            `timeout` and `count` are set, the scroll will end
            depending on which value is reached first.

        Returns
        -------
        Text
            `Text` reference.

        Raises
        ------
        ValueError
            When invalid value is set.
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
        """Flips text on `axis` axis.

        Parameters
        ----------
        axis : str
            Axis to flip on (X, Y or both).
            (See :class:`FlipAxis`.)

        Returns
        -------
        Text
            `Text` reference.
        """
        self._string.flip_axis = axis
        return self

    def swap_colors(self):
        """Swaps foreground and background colors.

        Returns
        -------
        Text
            `Text` reference.
        """
        self._string.fg_color, self._string.bg_color = self._string.bg_color, self._string.fg_color  # noqa
        return self

    def render(self, matrix):
        """Renders text on matrix `matrix`.
        Used for internal purposes only.
        """
        self._string.render(matrix)


class Bitmap(Renderable):
    """Bitmap renderable on the Launchpad's surface.

    Examples
    --------
    Render text on Launchpad's surface:
        >>> lp.grid.render(Bitmap('path/to/bitmap'))

    Print the text in the console:
        >>> Bitmap('path/to/bitmap').print()
    """
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
        """Bits.
        """
        return self._bitmap.bits

    @Renderable.word_count.getter
    def word_count(self):
        """Word count.
        """
        return self._bitmap.word_count

    @property
    def filename(self):
        """File name.
        """
        return self._bitmap.filename

    @property
    def fg_color(self):
        """Foreground color.
        """
        return self._bitmap.fg_color

    @fg_color.setter
    def fg_color(self, color):
        self._bitmap.fg_color = RenderableColor(self, color)

    @property
    def bg_color(self):
        """Background color.
        """
        return self._bitmap.bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._bitmap.bg_color = RenderableColor(self, color)

    def render(self, matrix):
        """Renders text on matrix `matrix`.
        Used for internal purposes only.
        """
        self._bitmap.render(matrix)

    def print(self, *,
              one='X',
              zero=' '):
        """Prints text on matrix surface. `one` is the marker
        for an on bit (1) and `zero` is the marker for an off
        bit (0).

        Parameters
        ----------
        one : str
            Character that represents 1.
        zero : str
            Character that represents 0.
        """
        self._bitmap.print(one=one, zero=zero)

    def swap_colors(self):
        self._bitmap.fg_color, self._bitmap.bg_color = self._bitmap.bg_color, self._bitmap.fg_color  # noqa
        return self


class Movie(Renderable):
    """Movie renderable on the Launchpad's surface.

    Examples
    --------
    Render text on Launchpad's surface:
        >>> lp.grid.render(Movie('path/to/movie'))

    Print the first from of the movie in the console:
        >>> Movie('path/to/movie').print()

    Play a movie on Launchpad's surface:
        >>> lp.grid.render(Movie('path/to/movie').play())

    Play movie on the console:
        >>> Movie('path/to/movie').play().print()
    """
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
        """Bits.
        """
        return self._movie.bits

    @Renderable.word_count.getter
    def word_count(self):
        """Word count.
        """
        return self._movie.word_count

    @property
    def filename(self):
        """File name.
        """
        return self._movie.filename

    @property
    def fg_color(self):
        """Foreground color.
        """
        return self._movie.fg_color

    @fg_color.setter
    def fg_color(self, color):
        self._movie.fg_color = RenderableColor(self, color)

    @property
    def bg_color(self):
        """Background color.
        """
        return self._movie.bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._movie.bg_color = RenderableColor(self, color)

    @property
    def framerate(self):
        """Frame rate.
        """
        return Framerate(self, self._movie)

    @property
    def frames(self):
        """Frames.
        """
        return self._movie.frames

    @property
    def first_frame(self):
        """First frame.
        """
        return self._movie.first_frame

    @property
    def last_frame(self):
        """Last frame.
        """
        return self._movie.last_frame

    @property
    def position(self):
        """Position.
        """
        return self._movie.position

    @position.setter
    def position(self, position):
        self._movie.position = position

    def render(self, matrix):
        """Render on matrix `matrix`.
        """
        self._movie.render(matrix)

    def play(self, *,
             count=1,
             cycle_func=None):
        """Plays movie on the Launchpad's surface.

        Parameters
        ----------
        count : int or None
            Number of times to play movie.
        cycle_func : callable or None
            Function to be called each cycle.
        """
        if cycle_func and not callable(cycle_func):
            raise ValueError("'cycle_func' must be callable.")
        self._movie.roll = MovieRoll(self._movie,
                                     int(self.framerate),
                                     cycle_func=cycle_func,
                                     count=count)
        return self

    def skip(self, frame_count=1):
        """Skips a frame by `frame_count`.

        Parameters
        ----------
        frame_count : int
            Frame count.
        """
        return self._movie.skip(frame_count, ref=self)

    def print(self, *,
              one='X',
              zero=' '):
        """Prints text on matrix surface. `one` is the marker
        for an on bit (1) and `zero` is the marker for an off
        bit (0).

        Parameters
        ----------
        one : str
            Character that represents 1.
        zero : str
            Character that represents 0.
        """
        self._movie.print(one=one, zero=zero)

    def swap_colors(self):
        """Swaps colors.
        """
        self._movie.fg_color, self._movie.bg_color = self._movie.bg_color, self._movie.fg_color  # noqa
        return self


class TextStrip:
    """Text strip that renders words on multiple Launchpad surfaces.

    Examples
    --------
    Render text on Launchpad surfaces:
        >>> lps = lpminimk3.find_launchpads()
        >>> TextStrip(*lps).render(" Hello, world!")

    Scroll text on Launchpad surfaces twice:
        >>> lps = lpminimk3.find_launchpads()
        >>> TextStrip(*lps).scroll(" Hello, world!", count=2)
    """
    def __init__(self, *lps, options={}):
        self._lps = lps
        self._options = options

    def render(self, text):
        """Render text on Launchpad surfaces.

        text : str
            Text to render.

        Returns
        -------
        TextStrip
            `TextStrip` reference.

        Raises
        ------
        ValueError
            When invalid value is set.
        """
        if not isinstance(text, str):
            raise ValueError("Invalid text set")

        texts = []
        for lp in self._lps:
            lp.open()
            lp.mode = Mode.PROG
            texts.append(Text(text))

        for index, lp in enumerate(self._lps):
            lp.grid.render(texts[index].shift(index * -1 * texts[index].word_count, circular=True))

        return self

    def scroll(self, text, *,
               count=1,
               period=.05,
               direction=ScrollDirection.LEFT):
        """Scrolls set text on Launchpad surfaces, shifting every `period` seconds in the
        `direction` direction.

        Parameters
        ----------
        text : str
            Text to scroll.
        period : float
            Delay before every text render call.
        direction : str
            Direction of scroll, either left or right.
                (See :class:`ScrollDirection`.)
        count : int
            Number of complete scrolls. Scrolls indefinitely if
            `count` is set to -1.

        Returns
        -------
        TextStrip
            `TextStrip` reference.

        Raises
        ------
        ValueError
            When invalid value is set.
        """
        if not isinstance(text, str):
            raise ValueError("Invalid text set")

        texts = []
        for index, lp in enumerate(self._lps):
            lp.open()
            lp.mode = Mode.PROG
            texts.append(Text(text))

            if index not in self._options:
                continue
            if "bg_color" in self._options[index]:
                texts[index].bg_color = self._options[index]["bg_color"]
            if "fg_color" in self._options[index]:
                texts[index].fg_color = self._options[index]["fg_color"]
            if "rotate" in self._options[index]:
                texts[index].rotate(self._options[index]["rotate"])
            if "flip" in self._options[index]:
                texts[index].flip(self._options[index]["flip"])
            if "shift" in self._options[index]:
                texts[index].shift(self._options[index]["shift"])

        for index, lp in enumerate(self._lps):
            texts[index].shift(index * -1 * texts[index].word_count, circular=True)

        direction_polarity = -1 if ScrollDirection.LEFT else 1
        try:
            if count < 1:
                while True:
                    for index, lp in enumerate(self._lps):
                        lp.grid.render(texts[index].shift(direction_polarity, circular=True))

                    time.sleep(period)
            else:
                for _ in range(len(text) * texts[0].word_count * count):
                    for index, lp in enumerate(self._lps):
                        lp.grid.render(texts[index].shift(direction_polarity, circular=True))

                    time.sleep(period)
        finally:
            for lp in self._lps:
                lp.close()

    def set_option(self, index, name, value):
        if not isinstance(index, int):
            raise ValueError("Invalid index set")
        elif index < 0 or index >= len(self._lps):
            raise ValueError("Index out of range")
        elif not isinstance(name, str):
            raise ValueError("Invalid name set")
        elif name.lower() not in ["bg_color", "fg_color", "rotate", "flip", "shift"]:
            raise ValueError(f"Invalid option '{name}'")

        if index not in self._options:
            self._options[index] = {}

        if name.lower() == "bg_color" and not isinstance(value, (str, int)):
            raise ValueError(f"Invalid BG color '{name}'")
        elif name.lower() == "fg_color" and not isinstance(value, (str, int)):
            raise ValueError(f"Invalid FG color '{name}'")
        elif name.lower() == "rotate" and value not in [0, 90, 180, 270]:
            raise ValueError(f"Invalid rotation angle '{name}'")
        elif name.lower() == "flip" and value not in [FlipAxis.X, FlipAxis.Y]:
            raise ValueError(f"Invalid flip axis '{name}'")
        elif name.lower() == "shift" and not isinstance(value, int):
            raise ValueError(f"Invalid shift count '{name}'")

        self._options[index][name] = value
        return self
