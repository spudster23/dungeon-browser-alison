"""Room 1: The Kitchen. Intro + 3 puzzles: coffee cabinet, login riddle, fridge magnet code."""
import pyxel
from rooms.base import Room
from entities import Interactable, TILE, SCREEN_W, PLAY_AREA_H


CORRECT_CABINET = 1  # the middle one of three


class KitchenRoom(Room):
    name = "The Kitchen"
    bg_color = 6  # off-white

    def intro_lines(self):
        return [
            ("THE BROWSER", "Welcome, Alison Gretz. Subject 0x40."),
            ("THE BROWSER", "Your house has been inducted into FLOOR 1 of the Browser."),
            ("THE BROWSER", "Family members: relocated. Their return is conditional on your completion of three trivial tasks."),
            ("Alison", "...is this a dream? It's 6am and I haven't had coffee."),
            ("THE BROWSER", "Find coffee. Log in. Open the door. In that order. The narrator suggests starting with the cabinets."),
        ]

    def setup(self) -> None:
        # Walls: counter along top
        self.walls = [
            Interactable(0, 0, SCREEN_W, 8, "counter", color=4, solid=True),
        ]
        # Cabinets along top
        self.cabinets = [
            Interactable(16, 12, TILE, TILE, "cabinet", color=4),
            Interactable(40, 12, TILE, TILE, "cabinet", color=4),
            Interactable(64, 12, TILE, TILE, "cabinet", color=4),
        ]
        for i, cab in enumerate(self.cabinets):
            cab.on_interact = lambda i=i: self._check_cabinet(i)
        # Fridge (login riddle)
        self.fridge = Interactable(120, 12, TILE, TILE * 2, "fridge", color=7)
        self.fridge.on_interact = self._login_riddle
        # Magnets on fridge - 4 magnets that must be touched in order 1,2,3,4
        self.magnet_order: list[int] = []
        self.magnets = [
            Interactable(100 + i * 6, 38, 4, 4, f"m{n}", color=10 + i)
            for i, n in enumerate([3, 1, 4, 2])  # display order: 3,1,4,2
        ]
        self.magnet_labels = [3, 1, 4, 2]
        for i in range(4):
            self.magnets[i].on_interact = lambda n=self.magnet_labels[i]: self._magnet_press(n)
            self.magnets[i].solid = False
        # Door (exit)
        self.exit_object = Interactable(SCREEN_W - TILE - 2, PLAY_AREA_H - TILE - 2, TILE, TILE, "door", color=13)
        self.exit_object.solid = False
        self.objects = self.cabinets + [self.fridge] + self.magnets

    def _check_cabinet(self, idx: int) -> None:
        if self.state.flag("kitchen", "coffee"):
            self.dialogue.say("Just empty mugs and an air fryer manual.", "Alison")
            return
        if idx == CORRECT_CABINET:
            self.state.set_flag("kitchen", "coffee")
            self.state.add_item("coffee")
            self.dialogue.say("Coffee beans! And a sticky note: \"Carl was here.\"", "Alison")
            self.dialogue.say("Stage 1/3: complete. The fridge is asking for credentials.", "THE BROWSER")
        else:
            self.dialogue.say("Just empty mugs and an air fryer manual.", "Alison")

    def _login_riddle(self) -> None:
        if not self.state.flag("kitchen", "coffee"):
            self.dialogue.say("The fridge has a tiny terminal on it. It demands coffee first.", "Alison")
            return
        if self.state.flag("kitchen", "login"):
            self.dialogue.say("LOGIN ACCEPTED. Continue, Subject 0x40.", "THE BROWSER")
            return
        # Cycle through 3 answers using Z presses
        idx = self.state.flag("kitchen", "login_choice", 0) or 0
        choices = ["WAR AND PEACE", "DUNGEON CRAWLER CARL", "THE FOUR HOUR WORK WEEK"]
        if idx >= len(choices):
            idx = 0
        self.dialogue.say(f"FRIDGE: What book did you fall asleep reading? [{idx+1}/{len(choices)}] {choices[idx]} (Z again to cycle, X to confirm)", "Alison")
        # advance choice for next interact
        self.state.set_flag("kitchen", "login_choice", (idx + 1) % len(choices))
        self.state.set_flag("kitchen", "login_pending", choices[idx])

    def _magnet_press(self, n: int) -> None:
        if self.state.flag("kitchen", "magnets_done"):
            return
        if not self.state.flag("kitchen", "login"):
            self.dialogue.say("The magnets buzz, ignored.", "Alison")
            return
        expected = len(self.magnet_order) + 1
        if n == expected:
            self.magnet_order.append(n)
            if len(self.magnet_order) == 4:
                self.state.set_flag("kitchen", "magnets_done")
                self.state.add_item("door_key")
                self.dialogue.say("The fridge slides aside. A door appears.", "Alison")
                self.dialogue.say("Stage 3/3 complete. Proceed to the Garage.", "THE BROWSER")
            else:
                self.dialogue.say(f"*click* {n}", "")
        else:
            self.magnet_order.clear()
            self.dialogue.say("*BZZT* The magnets reset.", "")

    def update(self) -> None:
        # Handle login X confirm
        if pyxel.btnp(pyxel.KEY_X) and not self.state.flag("kitchen", "login"):
            pending = self.state.flag("kitchen", "login_pending", "")
            if pending == "DUNGEON CRAWLER CARL":
                self.state.set_flag("kitchen", "login")
                self.state.add_item("bookmark")
                self.dialogue.say("LOGIN ACCEPTED. Stage 2/3 complete.", "THE BROWSER")
                self.dialogue.say("Now arrange the fridge magnets in order: 1, 2, 3, 4.", "THE BROWSER")
            elif pending:
                self.dialogue.say("FRIDGE: That is not the book. Try again.", "")
        super().update()

    def is_complete(self) -> bool:
        return self.state.flag("kitchen", "magnets_done")

    def next_room(self) -> str | None:
        return "garage"
