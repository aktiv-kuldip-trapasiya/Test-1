# -*- coding: utf-8 -*-
# Part of Odoo, SuperFoodsOnline and Aktiv Software.
# See LICENSE file for full copyright & licensing details.

from odoo.tools.float_utils import float_compare
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    actual_purchase_price = fields.Float(
        string="Actual Purchase Price",
        compute="_compute_actual_purchase_price",
        help="True COGS including landed costs and backorder fulfillment, based on valuation layers.",
    )
    pre_actual_purchase_price = fields.Float("Pre Actual Purchase Price", copy=False)

    def _compute_actual_purchase_price(self):
        """
        Compute the actual purchase price of a sale order line product based on FIFO costing,
        including landed costs.

        This method calculates the real cost of a product sold in a Sale Order Line by:
        1. Fetching the related lot (serial/batch) from the stock moves.
        2. Identifying the most recent completed Purchase Order (PO) related to that lot and product.
        3. From that PO, fetching the corresponding incoming stock picking (receipt).
        4. Summing the PO unit price and any applicable landed cost allocations (e.g., freight, duties)
           from associated `stock.landed.cost` records.

        Conditions:
        - Only applies if the product uses FIFO as the costing method.
        - Only considers completed Purchase Orders and Pickings (`state == 'done'`).
        - Landed costs are only added if:
            - They are validated (`state == 'done'`)
            - They are linked to the PO's picking
            - The product appears in the landed cost's valuation adjustment lines

        Updates the `actual_purchase_price` field with:
        - The unit price from the purchase order
        - Plus any additional landed costs allocated to the product

        This is useful for margin analysis, real profitability tracking, and advanced costing scenarios
        where true landed cost must be known.

        Note:
        - Assumes `lot_id.purchase_order_ids` is correctly populated via custom logic or automated linkage.
        - This method runs per sale order line.

        Models used:
        - `stock.move` and `stock.move.line` for lot tracking
        - `purchase.order` and `purchase.order.line` for purchase details
        - `stock.landed.cost` and `stock.valuation.adjustment.lines` for landed cost distribution
        """
        for line in self:
            line.actual_purchase_price = 0
            lot_ids = line.move_ids.move_line_ids.mapped("lot_id")
            for lot_id in lot_ids:
                if (
                    lot_id
                    and line.product_id.categ_id.with_company(
                        line.company_id
                    ).property_cost_method
                    == "fifo"
                ):
                    pos_with_receipts = []
                    po_receipt_map = {}

                    for po in lot_id.purchase_order_ids:
                        incoming_done_pickings = po.picking_ids.filtered(
                            lambda p: p.picking_type_id.code == "incoming"
                            and p.state == "done"
                        )
                        if incoming_done_pickings:
                            pos_with_receipts.append(po)
                            po_receipt_map[po.id] = incoming_done_pickings

                    # Sort the POs by the latest done date of their incoming pickings
                    sorted_pos = sorted(
                        pos_with_receipts,
                        key=lambda po: max(po_receipt_map[po.id].mapped("date_done")),
                        reverse=True,
                    )

                    latest_po = sorted_pos[0] if sorted_pos else False

                    if latest_po:
                        receipt_of_latest_po = po_receipt_map.get(
                            latest_po.id, self.env["stock.picking"]
                        )

                        for order_line in latest_po.order_line:
                            if (
                                order_line.product_id
                                == line.product_id.with_company(line.company_id)
                                and order_line.product_qty == order_line.qty_received
                            ):
                                line.actual_purchase_price += order_line.price_unit
                                if receipt_of_latest_po:
                                    landed_costs = self.env["stock.landed.cost"].search(
                                        [
                                            (
                                                "picking_ids",
                                                "in",
                                                [receipt_of_latest_po.id],
                                            ),
                                            ("state", "=", "done"),
                                        ]
                                    )
                                    for landed_cost in landed_costs:
                                        if any(
                                            pick in latest_po.picking_ids
                                            for pick in landed_cost.picking_ids
                                        ):
                                            for (
                                                val_line
                                            ) in landed_cost.valuation_adjustment_lines:
                                                if (
                                                    val_line.product_id
                                                    == line.product_id.with_company(
                                                        line.company_id
                                                    )
                                                ):
                                                    # Use per-unit landed cost
                                                    per_unit_landed_cost = 0.0
                                                    if val_line.quantity:
                                                        per_unit_landed_cost = (
                                                            val_line.additional_landed_cost
                                                            / val_line.quantity
                                                        )
                                                    line.actual_purchase_price += (
                                                        per_unit_landed_cost
                                                    )
