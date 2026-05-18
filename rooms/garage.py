"""Room 2: The Garage. Find Liam. 3 puzzles: math, skateboard assembly, memory pattern."""
import pyxel
import random
from rooms.base import Room
from entities import Interactable, TILE, SCREEN_W, PLAY_AREA_H


SIMON_SEQUENCE = [0, 2, 1, 3, 0]


class GarageRoom(Room):
    name = "The Garage"
    bg_color = 13  # dim concrete grey

    def intro_lines(self):
        return [
            ("THE BROWSER", "FLOOR 1 - ROOM 2: The Garage. Subject Liam, age 13, detained inside."),
            ("Liam (muffled)", "Mom?? It's me! There's a math problem on the whiteboard and the door won't open."),
            ("Alison", "Of COURSE there is. Hang on, bud."),
            ("THE BROWSER", "Three challenges. Liam's chosen difficulty: \"medium spicy.\""),
        ]

    def setup(self) -> None:
        # Whiteboard (math)
        self.whiteboard = Interactable(20, 14, 24, 16, "whiteboard", color=7)
        self.whiteboard.on_interact = self._math
        # Skateboard parts (deck, trucks, wheels) - interact in order
        self.parts = [
            Interactable(60, 40, TILE, 4, "deck", color=4),
            Interactable(80, 44, TILE, 4, "trucks", color=6),
            Interactable(100, 44, TILE, 4, "wheels", color=0),
        ]
        for i, p in enumerate(self.parts):
            p.on_interact = lambda i=i: self._part(i)
        # Simon buttons
        self.buttons = [
            Interactable(20 + i * 12, 60, TILE, TILE, f"btn{i}", color=8 + i)
            for i in range(4)
        ]
        for i, b in enumerate(self.buttons):
            b.on_interact = lambda i=i: self._simon(i)
            b.solid = False
        # Liam (revealed after all 3 puzzles)
        self.liam = Interactable(SCREEN_W - 30, 40, TILE, TILE, "Liam", color=12)
        self.liam.on_interact = self._save_liam
        self.liam.visible = False
        # Exit door
        self.exit_object = Interactable(SCREEN_W - TILE - 2, PLAY_AREA_H - TILE - 2, TILE, TILE, "door", color=13)
        self.exit_object.solid = False
        self.objects = [self.whiteboard] + self.parts + self.buttons + [self.liam]
        self._sim_progress: list[int] = []
        self._math_choice = 0

    def _math(self) -> None:
        if self.state.flag("garage", "math"):
            self.dialogue.say("WHITEBOARD: 13 + 7 x 3 = 34. (Order of operations, Mom.)", "Liam")
            return
        choices = [60, 34, 27]
        idx = self._math_choice % len(choices)
        self.dialogue.say(f"WHITEBOARD: 13 + 7 x 3 = ? [{idx+1}/3] {choices[idx]} (Z cycle, X confirm)", "Alison")
        self.state.set_flag("garage", "math_pending", choices[idx])
        self._math_choice = (idx + 1) % len(choices)

    def _part(self, i: int) -> None:
        if self.state.flag("garage", "skate"):
            return
        if not self.state.flag("garage", "math"):
            self.dialogue.say("The parts are bolted down. \"Solve math first,\" Liam yells.", "")
            return
        expected = len(self.state.flag("garage", "skate_order", []) or [])
        order = self.state.flag("garage", "skate_order", []) or []
        if i == expected:
            order = list(order) + [i]
            self.state.set_flag("garage", "skate_order", order)
            self.dialogue.say(["Deck.", "Trucks on the deck.", "Wheels on the trucks."][i], "Liam")
            if len(order) == 3:
                self.state.set_flag("garage", "skate")
                self.dialogue.say("Stage 2/3. Now the Simon buttons: red, blue, green, yellow. Pattern: R G B Y R.", "THE BROWSER")
        else:
            self.state.set_flag("garage", "skate_order", [])
            self.dialogue.say("That goes on AFTER the previous part. Start over.", "Liam")

    def _simon(self, i: int) -> None:
        if self.state.flag("garage", "simon"):
            return
        if not self.state.flag("garage", "skate"):
            self.dialogue.say("The buttons are dim. Skateboard first.", "")
            return
        expected = SIMON_SEQUENCE[len(self._sim_progress)]
        if i == expected:
            self._sim_progress.append(i)
            self.dialogue.say(f"*beep* ({len(self._sim_progress)}/{len(SIMON_SEQUENCE)})", "")
            if len(self._sim_progress) == len(SIMON_SEQUENCE):
                self.state.set_flag("garage", "simon")
                self.liam.visible = True
                self.dialogue.say("The cage releases. LIAM IS FREE.", "THE BROWSER")
        else:
            self._sim_progress.clear()
            self.dialogue.say("*BZZT* Reset.", "")

    def _save_liam(self) -> None:
        if "liam" in self.state.found_family:
            self.dialogue.say("Right behind you, Mom. I got the wrench.", "Liam")
            return
        self.state.found_family.add("liam")
        self.state.add_item("wrench")
        self.dialogue.say("Mom! I got a wrench out of the toolbox - we might need it.", "Liam")
        self.dialogue.say("Stage complete. Proceed to The Library. Subject Maisie awaits.", "THE BROWSER")

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_X) and not self.state.flag("garage", "math"):
            pending = self.state.flag("garage", "math_pending", None)
            if pending == 34:
                self.state.set_flag("garage", "math")
                self.dialogue.say("CORRECT. Stage 1/3.", "THE BROWSER")
                self.dialogue.say("Now assemble the skateboard: deck, trucks, wheels.", "THE BROWSER")
            elif pending is not None:
                self.dialogue.say("WRONG. Order of operations, Mom!", "Liam")
        super().update()

    def is_complete(self) -> bool:
        return "liam" in self.state.found_family

    def next_room(self) -> str | None:
        return "library"
