# -*- coding: utf-8 -*-
from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _mm_hidden_ptav_ids(self):
        """Ids of `product.template.attribute.value` to HIDE on the frontend.

        A variant value is hidden when EVERY active variant carrying it has
        `allow_out_of_stock_order = False` (the per-variant boolean redefined by
        `pos_product_display_mode`). If at least one variant carrying the value
        is ticked (True), the value stays visible — so a value shared by several
        variants (e.g. a single-value attribute) is never hidden by accident.
        """
        self.ensure_one()
        tmpl = self.sudo()
        Ptav = tmpl.env['product.template.attribute.value']
        shown = Ptav
        hidden = Ptav
        for variant in tmpl.product_variant_ids:  # active variants only
            ptavs = variant.product_template_attribute_value_ids
            if variant.allow_out_of_stock_order:
                shown |= ptavs
            else:
                hidden |= ptavs
        return (hidden - shown).ids

    def _mm_has_visible_variant(self):
        """True if at least one active variant is ticked (allow_out_of_stock_order)."""
        self.ensure_one()
        return any(
            variant.allow_out_of_stock_order
            for variant in self.sudo().product_variant_ids
        )

    def _get_additional_configurator_data(
        self, product_or_template, date, currency, pricelist, **kwargs
    ):
        """Send the hidden-value ids to the Owl "Configure your product" popup.

        That configurator is client-rendered from JSON, so it cannot be filtered
        by the server-side QWeb used for the product page / quick view. The JS
        (static/src/js/product_configurator_hide_variants.js) reads these ids to
        drop the corresponding value chips and to disable "Proceed" when a line
        has no visible value left.
        """
        data = super()._get_additional_configurator_data(
            product_or_template, date, currency, pricelist, **kwargs
        )
        template = product_or_template
        if template._name == 'product.product':
            template = template.product_tmpl_id
        data['mm_hidden_ptav_ids'] = template._mm_hidden_ptav_ids()
        return data
