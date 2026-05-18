"""Dialogue box: queue lines, page through with Z, word-wrap inside a bordered box."""
import pyxel

SCREEN_W = 160
SCREEN_H = 120
BOX_H = 36
PAD = 4
LINE_H = 8
CHARS_PER_LINE = 36  # rough fit at 4px font width


def _wrap(text: str, width: int = CHARS_PER_LINE) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        candidate = (cur + " " + w).strip()
        if len(candidate) <= width:
            cur = candidate
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Dialogue:
    """A simple page-by-page dialogue queue. Speaker is optional."""

    def __init__(self) -> None:
        self.pages: list[tuple[str, str]] = []  # (speaker, line)
        self.cursor_blink = 0

    @property
    def active(self) -> bool:
        return bool(self.pages)

    def say(self, line: str, speaker: str = "") -> None:
        self.pages.append((speaker, line))

    def say_many(self, lines: list[str], speaker: str = "") -> None:
        for line in lines:
            self.say(line, speaker)

    def update(self) -> None:
        if not self.active:
            return
        self.cursor_blink = (self.cursor_blink + 1) % 30
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.pages.pop(0)

    def draw(self) -> None:
        if not self.active:
            return
        speaker, line = self.pages[0]
        y0 = SCREEN_H - BOX_H
        pyxel.rect(0, y0, SCREEN_W, BOX_H, 1)
        pyxel.rectb(0, y0, SCREEN_W, BOX_H, 7)
        if speaker:
            pyxel.text(PAD, y0 + 2, speaker, 10)
            text_y = y0 + 2 + LINE_H
        else:
            text_y = y0 + PAD
        for i, wrapped in enumerate(_wrap(line)):
            pyxel.text(PAD, text_y + i * LINE_H, wrapped, 7)
        if self.cursor_blink < 15:
            pyxel.text(SCREEN_W - 10, y0 + BOX_H - 8, "\x86", 10)
