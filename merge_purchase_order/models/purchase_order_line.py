# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    purchasers = fields.Char(string=_("Purchasers"), readonly=True)
