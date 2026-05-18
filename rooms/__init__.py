from .base import Room
from .title import TitleRoom
from .kitchen import KitchenRoom
from .garage import GarageRoom
from .library import LibraryRoom
from .server_room import ServerRoom
from .ending import EndingRoom

ROOM_REGISTRY = {
    "title": TitleRoom,
    "kitchen": KitchenRoom,
    "garage": GarageRoom,
    "library": LibraryRoom,
    "server_room": ServerRoom,
    "ending": EndingRoom,
}
