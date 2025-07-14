# logic_nodes.py
from ._names import MithrilCategories

class MithrilMultiplexer:
    """
    A Multiplexer/Selector node. Now takes labeled inputs.
    Connect MithrilMultiplexerInput outputs to the item inputs.
    """
    LOG_PREFIX = "⚒️ MithrilMultiplexer: "

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("output",)
    FUNCTION = "select_item"
    CATEGORY = MithrilCategories.LOGIC
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "select": ("STRING", {"forceInput": True}),
            },
            "optional": {
                # These inputs now expect instances of MithrilMultiplexerInput
                "item_1": ("MITHRIL_MULTIPLEXER_INPUT",),
                "item_2": ("MITHRIL_MULTIPLEXER_INPUT",),
                "item_3": ("MITHRIL_MULTIPLEXER_INPUT",),
                "item_4": ("MITHRIL_MULTIPLEXER_INPUT",),
                "item_5": ("MITHRIL_MULTIPLEXER_INPUT",),
            }
        }
    
    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        """
        Validates that all connected 'item' inputs carry the same underlying data type.
        Returns False on failure to prevent execution and turn the node red.
        """
        connected_items = []
        for key in sorted(kwargs.keys()):
            if key.startswith("item_") and kwargs[key] is not None:
                connected_items.append(kwargs[key])
        
        if len(connected_items) >= 2:
            first_item_data_type = type(connected_items[0].get_data())
            for i, item in enumerate(connected_items[1:], start=2):
                current_item_data_type = type(item.get_data())
                if current_item_data_type is not first_item_data_type:
                    # Print the detailed error to the console for debugging.
                    error_message = f"{cls.LOG_PREFIX} Type Mismatch: Input 1 is '{first_item_data_type.__name__}', but Input {i} is '{current_item_data_type.__name__}'."
                    print(error_message)
                    # Return False to signal invalidation without confusing error messages.
                    return False
        
        # If all checks pass, return True.
        return True
 
    def select_item(self, select, **kwargs):
        # We can use **kwargs here to simplify getting the items.
        items_with_instances = [kwargs[key] for key in sorted(kwargs.keys()) if key.startswith("item_") and kwargs[key] is not None]
        
        # Create a map using the methods of the instances
        item_map = {instance.get_label(): instance.get_data() for instance in items_with_instances}
        if not item_map:
            raise ValueError(self.LOG_PREFIX + "No labeled items connected.")
        
        # This runtime type check is still a good fallback.
        all_data = list(item_map.values())
        if len(all_data) > 1:
            first_item_type = type(all_data[0])
            for item in all_data[1:]:
                if type(item) is not first_item_type:
                    raise ValueError(self.LOG_PREFIX + f"Runtime Type mismatch! All inputs must be the same. Expected {first_item_type.__name__}, but found {type(item).__name__}.")

        if select not in item_map:
            raise ValueError(self.LOG_PREFIX + f"Selected label '{select}' not found. Available labels: {list(item_map.keys())}")
        
        selected_item = item_map[select]
        print(self.LOG_PREFIX + f"Selected '{select}'.")
        
        return (selected_item,)
    
    

    
    
class MithrilMultiplexerInput:
    """
    Attaches a string label to any data type that is passed through.
    Useful for naming inputs for the Mithril Multiplexer.
    """
    def __init__(self):
        self._data = None
        self._label = None
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "label": ("STRING", {"default": "default_label"}),
                "data": ("*",),
            }
        }
    
    # We are now outputting a single, special type.
    RETURN_TYPES = ("MITHRIL_MULTIPLEXER_INPUT",) 
    RETURN_NAMES = ("multiplexer_input",)
    FUNCTION = "label_data"
    CATEGORY = MithrilCategories.LOGIC

    def label_data(self, label, data):
        # Store the data and label in the instance
        self._data = data
        self._label = label
        # Return this instance
        return (self,)
    
    def get_data(self):
        """Method that MithrilMultiplexer can call to get the wrapped data"""
        return self._data
    
    def get_label(self):
        """Method that MithrilMultiplexer can call to get the label"""
        return self._label