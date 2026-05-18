"""Room 3: The Library. Find Maisie. 3 puzzles: color-match shelves, hidden bookmark, shape pedestals."""
import pyxel
from rooms.base import Room
from entities import Interactable, TILE, SCREEN_W, PLAY_AREA_H


# Match each book to its shelf by color. Order doesn't matter; all 4 pairs needed.
SHELF_COLORS = [8, 11, 12, 10]  # red, green, blue, yellow

# Carl-themed shelf index where the bookmark is hidden
CARL_SHELF = 2

# Shape pedestals: must be activated in order circle, square, triangle (0,1,2)
SHAPE_ORDER = [0, 1, 2]


class LibraryRoom(Room):
    name = "The Library"
    bg_color = 4  # brown

    def intro_lines(self):
        return [
            ("THE BROWSER", "FLOOR 1 - ROOM 3: The Library. Subject Maisie, age 6, currently giggling somewhere."),
            ("Maisie (faint)", "MOMMYYYY! There's a TALKING SHELF and it sings!"),
            ("Alison", "Maisie, sweetie, where are you?"),
            ("Maisie", "BEHIND the books. The SECRET ones."),
            ("THE BROWSER", "Three challenges. Color-match the shelves. Find the hidden bookmark. Activate the shapes."),
        ]

    def setup(self) -> None:
        # 4 shelves with colored bands at top
        self.shelves = []
        for i, c in enumerate(SHELF_COLORS):
            s = Interactable(10 + i * 28, 14, 20, 18, f"shelf{i}", color=c)
            s.on_interact = lambda i=i: self._shelf(i)
            self.shelves.append(s)
        # 4 books on floor, each colored - player picks up and "deposits"
        self.books = []
        for i, c in enumerate(SHELF_COLORS):
            b = Interactable(20 + i * 28, 50, 6, 4, f"book{i}", color=c)
            b.on_interact = lambda i=i: self._pick_book(i)
            b.solid = False
            self.books.append(b)
        # Shape pedestals
        self.pedestals = [
            Interactable(20 + i * 18, 64, TILE, TILE, ["circle", "square", "tri"][i], color=6)
            for i in range(3)
        ]
        for i, p in enumerate(self.pedestals):
            p.on_interact = lambda i=i: self._pedestal(i)
        # Maisie (revealed)
        self.maisie = Interactable(SCREEN_W - 30, 40, TILE, TILE, "Maisie", color=14)
        self.maisie.on_interact = self._save_maisie
        self.maisie.visible = False
        self.exit_object = Interactable(SCREEN_W - TILE - 2, PLAY_AREA_H - TILE - 2, TILE, TILE, "door", color=13)
        self.exit_object.solid = False
        self.objects = self.shelves + self.books + self.pedestals + [self.maisie]

    def _pick_book(self, i: int) -> None:
        if self.state.flag("library", "colors"):
            return
        if self.state.flag("library", "holding", None) is not None:
            self.dialogue.say("You're already holding a book.", "")
            return
        if i in (self.state.flag("library", "placed", []) or []):
            return
        self.state.set_flag("library", "holding", i)
        self.dialogue.say(f"Picked up the {['red','green','blue','yellow'][i]} book.", "Alison")

    def _shelf(self, i: int) -> None:
        if self.state.flag("library", "colors"):
            if i == CARL_SHELF and not self.state.flag("library", "carl"):
                self.state.set_flag("library", "carl")
                self.state.add_item("carl_bookmark")
                self.dialogue.say("Inside DUNGEON CRAWLER CARL: a fresh bookmark with a tiny crayon drawing.", "Alison")
                self.dialogue.say("Stage 2/3. Now: the shape pedestals.", "THE BROWSER")
            else:
                self.dialogue.say("Just books. Books and dust.", "Alison")
            return
        held = self.state.flag("library", "holding", None)
        if held is None:
            self.dialogue.say("Bring a book to this shelf, it whispers.", "")
            return
        if held == i:
            placed = list(self.state.flag("library", "placed", []) or [])
            placed.append(i)
            self.state.set_flag("library", "placed", placed)
            self.state.set_flag("library", "holding", None)
            self.books[i].visible = False
            self.books[i].solid = False
            self.dialogue.say("The shelf hums approvingly.", "")
            if len(placed) == 4:
                self.state.set_flag("library", "colors")
                self.dialogue.say("Stage 1/3 complete. Now read the SHELVES to find the right book.", "THE BROWSER")
        else:
            self.dialogue.say("Wrong color. The shelf rejects it.", "")
            self.state.set_flag("library", "holding", None)

    def _pedestal(self, i: int) -> None:
        if self.state.flag("library", "shapes"):
            return
        if not self.state.flag("library", "carl"):
            self.dialogue.say("The pedestals are dormant. Find the bookmark first.", "")
            return
        progress = list(self.state.flag("library", "shape_progress", []) or [])
        expected = SHAPE_ORDER[len(progress)]
        if i == expected:
            progress.append(i)
            self.state.set_flag("library", "shape_progress", progress)
            self.dialogue.say(["Circle glows.", "Square glows.", "Triangle glows."][i], "")
            if len(progress) == 3:
                self.state.set_flag("library", "shapes")
                self.maisie.visible = True
                self.dialogue.say("A small chair scoots out. MAISIE IS FREE.", "THE BROWSER")
        else:
            self.state.set_flag("library", "shape_progress", [])
            self.dialogue.say("*nope* Reset.", "")

    def _save_maisie(self) -> None:
        if "maisie" in self.state.found_family:
            self.dialogue.say("I got a crayon, Mommy! Magic kind!", "Maisie")
            return
        self.state.found_family.add("maisie")
        self.state.add_item("crayon")
        self.dialogue.say("MOMMY!! I drew you a map. And I have a MAGIC CRAYON.", "Maisie")
        self.dialogue.say("Subject Maisie recovered. Final room: the Server Room.", "THE BROWSER")

    def is_complete(self) -> bool:
        return "maisie" in self.state.found_family

    def next_room(self) -> str | None:
        return "server_room"

    def draw(self) -> None:
        super().draw()
        # Show held book indicator
        held = self.state.flag("library", "holding", None)
        if held is not None:
            pyxel.text(SCREEN_W - 60, PLAY_AREA_H + 2, f"Holding:{['R','G','B','Y'][held]}", 7)
