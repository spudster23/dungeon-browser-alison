"""Shared mutable game state passed between rooms and the main loop."""
from dataclasses import dataclass, field


@dataclass
class GameState:
    current_room: str = "title"
    next_room: str | None = None
    inventory: list[str] = field(default_factory=list)
    found_family: set[str] = field(default_factory=set)
    # Per-room puzzle flags. Each room owns its own sub-dict.
    flags: dict[str, dict] = field(default_factory=dict)

    def add_item(self, item: str) -> None:
        if item not in self.inventory:
            self.inventory.append(item)

    def has(self, item: str) -> bool:
        return item in self.inventory

    def flag(self, room: str, key: str, default=False):
        return self.flags.setdefault(room, {}).get(key, default)

    def set_flag(self, room: str, key: str, value=True) -> None:
        self.flags.setdefault(room, {})[key] = value
