/** @odoo-module **/

// Hiding of variant VALUES is done server-side (views/hide_variants_templates.xml)
// so there is no flash. This file only covers the edge case that cannot be done
// server-side cleanly: when EVERY value of a variant attribute is hidden (all its
// variants unticked), the attribute renders with no selectable value, so Add to
// Cart must be disabled.
//
// Use WebsiteSale.include() rather than patching VariantMixin (Odoo copies mixin
// methods at extend() time). WebsiteSale drives the product page and Theme Prime's
// Quick View, so this covers both.
import { WebsiteSale } from "@website_sale/js/website_sale";

WebsiteSale.include({
    _onChangeCombination(ev, $parent, combination) {
        this._super(...arguments);
        this._mmToggleAddToCart($parent);
    },

    /**
     * Disable Add to Cart when any variant attribute has no selectable value
     * left (radio/pills/color list with no inputs, or a <select> with no
     * options).
     *
     * @private
     * @param {jQuery} $parent The current `.js_product` container.
     */
    _mmToggleAddToCart($parent) {
        let noSelectableValue = false;

        $parent.find("ul[data-attribute_id]").each(function () {
            if ($(this).find("input.js_variant_change").length === 0) {
                noSelectableValue = true;
                return false;
            }
        });
        if (!noSelectableValue) {
            $parent.find("select.js_variant_change").each(function () {
                if ($(this).find("option").length === 0) {
                    noSelectableValue = true;
                    return false;
                }
            });
        }

        // `.btn.disabled` gives Bootstrap disabled styling and `pointer-events:
        // none`, which blocks the .a-submit click handler.
        $parent
            .closest("form")
            .find("#add_to_cart, #add_to_cart_button")
            .toggleClass("disabled", noSelectableValue)
            .attr("aria-disabled", noSelectableValue);
    },
});
