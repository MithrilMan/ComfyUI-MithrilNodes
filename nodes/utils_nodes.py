# utils_nodes.py
from ._names import MithrilCategories

class MithrilTextConstantNode:
    """
    A node that outputs a constant string value.
    Perfect for setting parameters, filenames, or names for GetNamedConfig.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # The widget for the node. "multiline: True" gives a nice text area.
                "text": ("STRING", {"multiline": True, "default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_text"
    CATEGORY = MithrilCategories.UTILS

    def get_text(self, text):
        # This function simply returns the text from the widget as an output.
        return (text,)