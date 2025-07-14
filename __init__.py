"""
@author: Mithril Man
@title: Mithril-Nodes
@nickname: Mithril Man
@version: 0.1.0
@project: "https://github.com/MithrilMan/ComfyUI-MithrilNodes",
@description: Plugins with utility nodes for ComfyUI, including a multiplexer, gateway management nodes, and text constants.
@license: MIT
@notes: This package extends ComfyUI with custom nodes for better data management and routing.
"""

from .nodes._names import CLASSES
from .nodes.logic_nodes import MithrilMultiplexer, MithrilMultiplexerInput
from .nodes.utils_nodes import MithrilTextConstantNode
from .nodes.gateway_nodes import SetMithrilMultiplexerGateway, GetMithrilMultiplexerGateway

# --- Crucially, import the api module to register routes ---
# This ensures the API endpoint exists when the JS calls it.
try:
    import server.api
    print("✅ Mithril-Nodes: Registered custom API endpoints.")
except Exception as e:
    print(f" MITHRIL-NODES-ERROR: Could not import API endpoints: {e}")
    
NODE_CLASS_MAPPINGS = {
    CLASSES.MULTIPLEXER_NAME.value: MithrilMultiplexer,
    CLASSES.MULTIPLEXER_INPUT_NAME.value: MithrilMultiplexerInput,
    CLASSES.TEXT_CONSTANT_NAME.value: MithrilTextConstantNode,
    CLASSES.SET_MULTIPLEXER_GATEWAY_NAME.value: SetMithrilMultiplexerGateway,
    CLASSES.GET_MULTIPLEXER_GATEWAY_NAME.value: GetMithrilMultiplexerGateway,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    CLASSES.MULTIPLEXER_NAME.value: CLASSES.MULTIPLEXER_DESC.value,
    CLASSES.MULTIPLEXER_INPUT_NAME.value: CLASSES.MULTIPLEXER_INPUT_DESC.value,
    CLASSES.TEXT_CONSTANT_NAME.value: CLASSES.TEXT_CONSTANT_DESC.value,
    CLASSES.SET_MULTIPLEXER_GATEWAY_NAME.value: CLASSES.SET_MULTIPLEXER_GATEWAY_DESC.value,
    CLASSES.GET_MULTIPLEXER_GATEWAY_NAME.value: CLASSES.GET_MULTIPLEXER_GATEWAY_DESC.value,
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

print("✅ Loaded Mithril-Nodes with UI extensions")