import { app } from "/scripts/app.js";

const _ID = "MithrilMultiplexer";
const _LABELER_NAME = "MithrilMultiplexerInput";
const _SET_GATEWAY_NAME = "SetMithrilMultiplexerGateway";

function setupNodes(nodeType) {
    const original_getSlotMenuOptions = nodeType.prototype.getSlotMenuOptions;
    const self = this;
    nodeType.prototype.getSlotMenuOptions = function (slot) {
        const menu = original_getSlotMenuOptions ? original_getSlotMenuOptions.apply(this, arguments) : [];
        if (slot.input && slot.input.name.startsWith("item_")) {
            menu.push({ content: "Add Multiplexer Input", callback: () => addLabeller(this, slot) });
        }
        if (slot.output && this.outputs[slot.slot]?.name === "output") {
            menu.push({ content: "Add Set Gateway", callback: () => addGateway(this, slot) });
        }
        return menu;
    };

    /**
     * Creates a Labeller node and connects it to a multiplexer's input slot.
     * @param {LGraphNode} multiplexerNode The multiplexer node instance.
     * @param {object} slot The rich slot object that was right-clicked.
     */
    function addLabeller(multiplexerNode, slot) {
        const labellerNode = LiteGraph.createNode(_LABELER_NAME);
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
    };

    /**
     * Creates a Set Gateway node and connects it to a multiplexer's output.
     * @param {LGraphNode} multiplexerNode The multiplexer node instance.
     * @param {object} slot The rich slot object that was right-clicked.
     */
    function addGateway(multiplexerNode, slot) {
        const gatewayNode = LiteGraph.createNode(_SET_GATEWAY_NAME);
        app.graph.add(gatewayNode);

        const slotPos = multiplexerNode.getConnectionPos(false, slot.slot);
        gatewayNode.pos = [
            slotPos[0] + 30, // Position to the right
            slotPos[1] - gatewayNode.size[1] / 2
        ];

        // Find the 'data' input slot by its name for a robust connection.
        const dataSlotIndex = gatewayNode.inputs.findIndex(s => s.name === 'data');
        if (dataSlotIndex === -1) {
            console.error(`Gateway node ${gatewayNode.id} does not have a 'data' input slot.`);
            return;
        }

        // Connect the Multiplexer's clicked output slot to the Gateway's 'data' input slot.
        multiplexerNode.connect(slot.slot, gatewayNode, dataSlotIndex);
        app.graph.setDirtyCanvas(true, true);
    };
}


app.registerExtension({
    name: "Mithril:" + _ID,

    setup() {
        console.log(`Mithril-UI: ${_ID} nodes setup complete.`);
    },

    beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData?.name !== _ID) return;

        setupNode(nodeType);
    }
});