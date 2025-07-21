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

import os
import importlib
import inspect

# --- Automatic Node Discovery and Mapping ---

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Get the path to the 'nodes' directory
nodes_dir = os.path.join(os.path.dirname(__file__), "nodes")

# Iterate over all .py files in the 'nodes' directory
for filename in os.listdir(nodes_dir):
    if filename.endswith(".py") and not filename.startswith("_"):
        module_name = filename[:-3] # Remove the .py extension
        print(f"🔍 Mithril-Nodes: Attempting to load nodes from {module_name}...")
        try:
            # Import the module
            module = importlib.import_module(f".nodes.{module_name}", __name__)
            
            # Iterate over all members of the module
            for name, obj in inspect.getmembers(module):
                # Check if the member is a class defined in this module
                if inspect.isclass(obj) and obj.__module__ == module.__name__:
                    # Check if it has the required metadata
                    if hasattr(obj, 'DISPLAY_NAME'):
                        node_name = name
                        display_name = obj.DISPLAY_NAME
                        
                        NODE_CLASS_MAPPINGS[node_name] = obj
                        NODE_DISPLAY_NAME_MAPPINGS[node_name] = display_name
                        
                        print(f"✅ Mithril-Nodes: Registered node '{node_name}' as '{display_name}'")

        except Exception as e:
            print(f" MITHRIL-NODES-ERROR: Failed to load nodes from {filename}: {e}")

# list the mappings for debugging
print("Mithril-Nodes: Node Class Mappings:")
for node_name, cls in NODE_CLASS_MAPPINGS.items():
    print(f" - {node_name}: {cls.__name__}")    
    

# --- Import API and set Web Directory ---
# try:
#     import server.api
#     print("✅ Mithril-Nodes: Registered custom API endpoints.")
# except Exception as e:
#     print(f" MITHRIL-NODES-ERROR: Could not import API endpoints: {e}")

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

print("✅ Loaded Mithril-Nodes with UI extensions")