# serialization.py
import json
import torch


def safe_serialize(obj, max_depth=3, current_depth=0):
    """
    Recursively serializes a Python object into a JSON-compatible structure,
    handling common non-serializable types and preventing infinite recursion.
    """
    if current_depth > max_depth:
        return f"MAX DEPTH ({max_depth}) REACHED"

    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj

    if isinstance(obj, torch.Tensor):
        # Handle tensors by converting them to lists
        return safe_serialize(obj.tolist(), max_depth, current_depth)

    if isinstance(obj, dict):
        # Recurse on dictionary values
        return {
            str(k): safe_serialize(v, max_depth, current_depth + 1)
            for k, v in obj.items()
        }

    if isinstance(obj, (list, tuple)):
        # Recurse on list/tuple items
        return [safe_serialize(item, max_depth, current_depth + 1) for item in obj]

    # For any other object, return its string representation
    return repr(obj)


def get_json_string(obj, max_depth=3):
    """
    Converts an object to a JSON string, safely handling serialization.
    """
    serializable_obj = safe_serialize(obj, max_depth)
    return json.dumps(serializable_obj, indent=3)
