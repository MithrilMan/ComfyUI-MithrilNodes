# gateway_nodes.py
from .utils import Categories, dn, log

# This global dictionary will hold the actual data during runtime.
GATEWAY_DATA_STORE = {}


class SetMithrilMultiplexerGateway:
    """
    Acts as a named exit point for a Multiplexer's output.
    The name is read by the Getway node at design-time.
    This makes complex graphs cleaner and allows for easy retrieval elsewhere.
    """

    DISPLAY_NAME = dn("Set Multiplexer Gateway")

    # This node has no output, it's a sink.
    RETURN_TYPES = ()
    FUNCTION = "set_gateway"
    OUTPUT_NODE = True  # Important flag for the UI
    CATEGORY = Categories.GATEWAYS

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "gateway_name": ("STRING", {"default": "output_1"}),
                "data": ("*",),
            }
        }

    def set_gateway(self, gateway_name, data):
        # The only job of this node at runtime is to store the data.
        GATEWAY_DATA_STORE[gateway_name] = data
        return {"ui": {"text": [f"Set: {gateway_name}"]}}


class GetMithrilMultiplexerGateway:
    """
    Retrieves data from a named Gateway. The dropdown is populated by JavaScript
    by scanning the graph for all SetMithrilMultiplexerGateway nodes.
    """

    DISPLAY_NAME = dn("Get Multiplexer Gateway")

    RETURN_TYPES = ("*",)
    FUNCTION = "get_gateway"
    CATEGORY = Categories.GATEWAYS
    OUTPUT_NODE = True  # Important flag for the UI

    @classmethod
    def INPUT_TYPES(s):
        # We only provide a placeholder. The JS will provide the real values.
        return {
            "required": {
                "gateway_name": (["N/A"],),
            }
        }

    def get_gateway(self, gateway_name):
        if gateway_name == "N/A" or gateway_name not in GATEWAY_DATA_STORE:
            raise ValueError(
                f"⚒️ MithrilGateway: Gateway '{gateway_name}' not found or has not been executed yet."
            )

        return (GATEWAY_DATA_STORE[gateway_name],)
