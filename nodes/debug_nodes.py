# debug_nodes.py
from .utils import dn, log, Categories
from .serialization import get_json_string


class MithrilDebugViewer:
    """
    A node that displays data in a formatted way, either on the console or in the UI.
    It can handle any data type and allows for a maximum depth of nested structures.

    This node is useful for debugging and visualizing data structures in a readable format.
    """

    DISPLAY_NAME = dn("Debug Viewer")

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "display_data"
    OUTPUT_NODE = True  # This is crucial for displaying UI data
    CATEGORY = Categories.DEBUG

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "show_on_console": ("BOOLEAN", {"default": True}),
                "show_on_display": ("BOOLEAN", {"default": True}),
                "max_depth": ("INT", {"default": 3, "min": 0, "max": 10}),
            },
            "optional": {"data": ("*",)},
        }

    def display_data(self, show_on_console, show_on_display, max_depth, data=None):
        if data is None:
            return {"ui": {}}

        json_string = get_json_string(data, max_depth)

        if show_on_console:
            log("Debug Data:\n" + "=" * 20)
            log(json_string)
            log("=" * 20)

        ui_data = {}
        if show_on_display:
            ui_data["text"] = [json_string]

        return {"ui": ui_data}
