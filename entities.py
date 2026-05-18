"""Player + interactable object primitives. Sprites are drawn with primitives for now."""
import pyxel
from dataclasses import dataclass, field
from typing import Callable

TILE = 8
SCREEN_W = 160
SCREEN_H = 120
PLAY_AREA_H = 84  # leave bottom 36px for dialogue box when active


@dataclass
class Interactable:
    x: int
    y: int
    w: int = TILE
    h: int = TILE
    label: str = "?"
    on_interact: Callable[[], None] = lambda: None
    color: int = 8
    visible: bool = True
    solid: bool = True

    def overlaps(self, x: int, y: int, w: int = TILE, h: int = TILE) -> bool:
        return (
            x < self.x + self.w
            and x + w > self.x
            and y < self.y + self.h
            and y + h > self.y
        )

    def near(self, px: int, py: int) -> bool:
        cx = self.x + self.w // 2
        cy = self.y + self.h // 2
        return abs(cx - (px + TILE // 2)) <= TILE and abs(cy - (py + TILE // 2)) <= TILE

    def draw(self) -> None:
        if not self.visible:
            return
        pyxel.rect(self.x, self.y, self.w, self.h, self.color)
        pyxel.rectb(self.x, self.y, self.w, self.h, 0)


@dataclass
class Player:
    x: int = 80
    y: int = 50
    color: int = 14  # peach/pink for Alison
    speed: int = 1

    def update(self, walls: list[Interactable]) -> None:
        dx = dy = 0
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            dx -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            dx += self.speed
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            dy -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            dy += self.speed
        # Move with simple AABB collision against solid interactables
        new_x = max(0, min(SCREEN_W - TILE, self.x + dx))
        if not self._blocked(new_x, self.y, walls):
            self.x = new_x
        new_y = max(0, min(PLAY_AREA_H - TILE, self.y + dy))
        if not self._blocked(self.x, new_y, walls):
            self.y = new_y

    def _blocked(self, x: int, y: int, walls: list[Interactable]) -> bool:
        for w in walls:
            if w.solid and w.visible and w.overlaps(x, y):
                return True
        return False

    def draw(self) -> None:
        # body
        pyxel.rect(self.x, self.y + 2, TILE, TILE - 2, self.color)
        # head
        pyxel.rect(self.x + 2, self.y, 4, 3, 15)
        # eye
        pyxel.pset(self.x + 3, self.y + 1, 0)
