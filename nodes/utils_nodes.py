# utils_nodes.py
from typing import Dict, Tuple
from .utils import Categories, dn, log
from .serialization import get_json_string


class MithrilJsonBuilder:
    """
    A node that builds a JSON string from key/value pairs.
    It allows for up to 10 key/value pairs, with a maximum depth for nested structures.

    This node is useful for constructing JSON strings dynamically,
    especially when working with configurations or data that need to be serialized.
    """

    DISPLAY_NAME = dn("JSON Builder")
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "build_json"
    CATEGORY = Categories.UTILS

    _DEFAULT_MAX_DEPTH = 3
    _MIN_DEPTH = 0
    _MAX_DEPTH = 10

    @classmethod
    def INPUT_TYPES(s) -> Dict[str, dict]:
        # Il nodo ha solo un controllo. Tutti gli input sono gestiti da JS.
        return {
            "required": {
                "max_depth": (
                    "INT",
                    {
                        "default": s._DEFAULT_MAX_DEPTH,
                        "min": s._MIN_DEPTH,
                        "max": s._MAX_DEPTH,
                    },
                )
            },
            "optional": {},
        }

    def build_json(self, **kwargs) -> Tuple[str | None]:
        log("Assembling JSON...")

        max_depth = kwargs.pop("max_depth", self._DEFAULT_MAX_DEPTH)

        # Log each key being added
        for key in kwargs:
            log(f"... Adding key '{key}'")

        json_string = get_json_string(kwargs, max_depth=max_depth)

        return (json_string,)
