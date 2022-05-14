import time
from ..midi_messages import Colorspec,\
                            ColorspecFragment,\
                            Constants


class RawBitmapRenderer:
    def __init__(self,
                 raw_bitmap,
                 matrix, *,
                 angle=0,
                 flip_axis='',
                 fg_color=None,
                 bg_color=None):
        self._raw_bitmap = raw_bitmap
        self._matrix = matrix
        self._fg_color = fg_color
        self._bg_color = bg_color
        self._angle = angle
        self._flip_axis = flip_axis

    def render(self):
        colorspec_fragments = []
        for led, bit in zip(self._matrix.led_range(rotation=self._angle,
                                                   flip_axis=self._flip_axis),
                            self._raw_bitmap):
            bit_config = self._raw_bitmap.config[led.name]
            lighting_type = bit_config.lighting_type
            led_index = led.midi_value
            lighting_data = self._determine_lighting_data(bit_config,
                                                          bit,
                                                          self._fg_color,
                                                          self._bg_color)
            fragment = ColorspecFragment(lighting_type,
                                         led_index,
                                         *lighting_data)
            colorspec_fragments.append(fragment)
        payload = Colorspec(*colorspec_fragments)
        self._matrix.launchpad.send_message(payload)

    def _determine_lighting_data(self, config, bit, fg_color, bg_color):
        lighting_data = []
        if config.lighting_type == Constants.LightingType.FLASH:
            lighting_data = ([config.lighting_data.on_state.color.id]
                             if bit
                             else [config.lighting_data.off_state.color.id])
        elif config.lighting_type == Constants.LightingType.PULSE:
            lighting_data = ([config.lighting_data.on_state.color.id]
                             if bit
                             else [config.lighting_data.off_state.color.id])
        elif config.lighting_type == Constants.LightingType.RGB:
            lighting_data = (config.lighting_data.on_state.color.rgb
                             if bit
                             else config.lighting_data.off_state.color.rgb)
        else:
            fg_color_id = fg_color.color_id if fg_color else 0
            bg_color_id = bg_color.color_id if bg_color else 0
            on_state = ([config.lighting_data.on_state.color.id]
                        if config.lighting_data
                        else [fg_color_id])
            off_state = ([config.lighting_data.off_state.color.id]
                         if config.lighting_data
                         else [bg_color_id])
            lighting_data = (on_state
                             if bit
                             else off_state)
        return lighting_data


class TextRenderer:
    def __init__(self,
                 text,
                 string,
                 period,
                 direction,
                 matrix, *,
                 timeout,
                 count,
                 cycle_func):
        self._text = text
        self._string = string
        self._period = period
        self._direction = direction
        self._matrix = matrix
        self._timeout = timeout
        self._count = count
        self._cycle_func = cycle_func

    def render(self):
        time_left = self._timeout
        rotations_left = self._count
        text_width = len(self._text) * self._matrix.width
        while time_left and rotations_left:
            for _ in range(text_width):
                if self._direction == 'right':
                    self._string.shift_right()
                else:
                    self._string.shift_left()
                CharacterRenderer(self._string.character_to_render,
                                  self._matrix,
                                  angle=self._string.angle,
                                  flip_axis=self._string.flip_axis).render()
                if self._cycle_func:
                    self._cycle_func(_/text_width, self._matrix.launchpad)
                time.sleep(self._period)
                time_left = (max(time_left - self._period, 0)
                             if time_left != -1
                             else time_left)
            rotations_left = (max(rotations_left - 1, 0)
                              if rotations_left != -1
                              else rotations_left)


class CharacterRenderer:
    def __init__(self,
                 character,
                 matrix, *,
                 angle=0,
                 flip_axis=''):
        self._renderer = RawBitmapRenderer(character.raw_bitmap,
                                           matrix,
                                           angle=angle,
                                           flip_axis=flip_axis,
                                           fg_color=character.fg_color,
                                           bg_color=character.bg_color)

    def render(self):
        self._renderer.render()


class BitmapRenderer:
    def __init__(self,
                 raw_bitmap,
                 matrix, *,
                 fg_color,
                 bg_color):
        self._renderer = RawBitmapRenderer(raw_bitmap,
                                           matrix,
                                           fg_color=fg_color,
                                           bg_color=bg_color)

    def render(self):
        self._renderer.render()


class FrameRenderer:
    def __init__(self,
                 raw_bitmap,
                 matrix):
        self._renderer = RawBitmapRenderer(raw_bitmap,
                                           matrix)

    def render(self):
        self._renderer.render()


class MovieRenderer:
    def __init__(self,
                 raw_bitmaps,
                 framerate,
                 matrix, *,
                 count=None):
        self._raw_bitmaps = raw_bitmaps
        self._framerate = max(1, min(60, framerate))
        self._matrix = matrix
        self._angle = 0
        self._flip_axis = 'x'
        self._count = -1 if not count else count

    def render(self):
        period = 1 / self._framerate
        rotations_left = self._count
        while rotations_left:
            for bitmap in self._raw_bitmaps:
                renderer = RawBitmapRenderer(bitmap,
                                             self._matrix)
                renderer.render()
                time.sleep(period)
            rotations_left = (max(rotations_left - 1, 0)
                              if rotations_left != -1
                              else rotations_left)
