"""Room 4: The Server Room. Find Dad. 3 puzzles using items from prior rooms + final dialogue."""
import pyxel
from rooms.base import Room
from entities import Interactable, TILE, SCREEN_W, PLAY_AREA_H


CONSOLES = [
    ("door_key", "console_a", "Console A demands a KEY. The door key fits the slot."),
    ("wrench", "console_b", "Console B has stripped bolts. The WRENCH bites."),
    ("crayon", "console_c", "Console C is a screen. The MAGIC CRAYON scribbles past its DRM."),
]


class ServerRoom(Room):
    name = "The Server Room"
    bg_color = 1  # dark blue

    def intro_lines(self):
        return [
            ("THE BROWSER", "FLOOR 1 - FINAL ROOM: The Server Room."),
            ("Husband (typing)", "Honey? I'm fine. I'm just... I'm in the server itself. It's actually fascinating?"),
            ("Alison", "We are getting OUT of this dungeon and I am going to read a book in BED."),
            ("THE BROWSER", "Three consoles. Three items. One escape."),
        ]

    def setup(self) -> None:
        self.consoles = []
        for i, (item, key, _) in enumerate(CONSOLES):
            c = Interactable(20 + i * 40, 24, TILE * 2, TILE * 2, key, color=3)
            c.on_interact = lambda i=i: self._console(i)
            self.consoles.append(c)
        self.husband = Interactable(SCREEN_W - 30, 50, TILE, TILE, "Dad", color=9)
        self.husband.on_interact = self._save_husband
        self.husband.visible = False
        self.exit_object = Interactable(SCREEN_W - TILE - 2, PLAY_AREA_H - TILE - 2, TILE, TILE, "logout", color=13)
        self.exit_object.solid = False
        self.objects = self.consoles + [self.husband]

    def _console(self, i: int) -> None:
        item, key, success = CONSOLES[i]
        if self.state.flag("server_room", key):
            self.dialogue.say("Already activated. Humming softly.", "")
            return
        if not self.state.has(item):
            self.dialogue.say(f"This console needs the {item.replace('_', ' ').upper()}. You don't have it.", "Alison")
            return
        self.state.set_flag("server_room", key)
        self.dialogue.say(success, "Alison")
        active = sum(self.state.flag("server_room", k) for _, k, _ in CONSOLES)
        if active == 3:
            self.husband.visible = True
            self.dialogue.say("All three consoles online. The cage around your husband disengages.", "THE BROWSER")

    def _save_husband(self) -> None:
        if "husband" in self.state.found_family:
            return
        self.state.found_family.add("husband")
        self.dialogue.say("Hi, hon. I almost have a working theory about The Browser's architecture.", "Husband")
        self.dialogue.say("Tell me in the car. WHERE'S THE EXIT.", "Alison")
        self.dialogue.say("THE BROWSER thanks Subject 0x40 for completing Floor 1. Floor 2: queued.", "THE BROWSER")

    def is_complete(self) -> bool:
        return "husband" in self.state.found_family

    def next_room(self) -> str | None:
        return "ending"
