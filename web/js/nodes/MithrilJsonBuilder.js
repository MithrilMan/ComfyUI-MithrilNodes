import { app } from "/scripts/app.js";
import { SlotType, SlotEventType } from "../common.js";

const _ID = "MithrilJsonBuilder";
const INPUT_NAME_GHOST = "(new parameter)";
const INPUT_NAME_MAX_DEPTH = "max_depth";

function setupNode(nodeType) {

    const original_getSlotMenuOptions = nodeType.prototype.getSlotMenuOptions;
    nodeType.prototype.getSlotMenuOptions = function (slot) {
        const menu = original_getSlotMenuOptions ? original_getSlotMenuOptions.apply(this, arguments) : [];
        if (slot.input && slot.input.name !== INPUT_NAME_MAX_DEPTH && slot.input.name !== INPUT_NAME_GHOST) {
            menu.push({
                content: "Remove Parameter",
                callback: () => {
                    this.removeInput(slot.slot);
                    this.setDirtyCanvas(true, true);
                }
            });
            menu.push({
                content: "Rename Parameter",
                callback: () => {
                    const oldName = slot.input.name;
                    const newNameRaw = prompt("Enter new parameter name:", oldName);
                    if (newNameRaw && newNameRaw !== oldName) {
                        const newNameSanitized = this.sanitizeIdentifier(newNameRaw);
                        if (this.inputs.some(i => i.name === newNameSanitized)) {
                            alert(`Error: Parameter name "${newNameSanitized}" is already in use.`);
                        } else {
                            this.renameSlot(slot.slot, newNameSanitized);
                        }
                    }
                }
            });
        }
        return menu;
    };

    const original_onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
        original_onNodeCreated?.apply(this);
        this.widgets = this.widgets || [];

        this.addWidget("button", "Remove Unconnected", "remove_unconnected", () => {
            this.removeUnconnectedInputs();
        });

        this.addInput(INPUT_NAME_GHOST, "*");

        this.renameSlot = function (slotIndex, newName) {
            this.inputs[slotIndex].name = newName;
            this.setDirtyCanvas(true, true);
        };

        this.sanitizeIdentifier = function (name) {
            if (!name) return `parameter_${this.inputs.length}`;
            let sanitized = name.replace(/[^a-zA-Z0-9_]/g, '');
            if (/^[0-9]/.test(sanitized)) sanitized = '_' + sanitized;
            return sanitized || `parameter_${this.inputs.length}`;
        };

        this.removeUnconnectedInputs = function () {
            for (let i = this.inputs.length - 1; i >= 0; i--) {
                const input = this.inputs[i];
                if (input.name !== INPUT_NAME_MAX_DEPTH && input.name !== INPUT_NAME_GHOST && input.link === null) {
                    this.removeInput(i);
                }
            }
            this.setDirtyCanvas(true, true);
        };

        // Ensure the new slot has proper appearance
        const slot = this.inputs[this.inputs.length - 1];
        if (slot) {
            slot.color_off = "#777";
        }
    };

    // const onConfigure = nodeType.prototype.onConfigure;
    // nodeType.prototype.onConfigure = function () {
    //     onConfigure?.apply(this, arguments);
    //     // Ensure helpers and a clean ghost input exist on loaded nodes
    //     if (!this.renameSlot) {
    //         nodeType.prototype.onNodeCreated.apply(this);
    //     }
    //     // Remove any old ghost inputs from the saved data and add a fresh one.
    //     const ghostIndex = this.inputs.findIndex(i => i.name === INPUT_NAME_GHOST);
    //     if (ghostIndex !== -1) this.removeInput(ghostIndex);
    //     this.addInput(INPUT_NAME_GHOST, "*");
    // };

    const original_onConnectionsChange = nodeType.prototype.onConnectionsChange;
    nodeType.prototype.onConnectionsChange = function (slotType, slotIndex, event, link_info, node_slot) {
        original_onConnectionsChange?.apply(this, arguments);

        if (slotType !== SlotType.Input) return; // Only act on input connections

        const input = this.inputs[slotIndex];

        if (event === SlotEventType.Disconnect) {
            // If the ghost input is disconnected, remove it
            if (input && input.name !== INPUT_NAME_MAX_DEPTH && input.name !== INPUT_NAME_GHOST) {
                this.removeInput(slotIndex);
            }
            return; // No further action needed on disconnect
        }

        if (link_info && input && input.name === INPUT_NAME_GHOST) {
            // get the parent (left side node) from the link
            const fromNode = this.graph._nodes.find(
                (otherNode) => otherNode.id == link_info.origin_id
            )

            if (fromNode) {
                // make sure there is a parent for the link
                const parent_link = fromNode.outputs[link_info.origin_slot];
                if (parent_link) {
                    node_slot.type = parent_link.type;

                    setTimeout(() => {
                        const newNameRaw = prompt("Enter parameter name:", parent_link.name);
                        if (newNameRaw) {
                            const newNameSanitized = this.sanitizeIdentifier(newNameRaw);
                            if (this.inputs.some(i => i.name === newNameSanitized)) {
                                alert(`Error: Parameter name "${newNameSanitized}" is already in use.`);
                                app.graph.removeLink(link_info.id);
                            } else {
                                this.renameSlot(slotIndex, newNameSanitized);
                                this.addInput(INPUT_NAME_GHOST, "*");
                            }
                        } else { // User cancelled the prompt, so remove the link
                            app.graph.removeLink(link_info.id);
                        }
                    }, 10);

                    // // use comfyui prompt to get the name of the parameter
                    // LGraphCanvas.active_canvas.prompt("Enter parameter name:", parent_link.name, function (newNameRaw) {
                    //     if (newNameRaw) {
                    //         const newNameSanitized = this.sanitizeIdentifier(newNameRaw);
                    //         if (this.inputs.some(i => i.name === newNameSanitized)) {
                    //             alert(`Error: Parameter name "${newNameSanitized}" is already in use.`);
                    //             app.graph.removeLink(link_info.id);
                    //         } else {
                    //             this.renameSlot(slotIndex, newNameSanitized);
                    //             this.addInput(INPUT_NAME_GHOST, "*");
                    //         }
                    //     } else { // User cancelled the prompt, so remove the link
                    //         app.graph.removeLink(link_info.id);
                    //         this.setDirtyCanvas(true, true);
                    //     }
                    // }.bind(this));
                }
            }
        }
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