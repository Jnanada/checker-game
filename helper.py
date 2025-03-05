import json
from typing import Tuple


class CheckerEncoder(json.JSONEncoder):
    def default(self, obj):
        from piece import Piece

        if isinstance(obj, Piece):
            return {
                "color": obj.color,
                "position": obj.position,
                "king": obj.king,
                "direction": obj.direction.name,
            }
        return json.JSONEncoder.default(self, obj)
