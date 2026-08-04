/** @odoo-module **/

// The "Configure your product" popup is Odoo's core Owl Product Configurator.
// It is client-rendered from JSON, so the server-side QWeb that hides values on
// the product page / quick view cannot reach it. Our server override
// (models/product_template.py -> _get_additional_configurator_data) puts the
// ids of the values to hide on each product payload as `mm_hidden_ptav_ids`.
//
//   1. _loadData -> strip the hidden values (and any hidden selected value) from
//      every attribute line, so the configurator simply never shows them.
//   2. _isPossibleCombination -> treat the configuration as invalid (which
//      disables the "Proceed" button, bound to !isPossibleConfiguration()) when
//      a line has no visible value left, or has visible values but none picked.
import { patch } from "@web/core/utils/patch";
import { ProductConfiguratorDialog } from "@sale/js/product_configurator_dialog/product_configurator_dialog";

patch(ProductConfiguratorDialog.prototype, {
    async _loadData() {
        const result = await super._loadData(...arguments);
        for (const product of result?.products || []) {
            const hidden = new Set(product.mm_hidden_ptav_ids || []);
            if (!hidden.size) {
                continue;
            }
            for (const ptal of product.attribute_lines || []) {
                ptal.attribute_values = (ptal.attribute_values || []).filter(
                    (v) => !hidden.has(v.id)
                );
                ptal.selected_attribute_value_ids = (
                    ptal.selected_attribute_value_ids || []
                ).filter((id) => !hidden.has(id));
            }
        }
        return result;
    },

    _isPossibleCombination(product) {
        if (!super._isPossibleCombination(product)) {
            return false;
        }
        // Every attribute line must still have a visible value AND one selected.
        return product.attribute_lines.every(
            (ptal) =>
                (ptal.attribute_values || []).length > 0 &&
                (ptal.selected_attribute_value_ids || []).length > 0
        );
    },
});
