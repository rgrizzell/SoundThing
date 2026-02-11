import os

import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.text_box import TextBox
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_displayio_layout.widgets.widget import Widget
from displayio import Bitmap, ColorConverter, Colorspace, Group, TileGrid
from jpegio import JpegDecoder

try:
    from fontio import FontProtocol
except ImportError:
    pass

decoder = JpegDecoder()


class GUI(Group):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        self.width = width
        self.height = height

        self.background = Rect(0, 0, width=width, height=height, fill=0x000000)
        self.append(self.background)
        self.layout = GridLayout(
            x=0,
            y=0,
            width=width,
            height=height,
            grid_size=(2, 2),
            cell_padding=10,
            divider_lines=True,
        )
        self.append(self.layout)

        artwork = Rect(0, 0, width=120, height=120, outline=0xFFFFFF)
        self.layout.add_content(
            artwork,
            grid_position=(0, 0),
            cell_size=(1, 2),
            cell_anchor_point=(0.5, 0.5),
        )

        self.artist = TextBox(
            text="Unknown Artist",
            x=width // 2,
            y=10,
            width=(width // 2) - 10,
            height=(height // 2) - 10,
            align=TextBox.ALIGN_LEFT,
            font=load_font(os.getenv("SOUNDTHING_ARTIST_FONT")),
            scale=os.getenv("SOUNDTHING_ARTIST_FONT_SCALE", 1),
        )
        self.layout.add_content(self.artist, grid_position=(1, 0), cell_size=(1, 1))
        self.track = TextBox(
            text="Unknown Track",
            x=width // 2,
            y=height // 2,
            width=(width // 2) - 10,
            height=(height // 2) - 10,
            align=TextBox.ALIGN_LEFT,
            font=load_font(os.getenv("SOUNDTHING_TRACK_FONT")),
            scale=os.getenv("SOUNDTHING_TRACK_FONT_SCALE", 1),
        )
        self.layout.add_content(self.track, grid_position=(1, 1), cell_size=(1, 1))

    def update(self):
        pass

    def set_track_info(self, artist: str, track: str) -> None:
        self.artist.text = artist
        self.track.text = track

    def render_artwork(self, data: bytes) -> None:
        width, height = decoder.open(data)
        bitmap = Bitmap(width, height, 65536)
        decoder.decode(bitmap)
        artwork = TileGrid(
            bitmap,
            pixel_shader=ColorConverter(input_colorspace=Colorspace.RGB565_SWAPPED),
        )
        self.layout.pop_content((0, 0))
        self.layout.add_content(artwork, grid_position=(0, 0), cell_size=(1, 2))


def load_font(font_name: str | None) -> FontProtocol:
    font = terminalio.FONT
    if font_name:
        try:
            font_lib = __import__(font_name)
            font = font_lib.FONT
        except ImportError:
            print(f"[ERR] Could not find font: {font_name}")
    return font
