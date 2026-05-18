"""Dungeon Browser: Alison — main entry point and room state machine."""
import pyxel
from game_state import GameState
from dialogue import Dialogue
from rooms import ROOM_REGISTRY

SCREEN_W = 160
SCREEN_H = 120


class App:
    def __init__(self) -> None:
        pyxel.init(SCREEN_W, SCREEN_H, title="Dungeon Browser: Alison", fps=60)
        self.state = GameState()
        self.dialogue = Dialogue()
        self.current = self._make_room("title")
        pyxel.run(self.update, self.draw)

    def _make_room(self, name: str):
        cls = ROOM_REGISTRY[name]
        self.state.current_room = name
        self.dialogue.pages.clear()
        room = cls(self.state, self.dialogue)
        room.on_enter()
        return room

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.current.update()
        if self.state.next_room and self.state.next_room != self.state.current_room:
            self.current = self._make_room(self.state.next_room)
            self.state.next_room = None

    def draw(self) -> None:
        self.current.draw()


if __name__ == "__main__":
    App()
