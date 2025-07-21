# utils_nodes.py
from .utils import Categories, dn, log


class MithrilTextConstantNode:
    """
    A node that outputs a constant string value.
    Perfect for setting parameters, filenames, or names for GetNamedConfig.
    """

    DISPLAY_NAME = dn("Text Constant")

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "get_text"
    CATEGORY = Categories.PRIMITIVES

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # The widget for the node. "multiline: True" gives a nice text area.
                "text": ("STRING", {"multiline": True, "default": ""})
            }
        }

    def get_text(self, text):
        # This function simply returns the text from the widget as an output.
        return (text,)
