"""Title screen — press Z to begin."""
import pyxel
from rooms.base import Room
from entities import SCREEN_W, PLAY_AREA_H


class TitleRoom(Room):
    name = "Title"
    bg_color = 0

    def setup(self) -> None:
        self._blink = 0

    def update(self) -> None:
        self._blink = (self._blink + 1) % 60
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_RETURN):
            self.state.next_room = "kitchen"

    def draw(self) -> None:
        pyxel.cls(0)
        # Title
        pyxel.text(SCREEN_W // 2 - 50, 24, "DUNGEON BROWSER", 8)
        pyxel.text(SCREEN_W // 2 - 18, 34, "ALISON", 10)
        pyxel.line(20, 44, SCREEN_W - 20, 44, 5)
        # Tagline
        pyxel.text(12, 56, "A retro escape-room RPG", 6)
        pyxel.text(12, 64, "starring the Gretz family.", 6)
        # Prompt
        if self._blink < 40:
            pyxel.text(SCREEN_W // 2 - 38, 96, "PRESS Z TO BEGIN", 7)
        pyxel.text(4, PLAY_AREA_H + 22, "arrows: move  Z: interact  Q: quit", 13)
