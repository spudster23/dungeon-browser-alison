"""Ending screen — cliffhanger after the Server Room."""
import pyxel
from rooms.base import Room
from entities import SCREEN_W, PLAY_AREA_H


class EndingRoom(Room):
    name = "Floor 1 Cleared"
    bg_color = 0

    def setup(self) -> None:
        self._t = 0

    def update(self) -> None:
        self._t += 1

    def draw(self) -> None:
        pyxel.cls(0)
        pyxel.text(SCREEN_W // 2 - 42, 16, "FLOOR 1 CLEARED", 10)
        pyxel.line(20, 26, SCREEN_W - 20, 26, 5)
        lines = [
            "The Gretz family is together.",
            "But the floor only goes deeper.",
            "",
            "Somewhere far below the house,",
            "a server hums her name.",
            "",
            "TO BE CONTINUED.",
        ]
        for i, line in enumerate(lines):
            pyxel.text(8, 36 + i * 8, line, 7 if i != 6 else 8)
        if (self._t // 30) % 2 == 0:
            pyxel.text(SCREEN_W // 2 - 36, PLAY_AREA_H + 10, "thanks for playing", 13)
