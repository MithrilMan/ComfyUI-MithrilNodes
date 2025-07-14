from enum import Enum

prefix = '⚒️ '

class CLASSES(Enum):
    MULTIPLEXER_NAME = 'MithrilMultiplexer'
    MULTIPLEXER_DESC = prefix + 'Multiplexer'
    MULTIPLEXER_INPUT_NAME = 'MithrilMultiplexerInput'
    MULTIPLEXER_INPUT_DESC = prefix + 'Multiplexer input'

    TEXT_CONSTANT_NAME = 'MithrilTextConstant'
    TEXT_CONSTANT_DESC = prefix + 'Text constant'
    
    SET_MULTIPLEXER_GATEWAY_NAME = 'SetMithrilMultiplexerGateway'
    SET_MULTIPLEXER_GATEWAY_DESC = prefix + 'Set Multiplexer gateway'
    GET_MULTIPLEXER_GATEWAY_NAME = 'GetMithrilMultiplexerGateway'
    GET_MULTIPLEXER_GATEWAY_DESC = prefix + 'Get Multiplexer gateway'

class MithrilCategories:
    """
    Contain the strings for the categories of MithrilNodes nodes.
    This prevents typos and centralizes the management of names.
    """
    # Main category
    MAIN = "⚒️ MithrilNodes"
    
    # Subcategories
    UTILS = f"{MAIN}/Utils"
    GATEWAYS = f"{MAIN}/Gateways"
    LOGIC = f"{MAIN}/Logic"
    TEXT = f"{MAIN}/Text"

# This file defines the Mithril categories and class names used in the nodes.
# It provides a structured way to categorize nodes and their functionalities.
# This is used in the node definitions to ensure consistent naming and categorization.
# This file is part of the Mithril-Nodes package for ComfyUI.