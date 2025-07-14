# Mithril-Nodes for ComfyUI

Mithril-Nodes is a collection of custom nodes for ComfyUI that enhance workflow modularity, data routing, and configuration management. These nodes help you build more dynamic, organized, and reusable pipelines for generative AI workflows.

## What These Custom Nodes Do

- **Mithril Multiplexer**: A selector node that routes one of several labeled inputs to its output, based on a string label. Useful for switching between different data sources or models dynamically.
- **Mithril Multiplexer Input**: Attaches a string label to any data type, making it easy to name and organize inputs for the multiplexer.
- **Set Multiplexer Gateway**: Stores the output of a node under a user-defined gateway name. This acts as a named exit point, allowing you to reference this data elsewhere in the workflow.
- **Get Multiplexer Gateway**: Retrieves data from a named gateway. The dropdown menu is dynamically populated with all available gateway names in the current workflow.
- **Text Constant**: Outputs a constant string value, useful for parameters, filenames, or as a source for gateway names.

These nodes enable:

- Modular and reusable workflow components
- Clean separation of data routing and logic
- Dynamic switching between models, prompts, or settings
- Easy management of complex pipelines with named gateways

## Installation

1. Open the **ComfyUI Manager**.
2. Click on **Install Custom Nodes**.
3. Search for `Mithril-Nodes` and click **Install**.
4. Restart ComfyUI.

## Example Usage

- Use **Mithril Multiplexer Input** nodes to label different data sources.
- Connect them to a **Mithril Multiplexer** to select which input to route based on a label.
- Use **Set Multiplexer Gateway** to store the output under a name.
- Retrieve the stored data anywhere in your workflow with **Get Multiplexer Gateway**.
- Use **Text Constant** nodes for static strings or as gateway names.

(Insert a screenshot of your workflow here to illustrate how the nodes are used.)

![Example workflow](URL_OF_THE_SCREENSHOT_YOU_WILL_UPLOAD_ON_GITHUB)