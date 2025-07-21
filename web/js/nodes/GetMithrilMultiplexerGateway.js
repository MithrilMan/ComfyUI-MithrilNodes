import { app } from "/scripts/app.js";

const _ID = "GetMithrilMultiplexerGateway";

function setupNode(nodeType) {
    const original_onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
        original_onNodeCreated?.apply(this);
        const widget = this.widgets.find(w => w.name === "gateway_name");
        if (!widget) return;
        widget.options.values = () => {
            const setterNodes = app.graph.findNodesByType("SetMithrilMultiplexerGateway");
            const names = setterNodes.map(n => n.widgets.find(w => w.name === "gateway_name")?.value || "");
            const uniqueNames = [...new Set(names.filter(n => n))].sort();
            return uniqueNames.length ? uniqueNames : ["N/A"];
        };
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