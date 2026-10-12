"""Headless unit tests for the pure-logic parts (no Pyxel window is opened)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dialogue import _wrap  # noqa: E402
from entities import Interactable  # noqa: E402
from game_state import GameState  # noqa: E402


def test_add_item_is_idempotent():
    s = GameState()
    s.add_item("key")
    s.add_item("key")
    assert s.inventory == ["key"]
    assert s.has("key") and not s.has("book")


def test_flags_are_per_room():
    s = GameState()
    assert s.flag("kitchen", "coffee") is False
    s.set_flag("kitchen", "coffee")
    assert s.flag("kitchen", "coffee") is True
    assert s.flag("garage", "coffee") is False


def test_wrap_respects_width():
    lines = _wrap("the quick brown fox jumps over the lazy dog", width=12)
    assert lines and all(len(line) <= 12 for line in lines)
    assert " ".join(lines) == "the quick brown fox jumps over the lazy dog"


def test_interactable_overlap_and_near():
    box = Interactable(x=10, y=10, w=8, h=8)
    assert box.overlaps(12, 12)
    assert not box.overlaps(30, 30)
    assert box.near(10, 10)
    assert not box.near(100, 100)
