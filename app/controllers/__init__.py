from .events import event_blueprint
from .index import main_blueprint
from .places import place_blueprint
from .records import record_blueprint
from .users import user_blueprint

__all__ = [
    "event_blueprint",
    "main_blueprint",
    "place_blueprint",
    "record_blueprint",
    "user_blueprint"
]