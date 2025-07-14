import { app } from "/scripts/app.js";

/**
 * A class to handle all UI modifications for the Mithril-Nodes suite.
 * This keeps the code organized and easy to maintain for future additions.
 */
class MithrilUI {

	/**
	 * Adds specific context menus to the MithrilMultiplexer node.
	 * This is called for the node type when it's being registered.
	 * @param {typeof LGraphNode} nodeType The LGraphNode class of the node to modify.
	 */
	addMultiplexerContextMenu(nodeType) {
		const original_getSlotMenuOptions = nodeType.prototype.getSlotMenuOptions;
		const self = this;

		nodeType.prototype.getSlotMenuOptions = function(slot) {
			const menu = original_getSlotMenuOptions ? original_getSlotMenuOptions.apply(this, arguments) : [];
			
			// Menu for INPUT slots ("item_..."): Add a Labeller
			if (slot.input && slot.input.name.startsWith("item_")) {
				menu.push({
					content: "Add Multiplexer Input",
					callback: () => self.addLabeller(this, slot),
				});
			}

			// Menu for OUTPUT slot ("output"): Add a Set Gateway
			if (slot.output && this.outputs[slot.slot]?.name === "output") {
				menu.push({
					content: "Add Set Gateway",
					callback: () => self.addGateway(this, slot),
				});
			}
			return menu;
		};
	}

	/**
	 * Patches the GetGateway node to have a dynamic dropdown that scans the graph.
	 * This is the "magic" for the real-time design-time updates.
	 * @param {typeof LGraphNode} nodeType The LGraphNode class of the node to modify.
	 */
	addDynamicGatewayWidget(nodeType) {
		const original_onNodeCreated = nodeType.prototype.onNodeCreated;

		nodeType.prototype.onNodeCreated = function() {
			original_onNodeCreated?.apply(this, arguments);

			const widget = this.widgets.find(w => w.name === "gateway_name");
			if (!widget) {
				console.error("Mithril-UI: Could not find 'gateway_name' widget on GetGateway node.");
				return;
			}
			
			// This is the KJNodes technique. The values of the dropdown are provided by a function
			// that runs every time the user clicks on the widget.
			widget.options.values = () => {
				// Scan the graph for all nodes of the "SetMithrilMultiplexerGateway" type.
				const setterNodes = app.graph.findNodesByType("SetMithrilMultiplexerGateway");
				
				// Get the value of the 'gateway_name' widget from each of those nodes.
				const names = setterNodes.map(n => n.widgets.find(w => w.name === "gateway_name")?.value || "");
				
				// Return a unique, sorted list of non-empty names for the dropdown.
				const uniqueNames = [...new Set(names.filter(n => n))].sort();
				
				return uniqueNames.length ? uniqueNames : ["N/A"];
			};
		};
	}

	/**
	 * Creates a Labeller node and connects it to a multiplexer's input slot.
	 * @param {LGraphNode} multiplexerNode The multiplexer node instance.
	 * @param {object} slot The rich slot object that was right-clicked.
	 */
	addLabeller(multiplexerNode, slot) {
		const labellerNode = LiteGraph.createNode("MithrilMultiplexerInput");
		app.graph.add(labellerNode);

		// Get the absolute position of the slot on the canvas to position correctly.
		const slotPos = multiplexerNode.getConnectionPos(true, slot.slot);
		labellerNode.pos = [
			slotPos[0] - labellerNode.size[0] - 30, // Position to the left
			slotPos[1] - labellerNode.size[1] / 2   // Center vertically
		];
		
		// Connect the Labeller's output (index 0) to the Multiplexer's clicked input slot.
		labellerNode.connect(0, multiplexerNode, slot.slot);
		app.graph.setDirtyCanvas(true, true);
	}

	/**
	 * Creates a Set Gateway node and connects it to a multiplexer's output.
	 * @param {LGraphNode} multiplexerNode The multiplexer node instance.
	 * @param {object} slot The rich slot object that was right-clicked.
	 */
	addGateway(multiplexerNode, slot) {
		const gatewayNode = LiteGraph.createNode("SetMithrilMultiplexerGateway");
		app.graph.add(gatewayNode);
		
		const slotPos = multiplexerNode.getConnectionPos(false, slot.slot);
		gatewayNode.pos = [
			slotPos[0] + 30, // Position to the right
			slotPos[1] - gatewayNode.size[1] / 2
		];

		// Find the 'data' input slot by its name for a robust connection.
		const dataSlotIndex = gatewayNode.inputs.findIndex(s => s.name === 'data');
		if (dataSlotIndex === -1) {
			console.error("Mithril-UI: Could not find 'data' input on SetMithrilMultiplexerGateway node!");
			return;
		}
		
		// Connect the Multiplexer's clicked output slot to the Gateway's 'data' input slot.
		multiplexerNode.connect(slot.slot, gatewayNode, dataSlotIndex);
		app.graph.setDirtyCanvas(true, true);
	}
}

// Register the extension with ComfyUI
app.registerExtension({
	name: "MithrilNodes.UI",
	async beforeRegisterNodeDef(nodeType, nodeData) {
		// This function is called for each node as it is being registered.

		// Create a single, shared instance of our UI manager.
		if (!window.MithrilUI_instance) {
			window.MithrilUI_instance = new MithrilUI();
		}
		const mithrilUI = window.MithrilUI_instance;

		// Apply the correct modification to the correct node type.
		if (nodeData.name === "GetMithrilMultiplexerGateway") {
			mithrilUI.addDynamicGatewayWidget(nodeType);
		}
        
        if (nodeData.name === "MithrilMultiplexer") {
			mithrilUI.addMultiplexerContextMenu(nodeType);
		}
	}
});