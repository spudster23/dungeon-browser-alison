"""Base Room: each room owns its interactables, walls, puzzle state, and exit transition."""
import pyxel
from entities import Player, Interactable, TILE, SCREEN_W, PLAY_AREA_H
from dialogue import Dialogue
from game_state import GameState

ROOM_NAME = "Unknown"


class Room:
    name: str = "Unknown"
    bg_color: int = 5

    def __init__(self, state: GameState, dialogue: Dialogue) -> None:
        self.state = state
        self.dialogue = dialogue
        self.player = Player(x=16, y=PLAY_AREA_H // 2)
        self.walls: list[Interactable] = []
        self.objects: list[Interactable] = []
        self.exit_object: Interactable | None = None
        self._intro_shown = False
        self.setup()

    # --- Subclass hooks ---
    def setup(self) -> None: ...
    def intro_lines(self) -> list[tuple[str, str]]:
        """List of (speaker, line) shown on first entry. Empty = skip."""
        return []
    def is_complete(self) -> bool:
        return False
    def next_room(self) -> str | None:
        return None

    # --- Lifecycle ---
    def on_enter(self) -> None:
        if not self._intro_shown:
            for speaker, line in self.intro_lines():
                self.dialogue.say(line, speaker)
            self._intro_shown = True
        self._refresh_exit()

    def _refresh_exit(self) -> None:
        if self.exit_object is not None:
            self.exit_object.visible = self.is_complete()
            self.exit_object.solid = False  # exit is walked into, not blocked
            self.exit_object.color = 11 if self.is_complete() else 13

    # --- Interaction ---
    def _try_interact(self) -> None:
        if not pyxel.btnp(pyxel.KEY_Z):
            return
        candidates = self.objects + ([self.exit_object] if self.exit_object else [])
        for obj in candidates:
            if obj and obj.visible and obj.near(self.player.x, self.player.y):
                obj.on_interact()
                return

    def update(self) -> None:
        if self.dialogue.active:
            self.dialogue.update()
            return
        self._refresh_exit()
        if self.exit_object and self.exit_object.visible and self.exit_object.near(self.player.x, self.player.y):
            nxt = self.next_room()
            if nxt:
                self.state.next_room = nxt
                return
        self.player.update(self.walls + [o for o in self.objects if o.solid])
        self._try_interact()

    def draw(self) -> None:
        pyxel.cls(self.bg_color)
        # subtle floor pattern
        for y in range(0, PLAY_AREA_H, 8):
            for x in range(0, SCREEN_W, 8):
                if (x // 8 + y // 8) % 2 == 0:
                    pyxel.pset(x + 4, y + 4, self.bg_color + 1 if self.bg_color < 15 else self.bg_color - 1)
        for w in self.walls:
            w.draw()
        for o in self.objects:
            o.draw()
        if self.exit_object:
            self.exit_object.draw()
        self.player.draw()
        # HUD
        pyxel.text(2, PLAY_AREA_H + 2, self.name, 7)
        if self.state.inventory:
            pyxel.text(2, PLAY_AREA_H + 10, "Bag:" + ",".join(self.state.inventory), 6)
        if self.state.found_family:
            pyxel.text(2, PLAY_AREA_H + 18, "Family:" + ",".join(sorted(self.state.found_family)), 10)
        self.dialogue.draw()
