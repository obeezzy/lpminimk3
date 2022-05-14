import math
from ._parser import BitmapConfig


class RawBitmapMatrix:
    def __init__(self, raw_bitmap):
        self._raw_bitmap = raw_bitmap
        self._raw_matrix = self._load(raw_bitmap)

    def __repr__(self):
        return ('RawBitmapMatrix('
                f'bit={self._raw_matrix})')

    def bit(self, x, y):
        return self._raw_matrix[y][x]

    def rotated_range(self, angle, *, flip_axis=''):
        assert angle, 'Angle cannot be zero.'
        angle = self._normalize_angle(angle)
        angle = self._flip_angle(angle)
        angle_rad = math.radians(angle)
        for index, bit in enumerate(self._raw_bitmap):
            x = int(index / self._raw_bitmap.word_count)
            y = int(index % self._raw_bitmap.word_count)
            max_x = max_y = self._raw_bitmap.word_count - 1
            rotated_x = round((y * math.sin(angle_rad)) + (x * math.cos(angle_rad)))  # noqa
            rotated_y = round((y * math.cos(angle_rad)) - (x * math.sin(angle_rad)))  # noqa
            x_flip_required = y_flip_required = False
            if angle == 90:
                rotated_y = min(max_y + rotated_y, max_y)
                x_flip_required = (FlipAxis.X in flip_axis)
                y_flip_required = (FlipAxis.Y in flip_axis)
            elif angle == 180:
                rotated_y = min(max_y + rotated_y, max_y)
                rotated_x = min(max_x + rotated_x, max_x)
                x_flip_required = FlipAxis.Y in flip_axis
                y_flip_required = FlipAxis.X in flip_axis
            elif angle == 270:
                rotated_x = min(max_x + rotated_x, max_x)
                x_flip_required = (FlipAxis.X in flip_axis)
                y_flip_required = (FlipAxis.Y in flip_axis)
            if flip_axis:
                flipped_x = (self._flip_axis(rotated_x)
                             if x_flip_required
                             else rotated_x)
                flipped_y = (self._flip_axis(rotated_y)
                             if y_flip_required
                             else rotated_y)
                yield self.bit(flipped_x, flipped_y)
            else:
                yield self.bit(rotated_x, rotated_y)

    def flipped_range(self, axis):
        for index, bit in enumerate(self._raw_bitmap):
            x = int(index / self._raw_bitmap.word_count)
            y = int(index % self._raw_bitmap.word_count)
            flipped_x = (self._flip_axis(x)
                         if FlipAxis.Y in axis
                         else x)
            flipped_y = (self._flip_axis(y)
                         if FlipAxis.X in axis
                         else y)
            yield self.bit(flipped_x, flipped_y)

    def _blank_matrix(self):
        matrix = []
        for _ in range(self._raw_bitmap.word_count):
            matrix.append([])
            for _ in range(self._raw_bitmap.word_count):
                matrix[-1].append(0)
        return matrix

    def _load(self, raw_bitmap):
        matrix = self._blank_matrix()
        for index, bit in enumerate(raw_bitmap):
            x = int(index % raw_bitmap.word_count)
            y = int(index / raw_bitmap.word_count)
            matrix[x][y] = bit

        return matrix

    def _normalize_angle(self, angle):
        if angle and (angle % 90) == 0 and abs(angle) > 270:
            return angle % 360
        assert (round(abs(angle)) in (0, 90, 180, 270)), \
               'Angle must be a multiple of 90.'
        return angle

    def _flip_axis(self, value):
        max_value = self._raw_bitmap.word_count - 1
        return max_value - value

    def _flip_angle(self, angle):
        if angle == -90 or angle == 270:
            return 90
        elif angle == -180:
            return 180
        elif angle == 90 or angle == -270:
            return 270
        return angle


class RawBitmap:
    def __init__(self, bitmap_data, config_data=None):
        assert isinstance(bitmap_data, list)
        self._data = bitmap_data
        self._config = BitmapConfig(config_data)

    def __iter__(self):
        for word in self._data:
            bitmask = 1
            for _ in range(self.word_count):
                bit = 1 if (word & bitmask) else 0
                yield bit
                bitmask = bitmask << 1

    def __repr__(self):
        return f"RawBitmap('{self._data}')"

    def __str__(self):
        bit_string = ''
        for index, bit in enumerate(self, start=1):
            bit_string += str(bit)
            bit_string += ('\n'
                           if index % self.word_count == 0
                           else ' ')
        return bit_string

    @property
    def data(self):
        return self._data

    @property
    def word_count(self):
        return len(self._data)

    @property
    def config(self):
        return self._config

    def render(self):
        pass


class Offset:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def __repr__(self):
        return f'Offset({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Framerate:
    def __init__(self,
                 movie_ref,
                 movie):
        self._movie_ref = movie_ref
        self._movie = movie

    def set(self, framerate):
        self._movie.framerate = framerate
        return self._movie_ref

    def __int__(self):
        return self._movie.framerate

    def __repr__(self):
        return f"Framerate({self._movie.framerate})"

    def __str__(self):
        return repr(self)


class FlipAxis:
    X = 'x'
    Y = 'y'
    XY = 'xy'


class ScrollDirection:
    LEFT = 'left'
    RIGHT = 'right'
